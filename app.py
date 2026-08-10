from flask import Flask, render_template

from api.networks import network_bp
from config.database import test_connection


app = Flask(__name__)


# Register API routes
app.register_blueprint(network_bp)


# Dashboard
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":

    # Test MongoDB connection
    test_connection()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )