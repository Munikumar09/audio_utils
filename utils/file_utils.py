import json
from typing import Any, Union
from pathlib import Path
from utils.common import create_dir, resolve_path

def save_json(data: Any, save_path: Union[str, Path], ensure_ascii: bool = True):
    save_path=Path(save_path)
    create_dir(save_path.parent,parents=True)
    with open(save_path, "w") as f:
        json.dump(data, f, ensure_ascii=ensure_ascii)


def load_json(file_path: Union[str, Path]):
    resolve_path(file_path)
    with open(file_path, "r") as f:
        return json.load(f)
    
def get_audio_exceeds_length(file_path,threshold):
    data=load_json(file_path)
    exceeds_threshold={}
    for audio_name,duration in data.items():
        if duration>= threshold and audio_name not in ["max_duration","min_duration","total_duration"]:
            exceeds_threshold[audio_name]=duration
    return exceeds_threshold
def get_total_duration(file_path):
    data=load_json(file_path)
    if "total_duration" in data:
        return data["total_duration"]
    total_duration=0
    for audio_name,duration in data.items():
        total_duration+= duration
    return total_duration
    
