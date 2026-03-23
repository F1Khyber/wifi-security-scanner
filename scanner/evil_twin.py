def detect_evil(networks):
    ssid_map = {}

    for net in networks:
        ssid = net.get("ssid")
        bssid = net.get("bssid")

        if ssid not in ssid_map:
            ssid_map[ssid] = set()

        ssid_map[ssid].add(bssid)

    evil_list = []

    for ssid, bssids in ssid_map.items():
        if len(bssids) > 1:
            evil_list.append(ssid)

    return evil_list