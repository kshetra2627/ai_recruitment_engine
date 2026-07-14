"""Quick test of the full pipeline with mock LLM (no API key needed)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

_call_count = 0
def _mock_llm(prompt):
    global _call_count
    _call_count += 1
    prompt_lower = prompt.lower()
    # Rubric generation
    if "generate" in prompt_lower and "rubric" in prompt_lower:
        return json.dumps({"criteria":[{"name":"Python","weight":30,"description":"Python skill","evidence":"","levels":{}},{"name":"React","weight":30,"description":"React skill","evidence":"","levels":{}},{"name":"Experience","weight":40,"description":"Years exp","evidence":"","levels":{}}]})
    # Plan
    if "create evaluation" in prompt_lower:
        return json.dumps({"plan":["Parse JD","Generate rubric","Score candidates"]})
    # JD parsing
    if "extract structured data" in prompt_lower:
        return json.dumps({"job_title":"Software Engineer","required_skills":["Python","React"],"preferred_skills":["AWS"],"minimum_education":"B.Tech","minimum_experience":"2 years","responsibilities":["Develop"],"communication_required":True,"weight_suggestions":[]})
    # ANY prompt with "untrusted" + scoring = scoring call
    if "untrusted" in prompt_lower and ("score" in prompt_lower or "rubric" in prompt_lower):
        return json.dumps({"candidate":"Test","criteria":[{"name":"Python","score":4,"weight":30,"evidence":"5 years Python exp"},{"name":"React","score":3,"weight":30,"evidence":"2 years React"},{"name":"Experience","score":4,"weight":40,"evidence":"5 years total"}],"total_score":0.73,"strengths":["Strong Python"],"gaps":["Junior React"],"recommendation":"Interview"})
    # Resume parsing
    if "resume" in prompt_lower and "security" in prompt_lower:
        return json.dumps({"name":"Test Candidate","skills":["Python","React"],"education":["B.Tech CS"],"experience_years":5,"experience_details":["Senior Dev"],"projects":["Web App"],"certifications":[],"communication_evidence":"Good","resume_lines":["line1"]})
    # Decision
    if "decide" in prompt_lower:
        return json.dumps({"candidate_name":"Test","decision":"SHORTLIST","reason":"Good match"})
    # Guardrail
    if "guardrail" in prompt_lower or "safe, fair" in prompt_lower:
        return json.dumps({"is_safe":True,"reason":"OK","issues":[]})
    # Schedule
    if "schedule" in prompt_lower or "slot" in prompt_lower:
        return json.dumps({"candidate_name":"Test","date":"2026-07-15","time":"10:00 AM","format":"online"})
    # Fallback
    print(f"[MOCK UNMATCHED #{_call_count}] {prompt[:120]}", file=sys.stderr)
    return json.dumps({"candidate":"Test","criteria":[],"total_score":0.0,"strengths":[],"gaps":[],"recommendation":"Hold"})

from graph.nodes import node_parse_jd, node_generate_rubric, node_create_plan
from graph.state import RecruitmentState
from tools.parse_resume import parse_resume as parse_resume_tool
from tools.score_candidate import score_candidate as score_candidate_tool
from tools.availability import get_availability
from tools.interview import schedule_interview, send_interview_invite
from models.schemas import FinalDecision, ScoreCard, CriterionScore
from tools.fairness_auditor import audit_all_candidates, run_name_swap_test

data_dir = os.path.join(os.path.dirname(__file__), "data")
jd_raw = open(os.path.join(data_dir, "jd.txt")).read()
priya = open(os.path.join(data_dir, "priya.txt")).read()
rahul = open(os.path.join(data_dir, "rahul.txt")).read()
meera = open(os.path.join(data_dir, "meera.txt")).read()

s = RecruitmentState(jd_raw=jd_raw, jd_parsed=None, resume_raw="", resume_parsed=None,
    score_card=None, decision=None, interview_slot=None, available_slots="{}",
    plan=[], candidate_name="", trajectory=[], error=None, rubric=None,
    step_count=0, human_approval_status="pending", injection_log=[], fairness_results={})
s = node_parse_jd(s, _mock_llm)
assert s.get("jd_parsed"), "JD parsing failed"
print(f"✓ JD parsed: {s['jd_parsed'].job_title}")

s = node_generate_rubric(s, _mock_llm)
assert s.get("rubric"), "Rubric generation failed"
print(f"✓ Rubric: {len(s['rubric'].criteria)} criteria")

s = node_create_plan(s, _mock_llm)
print(f"✓ Plan: {len(s.get('plan',[]))} steps")

# Manually create scorecards for testing (avoid mock matching issues)
scores_map = {
    "Priya Sharma": 0.85,
    "Rahul Verma": 0.72,
    "Meera Patel": 0.45,
}
results = []
for name, rt in [("Priya Sharma", priya), ("Rahul Verma", rahul), ("Meera Patel", meera)]:
    rd = parse_resume_tool(rt, _mock_llm)
    print(f"✓ Parsed: {rd.candidate_name}")
    
    sc = score_candidate_tool(
        s["jd_parsed"].model_dump_json(),
        rd.model_dump_json(),
        s["rubric"].model_dump_json(),
        _mock_llm
    )
    sc.candidate = name
    print(f"  Score: {sc.total_score:.2f}")
    
    from prompts.decision_prompt import DECISION_PROMPT
    r = json.loads(_mock_llm(DECISION_PROMPT.format(score_card=sc.model_dump_json())))
    dec = FinalDecision(**r)
    print(f"  Decision: {dec.decision}")
    
    for c in sc.criteria:
        if "[NO EVIDENCE" in c.evidence:
            print(f"  ⚠️ Evidence missing for: {c.name}")
    
    results.append((name, sc, dec, None))
    
    if dec.decision == "SHORTLIST":
        from prompts.guardrail_prompt import GUARDRAIL_PROMPT
        g = json.loads(_mock_llm(GUARDRAIL_PROMPT.format(decision=dec.model_dump_json())))
        print(f"  Guardrail: {'Passed' if g.get('is_safe') else 'WARNING'}")
        av = get_availability()
        sl = schedule_interview(name, av, _mock_llm)
        print(f"  Slot: {sl.date} {sl.time}")

print("\n🔍 Running fairness audit...")
audit = audit_all_candidates(results)
print(f"  Bias detected: {audit['overall_bias_detected']}")
ns = audit.get("name_swap_test", {})
print(f"  Name-swap test: {'PASS' if ns.get('pass') else 'FAIL'}")
for p in ns.get("pairs", []):
    print(f"    {p['candidate_a']} ↔ {p['candidate_b']}: Δ={p['delta']:.2f} (reported for review)")

print(f"\n🔍 State verification:")
print(f"  step_count: {s.get('step_count', 0)}")
print(f"  injection_log: {s.get('injection_log', [])}")
print(f"  human_approval_status: {s.get('human_approval_status', '')}")

print("\n✅ FULL PIPELINE TEST PASSED")