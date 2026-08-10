def analyze_encryption(authentication, encryption=None):

    authentication = (
        authentication or ""
    ).upper()

    encryption = (
        encryption or ""
    ).upper()

    # Open network
    if (
        not authentication
        or authentication in ["OPEN", "NONE"]
    ):
        return {
            "type": "OPEN",
            "risk": "HIGH",
            "score": 50,
            "description": "Network does not use Wi-Fi authentication."
        }

    # WEP
    if "WEP" in authentication or "WEP" in encryption:
        return {
            "type": "WEP",
            "risk": "HIGH",
            "score": 40,
            "description": "WEP is considered insecure."
        }

    # WPA3
    if "WPA3" in authentication:
        return {
            "type": "WPA3",
            "risk": "LOW",
            "score": 0,
            "description": "WPA3 provides modern Wi-Fi security."
        }

    # WPA2
    if "WPA2" in authentication:
        return {
            "type": "WPA2",
            "risk": "LOW",
            "score": 5,
            "description": "WPA2 is commonly considered secure when configured correctly."
        }

    # Older WPA
    if "WPA" in authentication:
        return {
            "type": "WPA",
            "risk": "MEDIUM",
            "score": 20,
            "description": "Older WPA configuration detected."
        }

    return {
        "type": authentication,
        "risk": "UNKNOWN",
        "score": 20,
        "description": "Unknown authentication configuration."
    }