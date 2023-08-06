from pathlib import Path
from typing import Union
import os
import shutil

def resolve_path(path:Union[str,Path]):
    if isinstance(path,str):
        path=Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} is not found")
    return path

def create_dir(dir_path:Union[str,Path],parents:bool=False):
    if isinstance(dir_path,str):
        dir_path=Path(dir_path)
    if not dir_path.exists():
        dir_path.mkdir(parents=parents,exist_ok=True)


def delete_pycache_dirs(root_dir):
    for dir_name, subdirs, files in os.walk(root_dir):
        for subdir in subdirs:
            if subdir == "__pycache__":
                shutil.rmtree(os.path.join(dir_name, subdir))