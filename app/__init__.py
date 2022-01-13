from flask import Flask, request, jsonify, send_file
from app.kenzie.image import create_folders, list_all_images, list_by_extension, define_download_path

app = Flask(__name__)

create_folders()

@app.get('/download/<file_name>')
def download(file_name):
    try:
        path = define_download_path(file_name)
        return send_file(
        path, 
        as_attachment=True), 200
    except:
        return "File not found", 404 

@app.get('/download-zip')
def download_dir_as_zip():
    return "download arquivos em um zip por tipo"

@app.get('/files')
def list_files():
    return jsonify(list_all_images()), 200

@app.get('/files/<extension>')
def list_files_by_extension(extension):
    try:
        return jsonify(list_by_extension(extension)), 200
    except:
        return "Invalid format", 404

@app.post('/upload')
def upload_file():
    return "upload de arquivo"