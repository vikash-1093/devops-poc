from flask import Flask
app = Flask(__name__)

@app.route("/healthz")
def health():
    return {"status": "ok"}

@app.route("/")
def hello():
    return {"message": "Hello from DevOps POC"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

