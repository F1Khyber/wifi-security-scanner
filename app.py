from flask import Flask, render_template, jsonify
from scanner.wifi_scanner import scan_wifi
from scanner.password_checker import get_password, check_strength
from scanner.evil_twin import detect_evil
from scanner.risk_calculator import calculate_risk

app = Flask(__name__)

def process_networks():
    networks = scan_wifi()
    evil_list = detect_evil(networks)

    green = yellow = red = 0

    for net in networks:
        pwd = get_password(net["ssid"])
        strength = check_strength(pwd)

        net["password_strength"] = strength
        net["evil_twin"] = net["ssid"] in evil_list
        net["risk"] = calculate_risk(net, strength, net["evil_twin"])

        if net["risk"] == "Green":
            green += 1
        elif net["risk"] == "Yellow":
            yellow += 1
        else:
            red += 1

    return networks, green, yellow, red

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scan")
def scan():
    networks, green, yellow, red = process_networks()
    return jsonify({
        "networks": networks,
        "green": green,
        "yellow": yellow,
        "red": red
    })

if __name__ == "__main__":
    app.run(debug=True)