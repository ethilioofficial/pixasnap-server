from flask import Flask, request, send_file, jsonify
from rembg import remove, new_session
import io
import os

app = Flask(__name__)

# ✅ lightweight model (memory safe)
session = new_session("u2netp")

@app.route("/")
def home():
    return "BG Remove Server Running"

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    try:
        input_bytes = file.read()

        # ✅ NO resize (size exactly same থাকবে)
        output_bytes = remove(input_bytes, session=session)

        return send_file(
            io.BytesIO(output_bytes),
            mimetype="image/png",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Render port binding
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
