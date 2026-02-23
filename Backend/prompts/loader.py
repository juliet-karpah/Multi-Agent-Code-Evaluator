from pathlib import Path

PROMPT_ROOT = Path(__file__).parent

def load_prompt(category, version, role):
    """
    category: judge or solver
    version: v1..vn
    role: system or user
    """
    path = PROMPT_ROOT / category / version / f"{role}.txt"
    return path.read_text()