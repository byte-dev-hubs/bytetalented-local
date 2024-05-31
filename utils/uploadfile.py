import os
import uuid
import shutil

cwd = os.getcwd()
save_path = os.path.join(cwd, 'uploads')
os.makedirs(save_path, exist_ok=True)

def upload_file(filename):
    base_filename = os.path.splitext(filename)[1]
    hash_filename = str(uuid.uuid4()) + base_filename
    destination = os.path.join(save_path, hash_filename)
    shutil.move(filename, destination)
    return hash_filename