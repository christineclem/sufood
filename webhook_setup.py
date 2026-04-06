import os

from flask import Flask, request

from routes.customers import customers_bp

app = Flask(__name__)
app.register_blueprint(customers_bp)

@app.route("/tally-webhook", methods=["GET", "POST"])
def tally_webhook():
    if request.method == "POST":
        print("JSON:", request.json)
    return "", 200

# Ensure that the host is "0.0.0.0" at PORT 5000
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )