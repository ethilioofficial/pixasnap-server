from flask import Flask, request, jsonify, send_file
import io
from rembg import remove, new_session

app = Flask(__name__)

# 🔐 Dummy license store (replace with Firebase later)
VALID_KEYS = ["ABC123", "XYZ789"]

# 🤖 AI session
session = new_session("u2net_human_seg")

# -------------------------------
# 🔐 License Check
# -------------------------------
@app.route("/check-license", methods=["POST"])
def check_license():
    data = request.json
    key = data.get("key")

    if key in VALID_KEYS:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"}), 401


# -------------------------------
# 🎨 Background Removal
# -------------------------------
@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    file = request.files.get("image")
    key  = request.form.get("key")

    # 🔐 License verify
    if key not in VALID_KEYS:
        return jsonify({"error": "Invalid license"}), 403

    if not file:
        return jsonify({"error": "No image provided"}), 400

    input_bytes = file.read()

    # 🤖 AI process
    output = remove(input_bytes, session=session)

    return send_file(
        io.BytesIO(output),
        mimetype="image/png",
        as_attachment=False,
        download_name="output.png"
    )


# -------------------------------
# 🚀 Run server
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
