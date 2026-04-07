def grade(memory, ticket):
    score = 0.0

    if memory.get("priority") == ticket.expected_priority:
        score += 0.3

    if memory.get("team") == ticket.expected_team:
        score += 0.3

    if memory.get("resolved"):
        score += 0.4

    return max(0.1, min(score, 0.9))   # ✅ IMPORTANT