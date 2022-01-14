from flask import Flask, request, jsonify, send_file
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from app.kenzie import image
from os import getenv

MAX_CONTENT_LENGTH = int(getenv("MAX_CONTENT_LENGTH"))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH * 1024 * 1024

@app.get('/download/<file_name>')
def download(file_name):
    try:
        path = image.define_download_path(file_name)
        return send_file(
        path, 
        as_attachment=True), 200
    except:
        return "File not found", 404 

@app.get('/download-zip')
def download_dir_as_zip():
    file_type = request.args.get("file_extension")
    compression_ratio = request.args.get("compression_ratio", 6)

    if not file_type:
        return {'msg': 'Query param `file_extension` is required'}, 400
    
    image.download_zip(file_type, compression_ratio)

    return ''



@app.get('/files')
def list_files():
    return jsonify(image.list_all_images()), 200

@app.get('/files/<extension>')
def list_files_by_extension(extension):
    try:
        return jsonify(image.list_by_extension(extension)), 200
    except:
        return "Invalid format", 404

@app.post('/upload')
def upload_file():
    files: ImmutableMultiDict[str, FileStorage] = request.files

    for file in files.values():
        try:
            image.upload_image(file)
        except FileExistsError:
            return {'msg': 'File already exists'}, 409
        except :
            return {'msg': 'Extension not supported'}, 415

    return ''