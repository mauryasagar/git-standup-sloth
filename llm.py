import ollama

MODEL = "qwen2.5:1.5b"

SYSTEM_PROMPT = """You are a standup assistant. You receive a git log of commits.

Write in exactly this format:

Yesterday:
- <bullet per commit, past tense>

Today:
- <continuation of WIP/in-progress work only>

Blockers:
- None mentioned

Example of correct output:
Yesterday:
- Added a.txt file
- Fixed expired refresh token handling
- Refactored payment webhook retry logic

Today:
- Continue payment webhook retry refactor

Rules:
- EVERY commit belongs under Yesterday, in PAST TENSE (Fixed, Added, Refactored).
- Today: only from commits containing "WIP" or "in progress". Otherwise write "- Continue current work".
- Do NOT invent details, reasons, or file purposes.
- Bullets under 12 words.
"""

def generate_standup(git_log: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Git log:\n{git_log}"},
        ],
        options={"temperature": 0.2, "num_predict": 200},
    )
    return response["message"]["content"]