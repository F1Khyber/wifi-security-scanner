def format_security_event(network, alerts=None):

    alerts = alerts or []

    alert_text = []

    for alert in alerts:

        alert_text.append(
            f"{alert.get('severity')} severity: "
            f"{alert.get('reason')}"
        )

    return f"""
WiFi Security Event

SSID: {network.get('ssid')}
BSSID: {network.get('bssid')}
Authentication: {network.get('authentication')}
Encryption: {network.get('encryption')}
Signal: {network.get('signal')}
Channel: {network.get('channel')}

Detected anomalies:
{chr(10).join(alert_text)}

Risk: {network.get('risk', 'UNKNOWN')}
""".strip()