# Get Verified

Generate personalized images (such as certificates, badges, or scorecards) from templates and CSV data using this web-based application.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Usage Instructions](#usage-instructions)
- [Features](#features)
- [Mailing Feature (Upcoming)](#mailing-feature-upcoming)
- [Dependencies](#dependencies)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

Get Verified provides a platform to automatically generate dynamic images (e.g. certificates, badges, ID cards) by overlaying fields from a CSV onto predefined coordinates on a template image.

The web interface is built with Flask (Python) for backend logic and HTML/CSS/JS for the frontend.

---

## Project Structure

```
get-verified/
├── app.py                # Main Flask app (all backend logic)
├── uploads/              # Uploaded images and CSV files saved here
├── generated/            # Generated images are saved here
├── templates_data/       # (For image templates, if used)
├── templates_json/       # (Stores JSON descriptor for field placements)
├── previews/             # Preview images for the editor
├── templates/
│   ├── input.html        # Upload form, CSV/image preview
│   ├── edit_image.html   # Editor for associating CSV fields with locations
│   ├── editor.html       # In-browser editor: Drag CSV fields onto image
│   ├── generate.html     # Interface for generating and previewing images
│   └── ...               # Other HTML files for UI
└── ...                   # Other supporting files
```

---

## How It Works

1. **Upload Step**:  
   Upload a template image (e.g., blank certificate) and a CSV file with fields like "Name", "Score", etc.

2. **Field Placement**:  
   - Use the visual editor (`editor.html`) to drag fields (columns from your CSV) onto the locations where you want the text rendered on the image.
   - For each field, set attributes like position, font size, and color.

3. **Preview & Save Template**:  
   Save the placement template. Optionally preview how the images would look with sample data.

4. **Generate Images**:  
   For each row in the CSV, the app overlays each field's value onto the template image based on your placements and generates a personalized image to the `/generated/` directory.

5. **Download or Send Images**:  
   Download your generated images from the `/generated/` folder. (Mailing coming soon!)

---

## Getting Started

### Prerequisites

- **Python 3.7+**
- Recommended: [Virtualenv](https://virtualenv.pypa.io/)

### 1. Clone the Repository

```bash
git clone https://github.com/mradulnatani/get-verified.git
cd get-verified
```

### 2. Create a Virtual Environment & Activate

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install Flask pandas pillow
```

### 4. Run the Application

```bash
python app.py
```

- The app will run on `http://127.0.0.1:5000/`

---

## Usage Instructions

1. **Open the App**  
   Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.

2. **Upload Files**  
   - Upload a CSV file containing the fields for your images (e.g., Name, Score).
   - Upload a template image file (PNG/JPG/JPEG/GIF).

3. **Select & Map Fields**  
   - Choose your uploaded image to edit.
   - Select the corresponding CSV.
   - In the editor, drag and drop fields onto the image where you want each field to appear.
   - Set font size and color as needed.

4. **Preview Placement**  
   - Use the "Preview Generated Images" option to see how the placement looks with actual data from your CSV.

5. **Save the Template**  
   - Click "Save Template" when satisfied. This saves your placement for future use.

6. **Generate Images**  
   - Click "Generate & Email" to produce all personalized images into `/generated/`.
   - (Optional) Download generated images.

---

## Features

- Upload CSV and images via a web UI.
- Interactive drag-and-drop editor for mapping CSV columns to image regions.
- Font customization (size, color).
- Preview before batch generation.
- Outputs all images in `/generated/` (PNG format).
- User-friendly and extensible.

---

## Mailing Feature (Upcoming)

**Coming Soon:**  
You will be able to automatically send each generated image to the corresponding recipient's email address as specified in your CSV file. This powerful batch-emailing feature will streamline distribution (e.g., for certificates, badges, etc.) and will be integrated into the generation workflow.

---

## Dependencies

- Flask
- pandas
- pillow (PIL)
- [Optionally for email: smtplib, email.message]

Install all dependencies with:

```bash
pip install Flask pandas pillow
```

---

## Troubleshooting

- **Images aren't generating:**  
  Ensure your CSV columns match field labels exactly; check for typos.
- **Fonts Missing:**  
  The default font should be used, but you may need to install `DejaVuSans-Bold.ttf` for advanced font options.
- **Permission errors:**  
  Ensure the app can write to the `/uploads/`, `/generated/`, and `/previews/` directories.
- **Port conflicts:**  
  If something else is running on port 5000, either stop it or run Flask on another port with `python app.py --port=XXXX`.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
