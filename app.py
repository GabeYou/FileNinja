from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO
from convert_text import detect_document, add_to_pdf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return "No file part"

    image = request.files["image"]

    if image.name == "":
        return "No selected file"

    if image:
        # Read and process the uploaded image using PIL (Pillow)
        img = Image.open(BytesIO(image.read()))
        # Perform operations on the image (e.g., resizing, filtering, etc.)
        
        # You can return the processed image as a response
        img_data = BytesIO()
        img.save(img_data, format="PNG")
        img_data.seek(0)

        
        paragraph_coords = detect_document(image)
        path = add_to_pdf(paragraph_coords, image.name) # returns path of output file

        # application/pdf
        return send_file(img, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)