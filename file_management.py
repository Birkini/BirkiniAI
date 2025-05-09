import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Flask app setup
app = Flask(__name__)

# File upload configuration
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload a file to the server."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": f"File {filename} uploaded successfully!"}), 200
    else:
        return jsonify({"error": "File type not allowed"}), 400

# Route to list all uploaded files
@app.route('/files', methods=['GET'])
def list_files():
    """List all files in the upload directory."""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({"files": files}), 200

# Route to download a file
@app.route('/files/<filename>', methods=['GET'])
def download_file(filename):
    """Download a file from the server."""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)  # Create the upload directory if it doesn't exist
    app.run(debug=True)
