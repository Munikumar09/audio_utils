from pathlib import Path
import os
import shutil


def resolve_path(path: str | Path) -> Path:
    """
    Check if the given path exists and return the resolved path.

    Parameters
    ----------
    path: ``str | Path``
        The path to be resolved.

    Returns
    -------
    path: ``Path``
        The resolved path.
    """
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"{path} is not found")

    return path


def create_dir(dir_path: str | Path, parents: bool = False):
    """
    Create a directory if it does not exist.

    Parameters
    ----------
    dir_path: ``str | Path``
        The path to the directory to be created.
    parents: ``bool``
        If True, also create any missing parent directories.

    """
    if isinstance(dir_path, str):
        dir_path = Path(dir_path)
    if not dir_path.exists():
        dir_path.mkdir(parents=parents, exist_ok=True)


def remove_dir(dir_name: str | Path):
    """
    Delete an existing directory

    Parameters
    ----------
    dir_name: ``str | Path``
        Directory name to be deleted
    """
    if isinstance(dir_name, str):
        dir_name = Path(dir_name)

    if dir_name.exists():
        shutil.rmtree(dir_name)


def delete_pycache_dirs(root_dir: str | Path):
    """
    Delete all __pycache__ directories in the specified root directory.

    Parameters
    ----------
    root_dir: ``str | Path``
        The root directory in which to search for __pycache__ directories.
    """

    for dir_name, subdirs, files in os.walk(root_dir):
        for subdir in subdirs:
            if subdir == "__pycache__":
                shutil.rmtree(os.path.join(dir_name, subdir))
