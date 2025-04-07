from flask import Flask, request, render_template, jsonify
from ..authentification.enroll import Enrollment
from ..authentification.verify import Verifier
from ..feature_extraction.embeddings import EmbeddingGenerator

app = Flask(__name__)
enroller = Enrollment()
verifier = Verifier()

@app.route("/")
def home():
    # Render the enrollment/verification HTML form
    return render_template("index.html")

@app.route("/enroll", methods=["POST"])
def enroll():
    # Save uploaded image and enroll the user
    name = request.form.get("name")
    image = request.files["image"]
    image.save("temp.jpg")  # Temporary file for processing
    success = enroller.enroll_user(name, "temp.jpg")
    return jsonify({"success": success})

@app.route("/verify", methods=["POST"])
def verify():
    # Save uploaded image and verify the user
    image = request.files["image"]
    image.save("temp.jpg")
    embedding = EmbeddingGenerator().generate_embedding("temp.jpg")
    if embedding is None:
        return jsonify({"error": "No face detected"})
    user = verifier.verify_user(embedding)
    return jsonify({"user": user})

if __name__ == "__main__":
    app.run(debug=True)  # Run the Flask server