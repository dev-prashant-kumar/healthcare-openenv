def grade_hard(history: dict) -> float:
    total = history.get("total_patients", 1)
    treated = history.get("treated_patients", [])
    critical_saved = sum(1 for p in treated if p["severity"] >= 8)

    missed = history.get("missed_deadlines", 0)

    score = 0.0

    # prioritize critical patients
    score += (critical_saved / total) * 0.5

    # general efficiency
    score += (len(treated) / total) * 0.3

    # penalty
    score -= (missed / total) * 0.2

    return max(0.0, min(1.0, score))