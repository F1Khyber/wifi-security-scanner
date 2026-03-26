import subprocess
import re

def get_password(ssid):
    try:
        result = subprocess.check_output(
            f'netsh wlan show profile "{ssid}" key=clear',
            shell=True
        ).decode(errors="ignore")

        for line in result.split("\n"):
            if "Key Content" in line:
                return line.split(":")[1].strip()
    except:
        return None


def check_password_strength(password):
    if not password:
        return "Unknown"

    score = 0

    if len(password) >= 8:
        score += 2
    if len(password) >= 12:
        score += 2
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*]", password):
        score += 2

    if score >= 7:
        return "Strong"
    elif score >= 4:
        return "Moderate"
    else:
        return "Weak"