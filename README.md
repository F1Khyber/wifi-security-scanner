# ⚡ WiFi Security Scanner

A Python-based defensive WiFi security monitoring tool.

## Features

- WiFi network discovery
- SSID detection
- BSSID detection
- Channel detection
- Signal strength
- Authentication detection
- Encryption analysis
- Risk classification
- Evil Twin anomaly detection
- ARP anomaly detection
- Latency monitoring
- Packet loss monitoring
- Flask web dashboard

## Tech Stack

- Python
- Flask
- Scapy
- psutil
- pywifi
- HTML
- CSS
- JavaScript


## PROJECT SUMMARY


we have built a Python + Flask defensive WiFi security monitoring system.

What I have done:

WiFi Scanning
Detect nearby WiFi networks.
Collect SSID, BSSID, channel, signal and authentication/encryption information.
Security Analysis
Analyze WiFi encryption/security.
Analyze signal strength.
Generate a risk score and risk level: GREEN, YELLOW, RED.
Evil Twin Detection
Compare known SSIDs with their known BSSIDs.
Detect unexpected BSSIDs.
Higher suspicion when the security configuration also changes.
ARP Anomaly Detection
Use Scapy to inspect ARP traffic.
Detect suspicious ARP address/MAC relationships that may indicate ARP spoofing.
AI Embeddings

Convert security events such as:

"Unknown BSSID detected"

into embedding vectors.

This allows security events to be compared based on semantic similarity.
MongoDB
Store WiFi security events.
Store event information, alerts and embeddings.
Vector Search
Search MongoDB for security events similar to the current event.
This provides the foundation for historical anomaly analysis.
Flask Dashboard
Display scanned networks.
Show network count.
Show HIGH/MEDIUM/LOW risk statistics.
Display SSID, BSSID, security, signal, channel and risk.
Current architecture
WiFi Scanner
     ↓
Security Analysis
     ↓
Evil Twin + ARP Detection
     ↓
Risk Engine
     ↓
Security Event
     ↓
Embedding Model
     ↓
MongoDB + Vector Search
     ↓
Flask API
     ↓
Web Dashboard
What comes next

The main remaining work is to fully connect Evil Twin + ARP detection into the API/risk engine, then add RAG so the system can retrieve similar historical/security knowledge and provide an explanation for why a network is considered suspicious.

## Installation

Clone the repository:

```bash
