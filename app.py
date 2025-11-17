from flask import Flask, render_template, request
import os
from flask import send_from_directory

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


@app.route("/gallery")
def gallery():
    files = os.listdir(UPLOAD_FOLDER)

    # Filter only images
    images = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    return render_template("gallery.html", images=images)


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/csvs")
def csv_gallery():
    files = os.listdir(UPLOAD_FOLDER)

    # Filter only CSV files
    csv_files = [f for f in files if f.lower().endswith(".csv")]

    return render_template("csv_gallery.html", csv_files=csv_files)



if __name__ == "__main__":
    app.run(debug=True)

