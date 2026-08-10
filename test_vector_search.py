from scanner.arp_detector import (
    start_arp_monitor,
    get_arp_table
)


print("Starting ARP monitor...")

alerts = start_arp_monitor(
    interface=None,
    timeout=20
)


print("\n==============================")
print("ARP TABLE")
print("==============================")

print(get_arp_table())


print("\n==============================")
print("ARP ALERTS")
print("==============================")


if not alerts:

    print("No ARP anomalies detected.")

else:

    for alert in alerts:

        print(alert)


print("\nARP monitoring finished.")