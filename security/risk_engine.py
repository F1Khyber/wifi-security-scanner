def calculate_risk(findings):

    score = 0

    score += findings.get("encryption_score", 0)
    score += findings.get("evil_twin_score", 0)
    score += findings.get("arp_score", 0)
    score += findings.get("signal_score", 0)

    score = min(max(score, 0), 100)

    if score <= 25:
        level = "GREEN"

    elif score <= 60:
        level = "YELLOW"

    else:
        level = "RED"

    return {
        "score": score,
        "level": level
    }