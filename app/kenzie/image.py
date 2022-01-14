from werkzeug.datastructures import FileStorage
from flask import safe_join, send_file
import os

FILES = os.getenv("FILES_DIRECTORY")
EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS").split(",")

def list_all_images():
    dir_list = []

    for extension in EXTENSIONS:
        dir_list.append(os.listdir(f'./files/{extension}'))

    files_list = []
    for file in dir_list:
        files_list.append(file[0])
    
    return files_list


def list_by_extension(extension:str):
    if extension not in EXTENSIONS:
        raise

    extension = extension.lower()

    files_list = os.listdir(f'./files/{extension}')

    return files_list

def define_download_path(file_name):
    files_list = list_all_images()
    
    if file_name not in files_list:
        raise

    extension = file_name.split('.')[1]

    path = safe_join(os.path.realpath(FILES),extension,file_name)

    return path

def file_already_exists(filename: str, extension: str)-> bool:
    extension_path = os.path.join(FILES, extension)

    return filename in os.listdir(extension_path)

def upload_image(file: FileStorage) -> None:
    filename: str = file.filename

    root, extension = os.path.splitext(filename)
    extension = extension.replace(".", "")

    if file_already_exists(filename, extension):
        raise FileExistsError

    saving_path = os.path.join(FILES, extension, filename)
    print(saving_path)

    file.save(saving_path)

def download_zip(file_type: str, compression_ratio: str):
    output_file = f'{file_type}.zip'
    input_path = os.path.join(FILES, file_type)
    output_path_file = os.path.join('/tmp', output_file)

    if os.path.isfile(output_path_file):
        os.remove(output_path_file)

    command = f'zip -r -j -{compression_ratio} {output_path_file} {input_path}'

    os.system(command)

    return send_file(output_path_file, as_attachment=True)