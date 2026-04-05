def grade_medium(history: dict) -> float:
    treated = len(history.get("treated_patients", []))
    total = history.get("total_patients", 1)
    missed = history.get("missed_deadlines", 0)

    score = 0.0
    score += (treated / total) * 0.6
    score -= (missed / total) * 0.4

    return max(0.0, min(1.0, score))