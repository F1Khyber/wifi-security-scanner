from flask import Blueprint, jsonify

from scanner.wifi_scanner import scan_wifi
from scanner.signal_monitor import analyze_signal

from scanner.evil_twin import detect_evil_twin
from scanner.arp_detector import start_arp_monitor

from security.encryption import analyze_encryption
from security.risk_engine import calculate_risk

from ai.event_formatter import format_security_event
from ai.embeddings import create_embedding

from ai.vector_search import (
    store_security_event,
    search_similar_events
)


network_bp = Blueprint(
    "network",
    __name__,
    url_prefix="/api"
)


@network_bp.get("/networks")
def get_networks():

    try:

        # -----------------------------------------
        # 1. Scan WiFi networks
        # -----------------------------------------

        scan_result = scan_wifi()

        if not scan_result["success"]:
            return jsonify(scan_result), 500


        analyzed_networks = []


        # -----------------------------------------
        # 2. Analyze each network
        # -----------------------------------------

        for network in scan_result["networks"]:

            # -------------------------------------
            # Encryption analysis
            # -------------------------------------

            encryption = analyze_encryption(
                network.get("authentication"),
                network.get("encryption")
            )


            # -------------------------------------
            # Signal analysis
            # -------------------------------------

            signal = analyze_signal(
                network.get("signal")
            )


            # -------------------------------------
            # Current findings
            # -------------------------------------

            findings = {

                "encryption_score":
                    encryption["score"],

                "signal_score":
                    signal["score"],

                # Will be integrated later
                "evil_twin_score": 0,

                "arp_score": 0
            }


            # -------------------------------------
            # Risk calculation
            # -------------------------------------

            risk = calculate_risk(
                findings
            )


            # -------------------------------------
            # Add risk to network
            # -------------------------------------

            network_with_risk = {

                **network,

                "risk": risk
            }


            # -------------------------------------
            # Security alerts
            # -------------------------------------

            alerts = []


            # -------------------------------------
            # Create security event text
            # -------------------------------------

            event_text = format_security_event(

                network_with_risk,

                alerts
            )


            # -------------------------------------
            # Create embedding
            # -------------------------------------

            embedding = create_embedding(
                event_text
            )


            # -------------------------------------
            # Store in MongoDB
            # -------------------------------------

            event_id = store_security_event(

                network=network_with_risk,

                event_text=event_text,

                embedding=embedding,

                alerts=alerts
            )


            # -------------------------------------
            # Search similar events
            # -------------------------------------

            similar_events = search_similar_events(

                query_embedding=embedding,

                limit=5
            )


            # -------------------------------------
            # Final network response
            # -------------------------------------

            analyzed_networks.append({

                **network,

                "security_analysis": {

                    "encryption":
                        encryption,

                    "signal":
                        signal,

                    "findings":
                        findings,

                    "risk":
                        risk
                },

                "ai_analysis": {

                    "event":
                        event_text,

                    "embedding_dimensions":
                        len(embedding),

                    "event_id":
                        event_id,

                    "similar_events":
                        similar_events
                }

            })


        # -----------------------------------------
        # 3. Return response
        # -----------------------------------------

        return jsonify({

            "success": True,

            "count":
                len(analyzed_networks),

            "networks":
                analyzed_networks

        })


    except Exception as error:

        print(
            "Network API error:",
            error
        )

        return jsonify({

            "success": False,

            "error":
                str(error)

        }), 500