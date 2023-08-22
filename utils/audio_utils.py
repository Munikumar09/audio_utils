from pydub import AudioSegment
import mutagen
from pathlib import Path
from typing import Union,Dict,List
from tqdm import tqdm
from utils.common import resolve_path
import subprocess
import re
import json

def get_audio_info(audio_file):
    cmd = ['ffprobe', '-loglevel', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', str(audio_file)] 

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = p.communicate()

    audio_info = json.loads(out)
    sample_fmt = audio_info['streams'][0]['sample_fmt']
    bit_depth=0
    if sample_fmt == 'fltp':
        bit_depth = 16
    elif sample_fmt == 's16':
        bit_depth = 16 
    elif sample_fmt == 's32':
        bit_depth = 32
    bit_rate= audio_info["streams"][0].get("bit_rate",None)
    if bit_rate==None:
        bit_rate=audio_info["format"].get("bit_rate")
    if bit_rate!=None:
        bit_rate= f"{int(bit_rate)//1000} kb/s"
    audio_data={
    "audio_file":str(audio_file),
    "channels": audio_info["streams"][0]["channels"],
    "duration": audio_info["streams"][0]["duration"],
    "sample_rate": audio_info["streams"][0]["sample_rate"],
    "codec":audio_info["streams"][0]["codec_name"],
    "bit_depth or pcm ": bit_depth,
    "bit_rate": bit_rate
    }
    return audio_data
def get_duration_ffprobe(file_path):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 
        'format=duration', str(file_path)]

    output = subprocess.check_output(cmd).decode('utf-8')
    duration = re.search(r'duration=(.+)', output).group(1)
    return float(duration)

def get_duration_mutagen(file_path:Union[str,Path])->float:
    data=mutagen.File(file_path)
    duration=data.info.length
    return duration

def get_total_audio_duration(audio_path:Union[str,Path,List[str]],format:str="wav")->Dict[str,float]:
    if not isinstance(audio_path,list):
        audio_path=resolve_path(audio_path)
        audio_path=list(Path(audio_path).glob(f"*.{format}"))
    total_duration=0
    min_duration=1e10
    max_duration=1e-10
    
    audio_file_duration={}
    for file_path in tqdm(audio_path):
        
        if Path(file_path).suffix ==".m4a":
            duration=get_duration_ffprobe(str(file_path))
        else:
            duration=get_duration_mutagen(file_path)
        min_duration=min(min_duration,duration)
        max_duration=max(max_duration,duration)
        total_duration += duration
        audio_file_duration[file_path.name]=duration
        
    audio_file_duration["max_duration"]=max_duration
    audio_file_duration['min_duration']=min_duration
    audio_file_duration['total_duration']=total_duration
    return audio_file_duration