PARSER_PROMPT = """Extract structured resume data. Return JSON:
{{"name":"","skills":[],"education":[],"experience_years":0,"experience_details":[],"projects":[],"certifications":[],"communication_evidence":"","resume_lines":[]}}

Resume: {resume_text}"""