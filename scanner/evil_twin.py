"""
Evil Twin anomaly detection.

This module compares currently observed WiFi networks
against previously trusted network information.

Important:
An unknown BSSID does NOT automatically mean an Evil Twin.
Legitimate routers, mesh systems, and access points can
share the same SSID.
"""

from typing import Any


def detect_evil_twin(
    networks: list[dict[str, Any]],
    known_networks: dict[str, dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    """
    Detect suspicious changes in previously known WiFi networks.

    Parameters
    ----------
    networks:
        Currently scanned WiFi networks.

    known_networks:
        Previously trusted network information.

    Returns
    -------
    list:
        List of detected WiFi anomalies.
    """

    if known_networks is None:
        known_networks = {}

    alerts = []

    for network in networks:

        ssid = network.get("ssid")
        bssid = network.get("bssid")
        authentication = network.get("authentication")

        # Ignore networks without an SSID
        if not ssid:
            continue

        # Look for this SSID in our trusted network database
        known = known_networks.get(ssid)

        # If we have never seen this SSID,
        # we don't classify it as an Evil Twin.
        if not known:
            continue

        known_bssids = known.get("bssids", [])
        known_authentication = known.get("authentication")

        # -------------------------------------------------
        # Unknown BSSID
        # -------------------------------------------------

        if bssid not in known_bssids:

            # Unknown BSSID + different security
            # configuration = higher suspicion
            if (
                known_authentication
                and authentication != known_authentication
            ):

                alerts.append({
                    "ssid": ssid,
                    "bssid": bssid,
                    "severity": "HIGH",
                    "reason": (
                        "Known SSID appeared with an "
                        "unexpected BSSID and security "
                        "configuration."
                    )
                })

            # Unknown BSSID but same security
            else:

                alerts.append({
                    "ssid": ssid,
                    "bssid": bssid,
                    "severity": "MEDIUM",
                    "reason": (
                        "Known SSID appeared with an "
                        "unknown BSSID."
                    )
                })

    return alerts