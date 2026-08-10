def analyze_password(password):

    if not password:
        return {
            "score": 0,
            "strength": "UNKNOWN"
        }

    score = 0

    length = len(password)

    if length >= 16:
        score += 4

    elif length >= 12:
        score += 3

    elif length >= 8:
        score += 2

    else:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(not char.isalnum() for char in password):
        score += 1

    if score <= 3:
        strength = "WEAK"

    elif score <= 5:
        strength = "MEDIUM"

    else:
        strength = "STRONG"

    return {
        "score": score,
        "strength": strength
    }