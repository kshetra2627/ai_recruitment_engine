import json
from tools.sanitizer import SafePromptWrapper
from prompts.scorer_prompt import SCORER_PROMPT
from models.schemas import ScoreCard, CriterionScore

def score_candidate(jd_json: str, resume_data_json: str, rubric_json: str, llm_call,
                    resume_raw: str = "") -> ScoreCard:
    """Score a candidate against JD requirements using rubric.
    
    SECURITY: Resume-derived data is UNTRUSTED. The scoring prompt is wrapped
    with injection protection to prevent resume text from influencing scores,
    changing weights, or overriding the rubric.
    
    EVIDENCE RULE: Every criterion must have specific resume evidence.
    If evidence is missing or empty, the criterion score is zeroed.
    """
    raw_prompt = SCORER_PROMPT.format(jd=jd_json, resume_data=resume_data_json,
                                      rubric=rubric_json, resume_raw=resume_raw)
    safe_prompt = SafePromptWrapper.wrap_scoring(raw_prompt)
    response = llm_call(safe_prompt)
    try:
        data = json.loads(response)
        criteria_list = []
        for c in data.get("criteria", []):
            # Enforce evidence rule: empty evidence -> score 0
            evidence = c.get("evidence", "").strip()
            if not evidence:
                c["score"] = 0
                c["evidence"] = "[NO EVIDENCE - SCORE ZEROED]"
            criteria_list.append(CriterionScore(**c))
        data["criteria"] = criteria_list
        # Recalculate total if evidence was missing
        if any(c.evidence == "[NO EVIDENCE - SCORE ZEROED]" for c in criteria_list):
            total = 0.0
            total_w = 0
            for c in criteria_list:
                total += (c.score / 5.0) * c.weight
                total_w += c.weight
            data["total_score"] = total / max(total_w, 1)
        return ScoreCard(**data)
    except (json.JSONDecodeError, Exception) as e:
        return ScoreCard(candidate="Unknown", recommendation="Hold")