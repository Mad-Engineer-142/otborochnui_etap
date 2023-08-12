import os

def search_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            file_path = os.path.join(root, filename)
            return file_path
    return None