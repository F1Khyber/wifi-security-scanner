import subprocess

def scan_wifi():
    result = subprocess.check_output(
        "netsh wlan show networks mode=bssid",
        shell=True
    ).decode(errors="ignore")

    networks = []
    current = {}

    for line in result.split("\n"):
        line = line.strip()

        if line.startswith("SSID"):
            if current:
                networks.append(current)
                current = {}
            current["ssid"] = line.split(":")[1].strip()

        elif "Authentication" in line:
            current["encryption"] = line.split(":")[1].strip()

        elif "Signal" in line:
            current["signal"] = line.split(":")[1].strip()

        elif "BSSID" in line:
            current["bssid"] = line.split(":")[1].strip()

    if current:
        networks.append(current)

    return networks