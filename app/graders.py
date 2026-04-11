# app/graders.py

def normalize_score(score: float) -> float:
    # STRICT: always between (0,1)
    if score <= 0:
        return 0.2
    if score >= 1:
        return 0.8
    return score


def grade_easy(memory: dict, ticket) -> float:
    score = 0.1

    if memory.get("priority") == ticket.expected_priority:
        score += 0.3

    if memory.get("team") == ticket.expected_team:
        score += 0.3

    if memory.get("resolved"):
        score += 0.2

    return normalize_score(score)


def grade_medium(memory: dict, ticket) -> float:
    score = 0.1

    if memory.get("priority") == ticket.expected_priority:
        score += 0.3

    if memory.get("team") == ticket.expected_team:
        score += 0.3

    if memory.get("resolved"):
        score += 0.2

    return normalize_score(score)


def grade_hard(memory: dict, ticket) -> float:
    score = 0.1

    if memory.get("priority") == ticket.expected_priority:
        score += 0.25

    if memory.get("team") == ticket.expected_team:
        score += 0.25

    if memory.get("resolved"):
        score += 0.2

    if memory.get("priority") and memory.get("team"):
        score += 0.1

    return normalize_score(score)