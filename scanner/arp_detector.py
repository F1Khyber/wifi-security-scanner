from scapy.all import ARP, sniff
import threading

arp_table = {}

def detect_arp(packet):
    if packet.haslayer(ARP) and packet[ARP].op == 2:
        ip = packet[ARP].psrc
        mac = packet[ARP].hwsrc

        if ip in arp_table:
            if arp_table[ip] != mac:
                print(f"[ALERT] ARP Spoofing detected! IP: {ip}")
                return True
        else:
            arp_table[ip] = mac
    return False


def start_arp_monitor():
    sniff(filter="arp", prn=detect_arp, store=0)