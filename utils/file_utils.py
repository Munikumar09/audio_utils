import json
from typing import Any, Union, Iterator, List
from pathlib import Path
from utils.common import create_dir, resolve_path
import csv
import os
import tarfile
from tqdm import tqdm
import shutil


def save_json(data: Any, save_path: Union[str, Path], ensure_ascii: bool = True):
    save_path = Path(save_path)
    create_dir(save_path.parent, parents=True)
    with open(save_path, "w") as f:
        json.dump(data, f, ensure_ascii=ensure_ascii)


def load_json(file_path: Union[str, Path]):
    resolve_path(file_path)
    with open(file_path, "r") as f:
        return json.load(f)


def get_audio_exceeds_length(file_path, threshold):
    data = load_json(file_path)
    exceeds_threshold = {}
    for audio_name, duration in data.items():
        if duration >= threshold and audio_name not in [
            "max_duration",
            "min_duration",
            "total_duration",
        ]:
            exceeds_threshold[audio_name] = duration
    return exceeds_threshold


def get_total_duration(file_path):
    data = load_json(file_path)
    if "total_duration" in data:
        return data["total_duration"]
    total_duration = 0
    for audio_name, duration in data.items():
        total_duration += duration
    return total_duration


def copy_files(src: Union[str, Path], dst: Union[str, Path]):
    os.system(f"cp {str(src)} {str(dst)}")

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print('File removed successfully!')
    else:
        print('File does not exist!')

def read_csv(
    csv_filepath: Union[str, Path], as_list: bool = True
) -> Iterator[Union[str, List[str]]]:
    """
    Reads the `csv_filepath` and return the row as either List or str

    Parameters
    ----------
    csv_filepath: ``Union[str, Path]``
        Input CSV file path
    as_list: ``bool``, ( default = True )
        Flag that denotes whether to return the row as `list` or `string`

    Returns
    -------
    ``Union[str, List[str]]``
    """
    with open(csv_filepath, "r") as fp:
        if as_list:
            for row in csv.reader(fp):
                yield row
        else:
            for line in fp:
                yield line

def extract_tar(file_path: Union[str, Path], output_path: str, pattern: str = "*.tgz") -> None:
    """
    Extract the archive file from `file_path` to the "output_path" directory
    """
    if output_path is None or output_path == "":
        raise ValueError(f"{output_path} should not be empty!")

    if isinstance(file_path, str):
        file_path = Path(file_path)

    file_paths: List[Path]
    if file_path.is_file():
        file_paths = [file_path]
    elif file_path.is_dir():
        file_paths = list(file_path.glob(pattern))
    else:
        raise ValueError(f"{file_path} should not be empty!")

    for file_path in file_paths:
        with tarfile.open(file_path) as tar:
            with tqdm(desc=f"Extracting {file_path.name} ") as progress_bar:
                member = tar.next()
                while member is not None:
                    progress_bar.update(1)
                    tar.extract(member, path=output_path)
                    member = tar.next()
                    
                    

def delete_pycache(root_dir: str, folder_name: str):
    """
    Deletes a folder and its contents from a given root directory.

    Parameters
    ----------
    root_dir: `str`
        The path of the root directory to traverse.
    folder_name: `str`
        The name of the folder to delete.

    Raises
    ------
    OSError:
        If the folder cannot be deleted due to permission or other errors.

    Examples
    --------
    >>> delete_folder("Users/Admin/Documents", "pycache")
        Deleting Users/Admin/Documents_pycache_
        Deleting Users/Admin/Documents/project_pycache_
    """
    # Traverse through the directory tree
    for dirpath, dirnames, _ in os.walk(root_dir):
        # Check if the specified folder exists in the current directory
        if folder_name in dirnames:
            # Get the full path of the pycache folder
            pycache_folder_path = os.path.join(dirpath, folder_name)

            # Print the path of the folder being deleted
            print(f"Deleting {pycache_folder_path}")

            # Delete the pycache folder and its contents
            shutil.rmtree(pycache_folder_path)
