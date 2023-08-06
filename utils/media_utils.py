import mutagen
from pathlib import Path
from typing import Union,Dict,List
from tqdm import tqdm
from utils.common import resolve_path

def get_duration_mutagen(file_path:Union[str,Path])->float:
    data=mutagen.File(file_path)
    duration=data.info.length
    return duration

def get_total_audio_duration(audio_path:Union[str,Path,List[str]],format:str="wav")->Dict[str,float]:
    if not isinstance(audio_path,list):
        audio_path=resolve_path
        audio_path=list(Path(audio_path).glob(f"*.{format}"))
    total_duration=0
    min_duration=1e10
    max_duration=1e-10
    audio_file_duration={}
    for file_path in tqdm(audio_path):
        duration=get_duration_mutagen(file_path)
        min_duration=min(min_duration,duration)
        max_duration=max(max_duration,duration)
        total_duration += duration
        audio_file_duration[file_path.name]=duration
    audio_file_duration["max_duration"]=max_duration
    audio_file_duration['min_duration']=min_duration
    audio_file_duration['total_duration']=total_duration
    return audio_file_duration
