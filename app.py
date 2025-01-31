from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"})
    
    files = request.files.getlist('image')  # Get all files from the request
    output_paths = []

    for file in files:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Convert to grayscale
        image = Image.open(filepath).convert('L')
        output_path = os.path.join(UPLOAD_FOLDER, f"grayscale_{filename}")
        image.save(output_path)
        output_paths.append(output_path)

    return jsonify({"message": "Images converted to grayscale", "outputs": output_paths})

if __name__ == '__main__':
    app.run(debug=True)
