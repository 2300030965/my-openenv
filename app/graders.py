# app/graders.py

def normalize_score(score: float) -> float:
    if score <= 0:
        return 0.1
    if score >= 1:
        return 0.9
    return score


# 🔹 EASY
def grade_easy(memory: dict) -> float:
    score = 0.0

    if memory.get("priority"):
        score += 0.3

    if memory.get("team"):
        score += 0.3

    if memory.get("resolved"):
        score += 0.2

    return normalize_score(score)


# 🔹 MEDIUM
def grade_medium(memory: dict) -> float:
    score = 0.0

    if memory.get("priority"):
        score += 0.25

    if memory.get("team"):
        score += 0.25

    if memory.get("resolved"):
        score += 0.2

    # small bonus
    if memory.get("priority") and memory.get("team"):
        score += 0.1

    return normalize_score(score)


# 🔹 HARD
def grade_hard(memory: dict) -> float:
    score = 0.0

    if memory.get("priority"):
        score += 0.2

    if memory.get("team"):
        score += 0.2

    if memory.get("resolved"):
        score += 0.2

    if memory.get("priority") and memory.get("team"):
        score += 0.2

    return normalize_score(score)