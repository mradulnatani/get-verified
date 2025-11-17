from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    csv_file = request.files["csvFile"]
    image_file = request.files["imageFile"]

    csv_file.save(os.path.join(UPLOAD_FOLDER, csv_file.filename))
    image_file.save(os.path.join(UPLOAD_FOLDER, image_file.filename))

    return "Files saved successfully!"

if __name__ == "__main__":
    app.run(debug=True)

