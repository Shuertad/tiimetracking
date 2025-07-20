from flask import Flask, request, jsonify
from utils.fetch import fetch_categories
from utils.embeddings import get_embedding, generate_category_embeddings
from utils.suggest import suggest_categories

app = Flask(__name__)

@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.json
    event_name = data.get("event_name")
    email = data.get("email")
    user_token = data.get("user_token")

    if not all([event_name, email, user_token]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        categories = generate_category_embeddings(email, user_token)
        suggestion = suggest_categories(event_name, categories)
        return jsonify(suggestion)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
