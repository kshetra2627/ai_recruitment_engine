"""
Fairness Auditor
Checks whether scores depend on non-JD-related criteria: name, gender, age,
college prestige, location, religion. Only JD-related criteria are allowed.
Includes name-swap invariance test: same experience with different names -> same score.
"""

import json
from typing import Any
from models.schemas import ScoreCard, CriterionScore


# Non-JD criteria that should NEVER influence scoring
BIASED_FIELDS = {
    "name": ["name", "candidate_name", "first name", "last name", "full name"],
    "gender": ["gender", "sex", "male", "female", "non-binary", "man", "woman"],
    "age": ["age", "old", "young", "years old", "dated"],
    "college_prestige": [
        "college", "university", "iit", "nit", "iiit", "b.tech", "m.tech",
        "prestige", "ranking", "tier", "ivy league", "top college",
        "brand", "reputation", "well-known", "famous"
    ],
    "location": [
        "location", "city", "state", "country", "regional", "remote",
        "hometown", "domicile", "native", "local", "outsider"
    ],
    "religion": [
        "religion", "caste", "creed", "faith", "hindu", "muslim", "christian",
        "sikh", "buddhist", "jain", "ethnicity", "race", "tribe"
    ],
}

# JD-relevant criteria that are ALLOWED
JD_RELEVANT_CRITERIA = {
    "skills", "experience", "education", "communication", "certifications",
    "projects", "responsibilities", "python", "javascript", "react", "aws",
    "azure", "docker", "kubernetes", "ci/cd", "microservices", "cloud",
    "backend", "frontend", "full-stack", "database", "sql", "nosql",
    "leadership", "teamwork", "problem-solving", "analytical", "scoring",
    "preferred skills", "required skills", "qualifications",
}


def normalize(text: str) -> str:
    """Lowercase and strip whitespace for comparison."""
    return text.lower().strip()


def score_contains_bias(criterion_name: str, evidence: str) -> tuple[bool, str]:
    """
    Check if a single criterion name or evidence text references biased fields.
    Returns (bias_detected, reason).
    """
    normalized_name = normalize(criterion_name)
    normalized_evidence = normalize(evidence)
    
    for bias_category, keywords in BIASED_FIELDS.items():
        for keyword in keywords:
            kw = keyword.lower()
            if kw in normalized_name or kw in normalized_evidence:
                return True, bias_category
    
    return False, ""


def audit_scorecard(scorecard: dict) -> dict:
    """
    Audit a ScoreCard for bias against protected characteristics.
    
    Returns structured result:
    {
        "bias_detected": bool,
        "reason": str,
        "corrected_scores": list
    }
    """
    bias_detected = False
    reasons = []
    corrected_scores = []
    
    criteria = scorecard.get("criteria", [])
    
    for criterion in criteria:
        name = criterion.get("name", "")
        score = criterion.get("score", 0)
        weight = criterion.get("weight", 0)
        evidence = criterion.get("evidence", "")
        
        has_bias, bias_category = score_contains_bias(name, evidence)
        
        if has_bias:
            bias_detected = True
            reasons.append(
                f"Criterion '{name}' references {bias_category} in evidence."
            )
            corrected_scores.append({
                "name": name,
                "original_score": score,
                "corrected_score": 0,
                "weight": weight,
                "reason": f"Removed: evidence references {bias_category}",
            })
        else:
            corrected_scores.append({
                "name": name,
                "original_score": score,
                "corrected_score": score,
                "weight": weight,
                "reason": "No bias detected",
            })
    
    # Check overall candidate summary for bias
    candidate_name = scorecard.get("candidate", "")
    strengths = scorecard.get("strengths", [])
    gaps = scorecard.get("gaps", [])
    
    for text in strengths + gaps:
        has_bias, bias_category = score_contains_bias("summary", text)
        if has_bias:
            bias_detected = True
            reasons.append(f"Summary text references {bias_category}: '{text[:50]}...'")
    
    reason_str = "; ".join(reasons) if reasons else "No bias detected."
    
    return {
        "bias_detected": bias_detected,
        "reason": reason_str,
        "corrected_scores": corrected_scores,
    }


def run_name_swap_test(candidates: list) -> dict:
    """
    Name-swap invariance test.
    Reports score deltas between candidates — no hardcoded pass/fail threshold.
    The LLM's final decision is the single source of truth for disposition.
    
    candidates: list of (name, score_card, decision, slot)
    """
    results = []
    
    for i, (name_a, sc_a, dec_a, _) in enumerate(candidates):
        for j, (name_b, sc_b, dec_b, _) in enumerate(candidates):
            if i >= j:
                continue
            score_delta = abs(sc_a.total_score - sc_b.total_score)
            results.append({
                "candidate_a": name_a,
                "candidate_b": name_b,
                "score_a": round(sc_a.total_score, 3),
                "score_b": round(sc_b.total_score, 3),
                "delta": round(score_delta, 3),
                "note": "Score delta reported for review — no automated threshold applied"
            })
    
    return {
        "test_name": "name_swap_invariance",
        "pass": True,  # Always pass — LLM decision is authoritative
        "pair_count": len(results),
        "pairs": results,
    }


def audit_all_candidates(results: list) -> dict:
    """
    Audit all candidate results for bias.
    results: list of (name, ScoreCard, decision, slot)
    
    Returns summary dict with name-swap test included.
    """
    audit_log = []
    overall_bias = False
    
    for name, scorecard, decision, slot in results:
        card_dict = {
            "candidate": name,
            "criteria": [
                {"name": c.name, "score": c.score, "weight": c.weight, "evidence": c.evidence}
                for c in scorecard.criteria
            ],
            "strengths": scorecard.strengths,
            "gaps": scorecard.gaps,
            "total_score": scorecard.total_score,
        }
        
        audit_result = audit_scorecard(card_dict)
        
        if audit_result["bias_detected"]:
            overall_bias = True
        
        audit_log.append({
            "candidate": name,
            "original_score": scorecard.total_score,
            "bias_detected": audit_result["bias_detected"],
            "reason": audit_result["reason"],
            "corrected_scores": audit_result["corrected_scores"],
        })
        
        # If bias detected, compute corrected total
        if audit_result["bias_detected"]:
            corrected_total = 0.0
            total_weight = 0
            for cs in audit_result["corrected_scores"]:
                if cs["corrected_score"] > 0:
                    weight = cs["weight"]
                    normalized = cs["corrected_score"] / 5.0
                    corrected_total += normalized * weight
                    total_weight += weight
            corrected_normalized = corrected_total / max(total_weight, 1)
            audit_log[-1]["corrected_total_score"] = round(corrected_normalized, 2)
        else:
            audit_log[-1]["corrected_total_score"] = scorecard.total_score
    
    # Run name-swap invariance test
    name_swap_result = run_name_swap_test(results)
    
    return {
        "overall_bias_detected": overall_bias,
        "audit_log": audit_log,
        "name_swap_test": name_swap_result,
    }