import os

from flask import Flask, request

from database import init_db
from routes.customers import customers_bp

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False
app.register_blueprint(customers_bp)

@app.route("/")
def home():
    init_db()
    return "Database ready :)"

@app.route("/tally-webhook", methods=["GET", "POST"])
def tally_webhook():
    if request.method == "POST":
        print("JSON:", request.json)
        print("FORM:", request.form)
        print("DATA:", request.data)
    return "", 200

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )