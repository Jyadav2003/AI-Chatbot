from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

co = cohere.Client(os.getenv("COHERE_API_KEY"))

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    try:
        response = co.generate(
            model="command",
            prompt=f"You are Beru, a helpful and intelligent assistant.\nUser: {prompt}\nBeru:",
            max_tokens=100
        )
        reply = response.generations[0].text.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
