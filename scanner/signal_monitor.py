def analyze_signal(signal):

    if signal is None:
        return {
            "score": 0,
            "quality": "UNKNOWN"
        }

    if signal >= 80:
        return {
            "score": 0,
            "quality": "EXCELLENT"
        }

    if signal >= 60:
        return {
            "score": 0,
            "quality": "GOOD"
        }

    if signal >= 40:
        return {
            "score": 5,
            "quality": "FAIR"
        }

    return {
        "score": 10,
        "quality": "WEAK"
    }