import subprocess

def scan_wifi():
    try:
        result = subprocess.check_output(
            "netsh wlan show networks mode=bssid",
            shell=True
        ).decode(errors="ignore")

        networks = []
        current = {}

        for line in result.split("\n"):
            line = line.strip()

            # New network
            if line.startswith("SSID"):
                if current:
                    networks.append(current)
                    current = {}

                parts = line.split(":", 1)
                if len(parts) > 1:
                    current["ssid"] = parts[1].strip()

            # Encryption
            elif "Authentication" in line:
                current["encryption"] = line.split(":", 1)[1].strip()

            # Signal
            elif "Signal" in line:
                signal = line.split(":", 1)[1].strip().replace("%", "")
                try:
                    current["signal"] = int(signal)
                except:
                    current["signal"] = 0

            # BSSID (important for duplicates / evil twin detection)
            elif "BSSID" in line:
                current["bssid"] = line.split(":", 1)[1].strip()

        # Append last network
        if current:
            networks.append(current)

        # 🔥 REMOVE EMPTY / DUPLICATE SSIDs
        unique_networks = []
        seen = set()

        for net in networks:
            ssid = net.get("ssid", "")
            if ssid and ssid not in seen:
                seen.add(ssid)
                unique_networks.append(net)

        return unique_networks

    except Exception as e:
        print("WiFi Scan Error:", e)
        return []