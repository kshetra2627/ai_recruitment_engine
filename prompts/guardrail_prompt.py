GUARDRAIL_PROMPT = """Verify decision is safe, fair, compliant. Return JSON:
{{"is_safe":true,"reason":"","issues":[]}}

Decision: {decision}"""