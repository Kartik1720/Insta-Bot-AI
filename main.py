from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Deployment Successful! 🚀"

if __name__ == "__main__":
    print("Starting Flask Server...")  # Debugging log
    app.run(host="0.0.0.0", port=8080)
