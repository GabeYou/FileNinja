from flask import Flask, render_template, request, send_file
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return "No file part"

    image = request.files["image"]

    if image.filename == "":
        return "No selected file"

    if image:
        # Read and process the uploaded image using PIL (Pillow)
        img = Image.open(BytesIO(image.read()))
        # Perform operations on the image (e.g., resizing, filtering, etc.)
        img = img.resize((200, 200))
        
        # You can return the processed image as a response
        img_data = BytesIO()
        img.save(img_data, format="PNG")
        img_data.seek(0)
        
        return send_file(img_data, mimetype="image/png")


    # return "recived: {}".format(request.form)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)