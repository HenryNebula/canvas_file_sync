from canvasapi import Canvas
from canvasapi.exceptions import CanvasException
from pathlib import Path
import json
from multiprocessing.dummy import Pool
import requests
import argparse


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
            print(sibiling.name)
            folder_name = sibiling.name
            recursive_files(sibiling, path / Path(folder_name), pool)
    except CanvasException as ex:
        print("[Warning] Exception {} occurs when reading sub-folders from \"{}\"".format(ex.message, folder.name))


def download_course(course, base_path, pool: Pool):
    try:
        top_folders = course.get_folders()
        names = [f.name for f in course.get_folders()]
        root_folder = top_folders[names.index("course files")]
        recursive_files(root_folder, 
                        Path(base_path) / Path(course.name.replace(" ", "_")),
                        pool)
    except ValueError:
        print("[Warning] No 'course files' directory found as root folder for course {}!\nCurrent top folders are {}"
        .format(course.name, [f.name for f in course.get_folders()]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", help="relative path for config file, the default is config.json", default="config.json")
    parser.add_argument("--course", type=int,
                        help="course id for the course needs downloading, " + 
                        "the default value (-1) will just print a ordered list of courses; " + 
                        "-2 will download all files and other integer will download the corresponding course.", 
                        default="-1")
    parser.add_argument("--threads", help="number of threads used for downloading, default 5", default=5)

    args = parser.parse_args()

    with open(args.config) as f:
        config = json.loads(f.read())

    canvas = Canvas(config["web_url"], config["token"])

    courses = canvas.get_courses()

    length = len(list(courses))

    pool = Pool(processes=args.threads)

    if args.course == -1:
        for id, course in enumerate(courses):
            print("\t{}\t{}\n".format(id, course))
    elif args.course == -2:
        for course in courses:
            download_course(course, config["base_path"], pool)
    elif args.course in range(0, length):
        course = courses[args.course]
        download_course(course, config["base_path"], pool)
    else:
        print("Course ID {} out of bound [{}, {}]".format(args.course, 0, length - 1))

