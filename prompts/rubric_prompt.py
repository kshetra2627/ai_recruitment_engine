RUBRIC_PROMPT = """Generate an objective hiring rubric from the JD. Return JSON:
{{"criteria":[{{"name":"","weight":0,"description":"","evidence":"","levels":{{}}}}]}}

JD parsed: {jd_parsed}
JD raw: {jd_raw}"""