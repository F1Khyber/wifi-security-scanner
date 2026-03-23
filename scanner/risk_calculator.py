def calculate_risk(net, password_strength, evil):
    score = 0
    enc = net.get("encryption", "").lower()

    # Encryption score
    if "open" in enc:
        score += 0
    elif "wep" in enc:
        score += 20
    elif "wpa" in enc:
        score += 50
    elif "wpa2" in enc:
        score += 80
    elif "wpa3" in enc:
        score += 100

    # Password strength
    if password_strength == "Strong":
        score += 15
    elif password_strength == "Weak":
        score -= 10

    # Evil twin penalty
    if evil:
        score -= 40

    # Final result
    if score >= 80:
        return "Green"
    elif score >= 50:
        return "Yellow"
    else:
        return "Red"