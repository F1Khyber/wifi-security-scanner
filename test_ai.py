from scanner.evil_twin import detect_evil_twin
from ai.event_formatter import format_security_event
from ai.embeddings import create_embedding


networks = [
    {
        "ssid": "HomeWiFi",
        "bssid": "AA:BB:CC:DD:EE:FF",
        "authentication": "OPEN",
        "encryption": "NONE",
        "signal": 85,
        "channel": 6
    }
]


known_networks = {
    "HomeWiFi": {
        "bssids": [
            "11:22:33:44:55:66"
        ],
        "authentication": "WPA2-Personal"
    }
}


# 1. Detect anomaly
alerts = detect_evil_twin(
    networks,
    known_networks
)

print("ALERTS:")
print(alerts)


# 2. Convert event to text
event_text = format_security_event(
    networks[0],
    alerts
)

print("\nEVENT:")
print(event_text)


# 3. Generate embedding
vector = create_embedding(event_text)

print("\nEMBEDDING:")
print("Dimensions:", len(vector))
print("First 5 values:", vector[:5])