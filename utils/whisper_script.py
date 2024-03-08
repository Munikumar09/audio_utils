import warnings
#from zspeech.inference.client import ZSpeech
from pathlib import Path

import torch
#from whisper import transcribe
import whisper
from tqdm import tqdm
#from zspeech.utils.file_utils import create_dir, extract_tar
from typing import Union

warnings.filterwarnings("ignore")
import json
import shutil

from librosa import get_duration

DEFAULT_LANGUAGE = "en"

audio_root = Path("/media/dataset-harddisk/munikumar/utils/audio_utils/data/test_audio/total_split")
copy_dir = Path("/media/data/munikumar/data_annotation/processed_audio/form4")

output_dir =  Path("/media/dataset-harddisk/munikumar/utils/audio_utils/data/test_audio/whisper_results")




def create_dir(dir_name: Union[str, Path], create_sub_dirs: bool = True):
    """
    Create a new directory if it's not present

    Parameters
    ----------
    dir_name: ``str``
        Directory name to be created
    create_sub_dirs: ``bool``
        Flag denotes whether to create sub directories or not
    """
    if isinstance(dir_name, str):
        dir_name = Path(dir_name)

    if not dir_name.exists():
        dir_name.mkdir(parents=create_sub_dirs)

def get_file_paths():
    all_audio_data = []

    for audio_file in tqdm(list(audio_root.glob("*mp3"))):
        # audio_file = audio_root / audio_name

        json_path = output_dir / f"{Path(audio_file).stem}.json"

        if json_path.exists():
            continue

        size = audio_file.stat().st_size
        all_audio_data.append((audio_file, size, json_path))

    all_audio_data = sorted(all_audio_data, key=lambda x: x[1], reverse=True)

    for audio_file, _, json_path in all_audio_data:
        yield audio_file, json_path


def save_model_trans(model, audio_path, json_path):
    try:
        if get_duration(filename=(str(audio_path))) < 1:
            raise RuntimeError("Duration less than 1")

        results = model.transcribe(str(audio_path), language="en")
        with (output_dir / json_path.name).open("w") as fp:
            json.dump(results, fp, indent=4)


    except (RuntimeError, IndexError) as e:
        results = {}
        print(e)
        with json_path.open("w") as fp:
            json.dump({}, fp)


def split_files(case):
    all_audio_paths = list(get_file_paths())
    return all_audio_paths
    print("-" * 50)
    print(f"Total audios to process === {len(all_audio_paths)}")
    print("-" * 50)
    if case ==1:
        start = 0
        end = int(len(all_audio_paths) / 4)
    elif case == 2:
        start = int(len(all_audio_paths) / 4)
        end = int(len(all_audio_paths) / 4) * 2
    elif case == 3:
        start = int(len(all_audio_paths) / 4) * 2
        end = int(len(all_audio_paths) / 4) * 3
    elif case == 4:
        start = int(len(all_audio_paths) / 4) * 3
        end = int(len(all_audio_paths) / 4) * 4
        
    all_audio_paths = all_audio_paths[start: end]
    print(start, end)
    print("-" * 50)
    print("-" * 50)


    return all_audio_paths


if __name__ == "__main__":
    model = whisper.load_model("medium",device="cuda:0")
    all_audio_paths = split_files(4)
        

    count=0
    for audio_path, json_path in tqdm(all_audio_paths):
        save_model_trans(model, audio_path, json_path)
        # output_file =copy_dir / (Path(audio_path).stem + ".mp3" )
        # shutil.copy(audio_path, output_file)
        count +=1
    print('*'*50)
    print(f"Total processed Audio : {count}")
    print("*"*50)
