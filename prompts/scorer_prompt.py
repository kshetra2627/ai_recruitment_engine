SCORER_PROMPT = """Score candidate vs JD per rubric.
Each criterion MUST cite specific resume evidence. No evidence = 0.
Never use name, gender, age, college.

Return JSON:
{{"candidate":"","criteria":[{{"name":"","score":0,"weight":0,"evidence":""}}],"total_score":0,"strengths":[],"gaps":[],"recommendation":"Interview/Hold/Reject"}}

Parsed Resume Data: {resume_data}
Full Resume Text (for evidence extraction): {resume_raw}
JD: {jd}
Rubric: {rubric}"""
