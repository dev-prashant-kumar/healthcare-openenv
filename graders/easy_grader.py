def grade_easy(history: dict) -> float:
    treated = len(history.get("treated_patients", []))
    total = history.get("total_patients", 1)

    score = treated / total

    return max(0.0, min(1.0, score))