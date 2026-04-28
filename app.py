from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello from Azure Demo Web App</h1><p>DB connection will go here soon.</p>"

@app.route("/health")
def health():
    return {"status": "ok"}

