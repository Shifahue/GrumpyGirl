import uuid

# Simple deterministic stub for Claude-like decomposition/coaching.
# Returns a list of subtasks for a given goal text.

def decompose_goal(goal_text: str):
    # For now, split by sentences or commas and return numbered subtasks.
    parts = [p.strip() for p in goal_text.replace(';', ',').split(',') if p.strip()]
    if not parts:
        parts = [goal_text]
    subtasks = []
    for i, p in enumerate(parts, start=1):
        subtasks.append({
            "id": str(uuid.uuid4()),
            "title": f"{i}. {p[:80]}",
            "notes": "(auto-decomposed)",
        })
    return {
        "goal": goal_text,
        "subtasks": subtasks
    }
