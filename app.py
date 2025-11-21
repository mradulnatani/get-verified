import os,json
from flask import send_from_directory
import pandas as pd
import smtplib
from email.message import EmailMessage
from PIL import Image, ImageDraw, ImageFont
import time
import csv
from flask import current_app
from flask import send_from_directory
from flask import Flask, render_template, request, send_from_directory, redirect, url_for,jsonify


app = Flask(__name__)



UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


TEMPLATE_FOLDER = "templates_data"
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)
GENERATED_FOLDER = "generated"
os.makedirs(GENERATED_FOLDER, exist_ok=True)
TEMPLATE_JSON_FOLDER = "templates_json"
os.makedirs(TEMPLATE_JSON_FOLDER, exist_ok=True)
UPLOAD_FOLDER = "uploads"

app.config["GENERATED_FOLDER"] = GENERATED_FOLDER

UPLOAD_DIR = "uploads"
TEMPLATE_DIR = "templates_json"
PREVIEW_DIR = "previews"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

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



@app.route("/select-image")
def select_image():
    files = os.listdir(UPLOAD_FOLDER)
    images = [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    return render_template("select_image.html", images=images)



@app.route("/select-csv")
def select_csv():
    image = request.args.get("image")
    files = os.listdir(UPLOAD_FOLDER)
    csv_files = [f for f in files if f.lower().endswith(".csv")]
    return render_template("select_csv.html", image=image, csv_files=csv_files)



@app.route("/editor")
def editor():
    image = request.args.get("image")
    csv_file = request.args.get("csv")

    import pandas as pd
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, csv_file))
    columns = list(df.columns)

    return render_template("editor.html", image=image, csv_file=csv_file, columns=columns)



@app.route("/edit/<image_name>")
def edit_image(image_name):
    files = os.listdir(UPLOAD_FOLDER)

    # Only CSV files
    csv_files = [f for f in files if f.lower().endswith(".csv")]

    return render_template(
        "edit_image.html",
        image_name=image_name,
        csv_files=csv_files
    )



@app.route("/generate", methods=["POST"])
def generate():
    import pandas as pd
    from PIL import Image, ImageDraw, ImageFont

    image_name = request.form["image"]
    csv_name = request.form["csv"]
    fields = request.form.get("fields")   # JSON string
    fields = eval(fields)                 # Convert back to dict

    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, csv_name))

    output_dir = os.path.join("generated")
    os.makedirs(output_dir, exist_ok=True)

    generated_files = []

    for index, row in df.iterrows():

        base = Image.open(os.path.join(UPLOAD_FOLDER, image_name))
        draw = ImageDraw.Draw(base)
        font = ImageFont.load_default()

        for field, pos in fields.items():
            x, y = pos
            value = str(row[field])
            draw.text((x, y), value, fill="black", font=font)

        output_file = f"{index}_{image_name}"
        output_path = os.path.join(output_dir, output_file)
        base.save(output_path)

        generated_files.append((output_file, row))

    return {"status": "done", "generated": generated_files}



@app.route("/send-emails", methods=["POST"])
def send_emails():
    import pandas as pd

    csv_name = request.form["csv"]
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, csv_name))

    generated_folder = "generated"

    EMAIL_USER = "mradulnatani0@gmail.com"
    EMAIL_PASS = "mp134055"

    for i, row in df.iterrows():
        email = row.get("email") or row.get("Email") or row.get("mail")
        if not email:
            continue

        filename = f"{i}_{request.form['image']}"
        filepath = os.path.join(generated_folder, filename)

        msg = EmailMessage()
        msg["Subject"] = "Your Certificate"
        msg["From"] = EMAIL_USER
        msg["To"] = email
        msg.set_content("Please find your generated image attached.")

        with open(filepath, "rb") as f:
            msg.add_attachment(f.read(), maintype="image", subtype="png", filename=filename)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

    return "Emails sent!"




# ... your existing code ...

PREVIEWS_FOLDER = "previews"
os.makedirs(PREVIEWS_FOLDER, exist_ok=True)

@app.route("/save_template", methods=["POST"])
def save_template():
    """
    Saves template and generates images for each CSV row.
    """
    data = request.get_json()
    image_name = data["image"]
    csv_file = data["csv"]
    placements = data["placements"]

    # Load CSV
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, csv_file))
    template_name = os.path.splitext(image_name)[0]
    preview_folder = os.path.join(PREVIEWS_FOLDER, template_name)
    os.makedirs(preview_folder, exist_ok=True)

    # Open base image
    base_path = os.path.join(UPLOAD_FOLDER, image_name)
    base_image = Image.open(base_path)

    for idx, row in df.iterrows():
        img = base_image.copy()
        draw = ImageDraw.Draw(img)
        # You can change font path if needed
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

        for placement in placements:
            col = placement["col"]
            nx = placement["x"]
            ny = placement["y"]
            font_size = placement["font_size"]
            color = placement["color"]

            text = str(row[col])  # value from CSV
            font = ImageFont.truetype(font_path, font_size)

            x = int(nx * img.width)
            y = int(ny * img.height)

            draw.text((x, y), text, font=font, fill=color)

        # Save generated image
        out_path = os.path.join(preview_folder, f"row_{idx+1}.png")
        img.save(out_path)

    return jsonify({"status":"ok", "template_name": template_name})





