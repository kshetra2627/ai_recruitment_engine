HIRING_DECISION_PROMPT = """Evaluate candidate and decide. Return JSON:
{{"candidate_name":"","decision":"SELECT/REJECT/HOLD","reason":"","strengths":[],"gaps":[],"recommendation":""}}

Score: {score_card}
JD: {jd}"""