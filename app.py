from flask import Flask, request, jsonify, render_template
from model import get_class
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --------- CHECK ----------
@app.route("/check", methods=["POST"])
def check():

    if "image" not in request.files:
        return jsonify({"error": "Olvidaste subir la imagen :("}), 400

    image = request.files["image"]

    filename = f"{uuid.uuid4()}_{image.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    try:
        clase, confidence = get_class(
            model_path="keras_model.h5",
            labels_path="labels.txt",
            image_path=filepath
        )

        return render_template(
            "index.html",
            result=clase,
            confidence=round(confidence,2)
        )

    finally:
        os.remove(filepath)


# --------- HOME ----------
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    