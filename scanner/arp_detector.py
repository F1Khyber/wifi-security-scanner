from scapy.all import ARP, sniff
from collections import defaultdict
from threading import Lock


# IP -> MAC mapping
ip_mac_table = {}

# Detected anomalies
arp_alerts = []

# Prevent concurrent modification
lock = Lock()


def process_arp_packet(packet):
    """
    Analyze a single ARP packet.

    Detects when the same IP address
    suddenly appears with a different MAC address.
    """

    if not packet.haslayer(ARP):
        return

    arp = packet[ARP]

    # We are mainly interested in ARP replies
    if arp.op != 2:
        return

    ip = arp.psrc
    mac = arp.hwsrc

    if not ip or not mac:
        return

    with lock:

        previous_mac = ip_mac_table.get(ip)

        # First time seeing this IP
        if previous_mac is None:

            ip_mac_table[ip] = mac

            return

        # Same mapping - normal
        if previous_mac.lower() == mac.lower():

            return

        # IP -> different MAC
        alert = {
            "type": "ARP_ANOMALY",
            "severity": "HIGH",
            "ip": ip,
            "previous_mac": previous_mac,
            "new_mac": mac,
            "reason": (
                f"IP {ip} changed from MAC "
                f"{previous_mac} to {mac}"
            )
        }

        arp_alerts.append(alert)

        # Update mapping
        ip_mac_table[ip] = mac


def start_arp_monitor(interface=None, timeout=10):
    """
    Start ARP monitoring.

    interface:
        Example: "Wi-Fi"

    timeout:
        Monitoring duration in seconds.
    """

    global arp_alerts

    with lock:
        arp_alerts = []

    sniff(
        filter="arp",
        prn=process_arp_packet,
        iface=interface,
        timeout=timeout,
        store=False
    )

    return get_arp_alerts()


def get_arp_alerts():

    with lock:
        return list(arp_alerts)


def get_arp_table():

    with lock:
        return dict(ip_mac_table)