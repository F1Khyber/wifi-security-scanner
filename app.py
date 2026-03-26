from flask import Flask, render_template, jsonify

from scanner.wifi_scanner import scan_wifi
from scanner.password_checker import check_password_strength, get_password
from scanner.evil_twin import detect_evil
from scanner.risk_calculator import calculate_risk

app = Flask(__name__)


def process_networks():
    networks = []

    try:
        scanned_networks = scan_wifi()
    except Exception as e:
        print("Scan error:", e)
        scanned_networks = []

    # detect evil twins once
    evil_list = detect_evil(scanned_networks)

    for net in scanned_networks:
        ssid = net.get("ssid", "Unknown")
        encryption = net.get("encryption", "Unknown")
        signal = net.get("signal", 0)

        # ✅ FIXED PASSWORD LOGIC
        password = get_password(ssid)
        password_strength = check_password_strength(password)

        # evil twin check
        evil = ssid in evil_list

        # risk + score
        score, risk = calculate_risk(
            net,
            password_strength,
            evil
        )

        networks.append({
            "ssid": ssid,
            "encryption": encryption,
            "signal": signal,
            "password_strength": password_strength,
            "evil_twin": evil,
            "net_score": score,
            "risk": risk
        })

    return networks


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan")
def scan():
    return jsonify(process_networks())


if __name__ == "__main__":
    app.run(debug=True)