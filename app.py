#In cmd 1.set path 2.python -m venv venv(to create a virtual env) 3.vevv\Scripts\activate(to activate) 4.pip install flask pillow --all these steps in cmd
#create file app.py for the code (it is flask code)
from flask import Flask, request, jsonify
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})
    
    files = request.files.getlist('image')
    if len(files) == 0:
        return jsonify({'error': 'No selected file'})
    
    output_files = []
    for file in files:
        if file and file.filename:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Convert image to grayscale
            img = Image.open(filepath).convert('L')
            output_path = os.path.join(UPLOAD_FOLDER, 'grayscale_' + file.filename)
            img.save(output_path)

            output_files.append ({'original': filepath, 'grayscale': output_path})

        return jsonify({'message': 'Image converted to grayscale', 'outputs': output_files})

if __name__ == '__main__':
    app.run(debug=True)
