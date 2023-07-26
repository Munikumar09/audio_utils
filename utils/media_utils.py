import mutagen
from pathlib import Path
from typing import Union,Dict
from tqdm import tqdm

def get_duration_mutagen(file_path:Union[str,Path])->float:
    data=mutagen.File(file_path)
    duration=data.info.length
    return duration

def get_total_audio_duration(folder_path:Union[str,Path],format:str)->Dict[str,float]:
    total_duration=0
    min_duration=1e10
    max_duration=1e-10
    audio_file_duration={}
    for file_path in tqdm(Path(folder_path).glob(f"*.{format}")):
        duration=get_duration_mutagen(file_path)
        min_duration=min(min_duration,duration)
        max_duration=max(max_duration,duration)
        total_duration += duration
        audio_file_duration[file_path.name]=duration
    audio_file_duration["max_duration"]=max_duration
    audio_file_duration['min_duration']=min_duration
    audio_file_duration['total_duration']=total_duration
    return audio_file_duration