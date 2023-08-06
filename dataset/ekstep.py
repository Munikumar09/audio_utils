from utils.file_utils import load_json
from pathlib import Path
from utils.media_utils import get_total_audio_duration
from utils.transcription_utils import clean_and_verify_transcript_hi
from typing import Dict

def get_unique_characters(transcription_path):
    data=load_json(transcription_path)
    unique_characters=set()
    for audio,text in data.items():
        unique_characters.update(list(text))
    return unique_characters

def get_transcript_data(file_path):
    data=load_json(file_path)
    audio_data={}
    for record in data:
        file_name=record["audioFilename"]
        text=record["text"]
        audio_data[file_name]=text
    return audio_data

def get_empty_transcriptions(file_path):
    audio_path_transcription=load_json(file_path)
    empty_transcripts={}
    for audio,transcript in audio_path_transcription.items():
        if transcript== "None":
            empty_transcripts[audio]=transcript
    return empty_transcripts

def get_total_empty_transcripts_duration(audio_path:str,empty_transcripts:Dict[str,str]):
    audio_path=Path(audio_path)
    empty_transcript_audio_paths=[audio_path/audio_name for audio_name,transcription in empty_transcripts.items()]
    duration=get_total_audio_duration(empty_transcript_audio_paths)
    return duration

def get_non_hindi_text(transcription_path):
    non_hindi_text={}
    data=load_json(transcription_path)
    for audio,text in data.items():
        if text != "None":
            clean_text,non_hi_chars=clean_and_verify_transcript_hi(text)
            if len(non_hi_chars) !=0:
                non_hindi_text[audio]={clean_text:non_hi_chars}
    return non_hindi_text