@app.route("/generate_images", methods=["POST"])
def generate_images():
    data = request.json
    template_name = data["template_name"]
    image_file = data["image"]
    csv_file = data["csv"]
    placements = data["placements"]

    template_folder = os.path.join(GENERATED_FOLDER, template_name)
    os.makedirs(template_folder, exist_ok=True)

    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, csv_file))
    for idx, row in df.iterrows():
        img_path = os.path.join(UPLOAD_FOLDER, image_file)
        img = Image.open(img_path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        for p in placements:
            x = p["x"] * img.width
            y = p["y"] * img.height
            font = ImageFont.load_default()  # replace with actual font if needed
            draw.text((x, y), str(row[p["col"]]), fill=p["color"], font=font)
        save_path = os.path.join(template_folder, f"{idx}.png")
        img.save(save_path)

    return jsonify({"status": "ok", "generated": os.listdir(template_folder)})


@app.route("/process_batch", methods=["POST"])
def process_batch():
    template_name = request.form.get("template_name")
    send_email = request.form.get("send_email") == "true"

    if not template_name:
        return jsonify({"status": "error", "message": "No template_name provided"}), 400

    template_path = os.path.join(TEMPLATE_DIR, template_name + ".json")
    if not os.path.exists(template_path):
        return jsonify({"status": "error", "message": "Template JSON not found"}), 400

    with open(template_path) as f:
        template = json.load(f)

    image_file = template.get("image")
    csv_file = template.get("csv")
    placements = template.get("placements")

    if not csv_file:
        return jsonify({"status": "error", "message": "CSV not specified in template"}), 400

    csv_path = os.path.join(UPLOAD_FOLDER, csv_file)
    if not os.path.exists(csv_path):
        return jsonify({"status": "error", "message": f"CSV file not found: {csv_file}"}), 400

    import csv
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = list(csv.DictReader(f))

    if not reader:
        return jsonify({"status": "error", "message": "CSV has no data"}), 400

    # Prepare output directory
    timestamp = int(time.time())
    out_dir = os.path.join(GENERATED_FOLDER, f"{template_name}_{timestamp}")
    os.makedirs(out_dir, exist_ok=True)

    from PIL import Image, ImageDraw, ImageFont

    for idx, row in enumerate(reader):
        img_path = os.path.join(UPLOAD_FOLDER, image_file)
        base = Image.open(img_path).convert("RGBA")
        draw = ImageDraw.Draw(base)

        for p in placements:
            col = p["col"]
            if col not in row:
                continue

            text = str(row[col])
            font_size = int(p.get("font_size", 32))
            color = p.get("color", "#000000")

            # Use system font or fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                font = ImageFont.load_default()

            x = int(p["x"] * base.width)
            y = int(p["y"] * base.height)
            draw.text((x, y), text, fill=color, font=font)

        # Save as PNG to avoid RGBA/JPEG issues
        out_file = os.path.join(out_dir, f"{idx}.png")
        base.save(out_file, format="PNG")

        # Optional: add email logic here if send_email==True

    return jsonify({"status": "ok", "template_name": f"{template_name}_{timestamp}", "generated_files": os.listdir(out_dir)})



@app.route("/save_template_new", methods=["POST"])
def save_template_new():
    data = request.json
    template_name = f"{data['image']}_{int(time.time())}"
    template_path = os.path.join(TEMPLATE_DIR, template_name + ".json")
    with open(template_path, "w") as f:
        json.dump(data, f)
    return jsonify({"status": "ok", "template_name": template_name})


@app.route("/preview")
def preview_auto():
    return redirect(url_for("preview_latest"))


@app.route("/generated/<path:filename>")
def serve_generated(filename):
    return send_from_directory("generated", filename)



@app.route("/preview_latest")
def preview_latest():
    base_path = "generated"

    # Find all directories inside generated/
    folders = [
        f for f in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, f))
    ]

    if not folders:
        return render_template("preview.html", images=[])

    # Pick the most recently modified folder
    latest = sorted(
        folders,
        key=lambda x: os.path.getmtime(os.path.join(base_path, x)),
        reverse=True
    )[0]

    # Build file list
    folder_path = os.path.join(base_path, latest)
    images = [
        f"/generated/{latest}/{img}"
        for img in os.listdir(folder_path)
        if img.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    return render_template("preview.html", images=images)



if __name__ == "__main__":
    app.run(debug=True)
