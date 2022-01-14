import os

FILES = os.getenv("FILES_DIRECTORY")
EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS").split(",")

def create_folders():

    for extension in EXTENSIONS:
        path = os.path.join(FILES, extension)

        if not os.path.exists(path):
            os.makedirs(path)

create_folders()