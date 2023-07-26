import json
from typing import Any, Union
from pathlib import Path
from utils.common import create_dir, resolve_path

def save_json(data: Any, save_path: Union[str, Path], ensure_ascii: bool = True):
    save_path=Path(save_path)
    create_dir(save_path.parent)
    with open(save_path, "w") as f:
        json.dump(data, f, ensure_ascii=ensure_ascii)


def load_json(file_path: Union[str, Path]):
    resolve_path(file_path)
    with open(file_path, "r") as f:
        return json.load(f)
