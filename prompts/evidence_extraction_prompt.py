# Evidence Extraction Prompt
# 从对话中萃取行为信号的 Prompt

EVIDENCE_EXTRACTION_PROMPT = """You are an evaluation signal extraction engine. 

Analyze the following conversation between an employee and a companion AI.

Your task: Identify whether the employee demonstrated behavior related to one of these dimensions:
- CONTEXT_JUDGMENT
- EXCEPTION_HANDLING  
- RISK_ANTICIPATION
- COLLABORATION

If relevant behavior exists, extract:
1. dimension (one of the four)
2. inferred_skill (short phrase, max 10 words)
3. supporting_quote (exact quote from employee)
4. confidence (0.0 to 1.0)

If no clear signal exists, return null.

Output strictly in JSON format:
{{
  "dimension": "...",
  "inferred_skill": "...",
  "supporting_quote": "...",
  "confidence": 0.0
}}

Conversation:
{conversation}

Output only JSON, no other text:"""
