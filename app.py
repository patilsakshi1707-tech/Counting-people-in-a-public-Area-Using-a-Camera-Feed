from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from users import users
from crowd_count import run_crowd_count

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-key-change-this"
jwt = JWTManager(app)

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        token = create_access_token(identity=username)
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401

# --------- PROTECTED CROWD COUNT ---------
@app.route("/run", methods=["POST"])
@jwt_required()
def run():
    data = request.json
    input_video = data.get("input_video")
    output_video = data.get("output_video")

    result = run_crowd_count(input_video, output_video)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
