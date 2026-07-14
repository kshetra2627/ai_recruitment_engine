SCHEDULE_PROMPT = """Propose interview slot. Return JSON:
{{"candidate_name":"","date":"","time":"","format":"online/offline"}}

Candidate: {candidate_name}
Slots: {slots}"""