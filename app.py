from flask import Flask, request, jsonify           #impost necessary modules from flask to create web app and handle request
from PIL import Image           #import os to interact with os
import os           #import pillow lib to process and manipulate images

app = Flask(__name__)           #initialize a flask app, which will handle requests

UPLOAD_FOLDER = "./uploads"         #set the folderwhere updated files will be saved
if not os.path.exists(UPLOAD_FOLDER):           #check if the folder exists
    os.makedirs(UPLOAD_FOLDER)          #create if it doesn't

@app.route('/upload', methods=['POST'])         #defint a route for handling file uploads, acccepting onlt post requests

def upload_files():         #func to process uploaded files
    if 'image' not in request.files:            #check if the 'image' exists in the request
        return jsonify({"error": "No file part"})           #if not return error
    
    files = request.files.getlist('image')  # Get all files from the request(as lists)
    output_paths = []           #create an empty listto store path of o/p images

    for file in files:          #iterate over each file
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)            #save original file in folder
        file.save(filepath)

        # now open the saved image and convert to grayscale
        image = Image.open(filepath).convert('L')
        #save the grayscale version to the same folder
        output_path = os.path.join(UPLOAD_FOLDER, f"grayscale_{filename}")
        image.save(output_path)

        output_paths.append(output_path)            #add the o/p paths to the o/p list(we made earlier)

    return jsonify({"message": "Images converted to grayscale",         #retun success msg along with o/p paths
                    "outputs": output_paths})           

#Entry point of the application
if __name__ == '__main__':
    app.run(debug=True)         #start the flask application in debugging mode
