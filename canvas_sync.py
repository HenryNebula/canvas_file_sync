from canvasapi import Canvas
from canvasapi.exceptions import CanvasException
from pathlib import Path
import json
from multiprocessing.dummy import Pool
import requests


class FileObj:
    def __init__(self, file, download_path):
        self.file = file
        self.download_path = download_path


def download_helper(file_obj: FileObj):
    path = file_obj.download_path
    if not path.exists() or path.stat().st_size < file_obj.file.size: 
        print("\t [downloading]: {}".format(path))
        response = requests.get(file_obj.file.url)
        with open(path, "wb") as f:
            f.write(response.content)
        
        print("\t [finished]: {}".format(path))

    else:
        print("\t [cached]: {}".format(path))


def recursive_files(folder, path: Path, pool: Pool):
    print("current folder: {}".format(path))
    if not path.is_dir(): path.mkdir(parents=True)

    files = []

    try:
        for file in folder.get_files():
            file_path = path / Path(file.display_name)
            files.append(FileObj(file, file_path))
    except CanvasException as ex:
        print("[Warning] Exception {} occurs when reading files from folder \"{}\"".format(ex.message, folder.name))
    
    pool.map(download_helper, files)

    try:
        for sibiling in folder.get_folders():
            folder_name = sibiling.name
            recursive_files(sibiling, path / Path(folder_name), pool)
    except CanvasException as ex:
        print("[Warning] Exception {} occurs when reading sub-folders from \"{}\"".format(ex.message, folder.name))


def download_course(course, base_path, pool: Pool):
    try:
        root_folder = course.get_folders()[0]
        recursive_files(root_folder, 
                        Path(base_path) / Path(course.name.replace(" ", "_")),
                        pool)
    except IndexError:
        print("No root folder for course {}".format(course.name))


if __name__ == "__main__":
    with open("config.json") as f:
        config = json.loads(f.read())

    canvas = Canvas(config["web_url"], config["token"])

    courses = canvas.get_courses()

    pool = Pool(processes=config["num_threads"])

    for course in courses:
        download_course(course, config["base_path"], pool)

