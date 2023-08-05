import hashlib
import os
import shutil
from typing import List


def hex_digest_files(filenames: List[str], algorithm_name: str) -> str:
    block_size = 65536
    hash_object = hashlib.new(algorithm_name)
    for filename in filenames:
        with open(filename, 'rb') as file_handle:
            buf = file_handle.read(block_size)
            while len(buf) > 0:
                hash_object.update(buf)
                buf = file_handle.read(block_size)
    return hash_object.hexdigest()


def hex_digest_file(filename: str, algorithm_name: str) -> str:
    return hex_digest_files(filenames=[filename], algorithm_name=algorithm_name)


def sha1_file(filename: str) -> str:
    return hex_digest_file(filename=filename, algorithm_name="sha1")


def sha1_files(filenames: List[str]) -> str:
    return hex_digest_files(filenames=filenames, algorithm_name="sha1")


def makedirs_for_file(filename: str):
    folder = os.path.dirname(filename)
    if folder != "":
        os.makedirs(folder, exist_ok=True)


def copy_mkdir(source: str, destination: str):
    makedirs_for_file(destination)
    shutil.copy(source, destination)


def unlink_files(files: List[str], only_if_exist: bool=True) -> None:
    for file in files:
        if only_if_exist:
            if os.path.isfile(file):
                os.unlink(file)
        else:
            os.unlink(file)


def files_under_folder(folder: str) -> List[str]:
    f = []
    for (dir_path, _dir_names, filenames) in os.walk(folder):
        f.extend([os.path.join(dir_path, filename) for filename in filenames])
    return f


def files_under_folders(folders: List[str]) -> List[str]:
    f = []
    for folder in folders:
        f.extend(files_under_folder(folder))
    return f


def sha1_folders(folders: List[str]) -> str:
    return sha1_files(filenames=files_under_folders(folders=folders))


def sha1_files_folders(files: List[str], folders: List[str]) -> str:
    f = files
    f.extend(files_under_folders(folders=folders))
    return sha1_files(f)


def touch(filename: str) -> None:
    with open(filename, "w"):
        pass
