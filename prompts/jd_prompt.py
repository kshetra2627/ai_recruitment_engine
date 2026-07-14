JD_ANALYSIS_PROMPT = """Extract structured data from this job description. Return JSON:
{{"job_title":"","required_skills":[],"preferred_skills":[],"minimum_education":"","minimum_experience":"","responsibilities":[],"communication_required":false,"weight_suggestions":[]}}

JD: {jd}"""