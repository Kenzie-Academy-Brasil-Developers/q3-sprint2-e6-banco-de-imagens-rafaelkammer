# from os import getenv, mkdir, listdir, walk
from flask import safe_join, jsonify
import os

FILES = os.getenv("FILES_DIRECTORY")
EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS").split(",")
MAX_LENGTH = os.getenv("MAX_CONTENT_LENGTH")

def create_folders():
    if "files" not in os.listdir("./"):

        os.mkdir(f'{FILES}')

        for extension in EXTENSIONS:
            path = f"{FILES}/{extension}"
            os.mkdir(path)

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