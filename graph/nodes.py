import json
from graph.state import RecruitmentState
from models.schemas import JobDescription, FinalDecision, HiringRubric, RubricCriterion
from tools.parse_resume import parse_resume as parse_resume_tool
from tools.score_candidate import score_candidate
from tools.availability import get_availability
from tools.interview import schedule_interview as schedule_interview_tool
from tools.sanitizer import contains_injection
from prompts.jd_prompt import JD_ANALYSIS_PROMPT
from prompts.planner_prompt import PLANNER_PROMPT
from prompts.decision_prompt import DECISION_PROMPT
from prompts.guardrail_prompt import GUARDRAIL_PROMPT
from prompts.rubric_prompt import RUBRIC_PROMPT
from typing import Any, Callable


def _make_traj_entry(thought: str, tool_used: str, arguments: dict, observation: str, state_changes: dict, decision: str = "") -> dict:
    """Helper to create a structured trajectory entry."""
    return {
        "thought": thought,
        "tool_used": tool_used,
        "arguments": arguments,
        "observation": observation,
        "state_changes": state_changes,
        "decision": decision,
    }


def _inc_step(state: RecruitmentState) -> int:
    """Increment step counter."""
    return state.get("step_count", 0) + 1


def node_parse_jd(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Parse the job description into structured data."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    if state.get("jd_parsed") is not None:
        trajectory.append(_make_traj_entry(
            thought="JD already parsed.",
            tool_used="parse_jd",
            arguments={},
            observation="Skipped - JD already parsed",
            state_changes={},
            decision="SKIP"
        ))
        return {**state, "trajectory": trajectory, "step_count": step}
    
    prompt = JD_ANALYSIS_PROMPT.format(jd=state["jd_raw"])
    response = llm_call(prompt)
    
    try:
        data = json.loads(response)
        jd_parsed = JobDescription(**data)
        trajectory.append(_make_traj_entry(
            thought="Analyze JD to extract structured requirements",
            tool_used="parse_jd",
            arguments={"jd_raw_length": len(state["jd_raw"])},
            observation=f"Parsed JD: {jd_parsed.job_title}",
            state_changes={"jd_parsed": {"from": None, "to": jd_parsed.job_title}},
            decision="PARSED"
        ))
        return {**state, "jd_parsed": jd_parsed, "trajectory": trajectory, "error": None, "step_count": step}
    except (json.JSONDecodeError, Exception) as e:
        trajectory.append(_make_traj_entry(
            thought="JD parsing failed",
            tool_used="parse_jd",
            arguments={},
            observation=f"Failed to parse JD: {str(e)}",
            state_changes={},
            decision="ERROR"
        ))
        return {**state, "trajectory": trajectory, "error": f"JD parse error: {str(e)}", "step_count": step}


def node_create_plan(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Create an evaluation plan."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    jd_json = state["jd_parsed"].model_dump_json() if state.get("jd_parsed") else state["jd_raw"]
    prompt = PLANNER_PROMPT.format(jd=jd_json, resume=state["resume_raw"])
    response = llm_call(prompt)
    
    try:
        data = json.loads(response)
        plan = data.get("plan", [])
        trajectory.append(_make_traj_entry(
            thought="Create step-by-step evaluation plan",
            tool_used="create_plan",
            arguments={"jd": "parsed", "resume": "loaded"},
            observation=f"Created plan: {len(plan)} steps",
            state_changes={"plan": {"from": "[]", "to": f"{len(plan)} steps"}},
            decision="PLANNED"
        ))
        return {**state, "plan": plan, "trajectory": trajectory, "step_count": step}
    except (json.JSONDecodeError, Exception) as e:
        trajectory.append(_make_traj_entry(
            thought="Plan creation needed",
            tool_used="create_plan",
            arguments={},
            observation=f"Plan creation failed: {str(e)}",
            state_changes={},
            decision="ERROR"
        ))
        return {**state, "plan": [], "trajectory": trajectory, "step_count": step}


def node_parse_resume(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Parse the resume into structured data."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    injection_log = list(state.get("injection_log", []))
    
    resume_text = state.get("resume_raw", "")
    print(f"[DEBUG] node_parse_resume: resume_raw={len(resume_text)} chars")
    
    # Check for injection in raw resume
    injections = contains_injection(resume_text)
    if injections:
        injection_log.append(f"injection detected: {len(injections)} pattern(s) in resume")
    
    resume_data = parse_resume_tool(resume_text, llm_call)
    trajectory.append(_make_traj_entry(
        thought="Extract structured information from resume",
        tool_used="parse_resume",
        arguments={"resume_length": len(state["resume_raw"])},
        observation=f"Parsed resume for: {resume_data.candidate_name}",
        state_changes={
            "resume_parsed": {"from": None, "to": f"{resume_data.candidate_name}"},
            "candidate_name": {"from": "", "to": resume_data.candidate_name}
        },
        decision="PARSED"
    ))
    
    return {
        **state,
        "resume_parsed": resume_data,
        "candidate_name": resume_data.candidate_name,
        "trajectory": trajectory,
        "step_count": step,
        "injection_log": injection_log,
    }


def node_score_candidate(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Score the candidate against JD with evidence enforcement."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    injection_log = list(state.get("injection_log", []))
    
    jd_json = state["jd_parsed"].model_dump_json() if state.get("jd_parsed") else state["jd_raw"]
    resume_json = state["resume_parsed"].model_dump_json() if state.get("resume_parsed") else state["resume_raw"]
    rubric_json = state["rubric"].model_dump_json() if state.get("rubric") else "{}"
    resume_raw = state.get("resume_raw", "")
    
    print(f"[DEBUG] node_score_candidate: resume_raw={len(resume_raw)} chars, resume_parsed={'yes' if state.get('resume_parsed') else 'no'}")
    
    score = score_candidate(jd_json, resume_json, rubric_json, llm_call, resume_raw=resume_raw)
    
    # Evidence rule enforcement: zero out criteria with empty evidence
    evidence_fixed = False
    for c in score.criteria:
        if not c.evidence or c.evidence.strip() == "":
            c.score = 0
            c.evidence = "[NO EVIDENCE - SCORE ZEROED]"
            evidence_fixed = True
    
    if evidence_fixed:
        total = 0.0
        total_w = 0
        for c in score.criteria:
            total += (c.score / 5.0) * c.weight
            total_w += c.weight
        score.total_score = total / max(total_w, 1)
    
    # Log injection handling in trajectory
    inj_count = getattr(state.get("resume_parsed"), "_injection_count", 0)
    if inj_count > 0:
        injection_log.append(f"injection handled: {inj_count} pattern(s) removed during scoring")
        trajectory.append(_make_traj_entry(
            thought="Injection detected in resume - scoring unaffected",
            tool_used="score_candidate",
            arguments={"injection_count": inj_count},
            observation="injection handled - scoring based on sanitized data only",
            state_changes={},
            decision="INJECTION_HANDLED"
        ))
    
    trajectory.append(_make_traj_entry(
        thought="Evaluate candidate against JD requirements and rubric",
        tool_used="score_candidate",
        arguments={"jd": "parsed", "resume": "parsed", "rubric": f"{len(state.get('rubric',{}).criteria or [])} criteria"},
        observation=f"Scored {score.candidate}: {score.total_score:.2f}",
        state_changes={
            "score_card": {"from": None, "to": f"score={score.total_score:.2f}"}
        },
        decision=f"SCORE={score.total_score:.2f}"
    ))
    
    return {**state, "score_card": score, "trajectory": trajectory, "step_count": step, "injection_log": injection_log}


def node_make_decision(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Make final decision on candidate."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    score_json = state["score_card"].model_dump_json() if state.get("score_card") else "{}"
    prompt = DECISION_PROMPT.format(score_card=score_json)
    response = llm_call(prompt)
    
    try:
        data = json.loads(response)
        decision = FinalDecision(**data)
        trajectory.append(_make_traj_entry(
            thought="Evaluate scorecard to determine candidate disposition",
            tool_used="make_decision",
            arguments={"scorecard": f"score={state['score_card'].total_score:.2f}"},
            observation=f"Decision for {decision.candidate_name}: {decision.decision}",
            state_changes={
                "decision": {"from": None, "to": f"{decision.decision}: {decision.reason[:50]}..."}
            },
            decision=decision.decision
        ))
        return {**state, "decision": decision, "trajectory": trajectory, "step_count": step}
    except (json.JSONDecodeError, Exception) as e:
        trajectory.append(_make_traj_entry(
            thought="Decision needed",
            tool_used="make_decision",
            arguments={},
            observation=f"Decision failed: {str(e)}",
            state_changes={},
            decision="ERROR"
        ))
        return {**state, "trajectory": trajectory, "error": f"Decision error: {str(e)}", "step_count": step}


def node_check_availability(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Check interviewer availability."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    slots = get_availability()
    trajectory.append(_make_traj_entry(
        thought="Selected candidate needs interview slot. Check interviewer availability.",
        tool_used="check_availability",
        arguments={},
        observation="Checked interviewer availability",
        state_changes={
            "available_slots": {"from": "not_checked", "to": "available"}
        },
        decision="AVAILABLE"
    ))
    
    return {**state, "available_slots": slots, "trajectory": trajectory, "step_count": step}


def node_schedule_interview(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Schedule interview after human approval gate (interrupt_before enforces gate)."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    # Human approval gate check (interrupt_before pauses before this node)
    human_status = state.get("human_approval_status", "pending")
    if human_status != "approved":
        trajectory.append(_make_traj_entry(
            thought="Human approval required before scheduling",
            tool_used="schedule_interview",
            arguments={"candidate": state["candidate_name"], "human_status": human_status},
            observation=f"Human approval status: {human_status} - scheduling blocked",
            state_changes={},
            decision="BLOCKED_PENDING_APPROVAL"
        ))
        return {**state, "trajectory": trajectory, "step_count": step}
    
    slot = schedule_interview_tool(
        state["candidate_name"],
        state.get("available_slots", "{}"),
        llm_call
    )
    trajectory.append(_make_traj_entry(
        thought="Human approved. Schedule interview for selected candidate.",
        tool_used="schedule_interview",
        arguments={"candidate": state["candidate_name"], "slot": f"{slot.date} {slot.time}"},
        observation=f"Interview scheduled for {slot.candidate_name}: {slot.date} {slot.time}",
        state_changes={
            "interview_slot": {"from": None, "to": f"{slot.date} {slot.time}"}
        },
        decision="SCHEDULED"
    ))
    
    return {**state, "interview_slot": slot, "trajectory": trajectory, "step_count": step}


def node_guardrail_check(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Perform guardrail check on the decision."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    decision_json = state["decision"].model_dump_json() if state.get("decision") else "{}"
    prompt = GUARDRAIL_PROMPT.format(decision=decision_json)
    response = llm_call(prompt)
    
    try:
        data = json.loads(response)
        is_safe = data.get("is_safe", True)
        reason = data.get("reason", "OK")
        trajectory.append(_make_traj_entry(
            thought="Verify decision is safe, fair, and compliant",
            tool_used="guardrail_check",
            arguments={"decision": state["decision"].decision if state.get("decision") else "unknown"},
            observation=f"Guardrail {'passed' if is_safe else 'WARNING'}: {reason}",
            state_changes={},
            decision="PASSED" if is_safe else "FLAGGED"
        ))
        return {**state, "trajectory": trajectory, "step_count": step}
    except (json.JSONDecodeError, Exception) as e:
        trajectory.append(_make_traj_entry(
            thought="Guardrail check needed",
            tool_used="guardrail_check",
            arguments={},
            observation=f"Guardrail check failed: {str(e)}",
            state_changes={},
            decision="ERROR"
        ))
        return {**state, "trajectory": trajectory, "step_count": step}


def node_generate_rubric(state: RecruitmentState, llm_call: Callable) -> RecruitmentState:
    """Generate an objective hiring rubric from the JD."""
    trajectory = list(state.get("trajectory", []))
    step = _inc_step(state)
    
    jd_parsed_json = state["jd_parsed"].model_dump_json() if state.get("jd_parsed") else "{}"
    prompt = RUBRIC_PROMPT.format(jd_parsed=jd_parsed_json, jd_raw=state["jd_raw"])
    response = llm_call(prompt)
    
    try:
        data = json.loads(response)
        criteria_list = []
        total_w = 0
        for c in data.get("criteria", []):
            criterion = RubricCriterion(**c)
            criteria_list.append(criterion)
            total_w += criterion.weight
        rubric = HiringRubric(criteria=criteria_list, total_weight=total_w)
        trajectory.append(_make_traj_entry(
            thought="Generate objective scoring criteria from JD requirements",
            tool_used="generate_rubric",
            arguments={"jd": state["jd_parsed"].job_title},
            observation=f"Generated rubric: {len(criteria_list)} criteria (total weight: {total_w})",
            state_changes={
                "rubric": {"from": None, "to": f"{len(criteria_list)} criteria, weight={total_w}"}
            },
            decision="RUBRIC_READY"
        ))
        return {**state, "rubric": rubric, "trajectory": trajectory, "step_count": step}
    except (json.JSONDecodeError, Exception) as e:
        trajectory.append(_make_traj_entry(
            thought="Rubric generation needed for objective scoring",
            tool_used="generate_rubric",
            arguments={},
            observation=f"Rubric generation failed: {str(e)}",
            state_changes={},
            decision="ERROR"
        ))
        return {**state, "trajectory": trajectory, "error": f"Rubric error: {str(e)}", "step_count": step}


def should_schedule(state: RecruitmentState) -> str:
    """Conditional edge: schedule only if shortlisted."""
    if state.get("decision") and state["decision"].decision == "SHORTLIST":
        return "schedule"
    return "skip"
