import os
from pydub import AudioSegment
import moviepy.editor as mp
import json

def video_to_audio(input_path:str,out_path:str,format:str):
    audio_file_name=input_path.split("/")[-1]
    file_name=audio_file_name.split(".")[0]
    output_file_path=os.path.join(out_path,f"{file_name}.{format}")
    clip = mp.VideoFileClip(input_path)
    clip.audio.write_audiofile(output_file_path)