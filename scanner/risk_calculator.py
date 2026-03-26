def calculate_risk(net, password_strength, evil):
    score = 0
    enc = net.get("encryption", "").lower()

    # 🔐 Encryption (50 max)
    if "open" in enc:
        score += 5
    elif "wep" in enc:
        score += 15
    elif "wpa" in enc and "wpa2" not in enc and "wpa3" not in enc:
        score += 25
    elif "wpa2" in enc:
        score += 40
    elif "wpa3" in enc:
        score += 50

    # 🔑 Password (20 max)
    if password_strength == "Strong":
        score += 20
    elif password_strength == "Moderate":
        score += 10
    elif password_strength == "Weak":
        score += 0

    # 📶 Signal (20 max)
    signal = net.get("signal", 0)
    try:
        signal = int(str(signal).replace('%',''))
    except:
        signal = 0

    score += int(signal * 0.2)

    # 👿 Evil Twin (-30 penalty)
    if evil:
        score -= 30

    # Clamp
    score = max(0, min(score, 100))

    # Label
    if score >= 75:
        risk = "Safe"
    elif score >= 50:
        risk = "Moderate"
    else:
        risk = "Risky"

    return score, risk