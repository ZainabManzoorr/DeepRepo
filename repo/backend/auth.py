from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



db.init_db()

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    username = data["username"]
    password = generate_password_hash(data["password"])

    try:
        db.create_user(username, password)
        return jsonify({"message": "User created successfully"})
    except:
        return jsonify({"error": "User already exists"}), 400


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = db.get_user(data["username"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    if check_password_hash(user["password"], data["password"]):
        return jsonify({
            "message": "Login successful",
            "user": user["username"]
        })

    return jsonify({"error": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(debug=True)