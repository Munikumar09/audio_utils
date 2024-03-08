import sys
sys.path.append("..")
from utils.audio_utils import get_total_audio_duration,get_audio_info
from pathlib import Path
from tqdm import tqdm
from utils.file_utils import save_json
from utils.transcription_utils import clean_and_verify_transcript_hi,get_transcription_info,get_stats,get_total_stats
from collections import Counter
from utils.conversions import sec_to_time
import csv
from ai4bharat.transliteration import XlitEngine
import re

save_path=Path("/media/dataset-harddisk/munikumar/utils/audio_utils/data/spring_inx")
text_path=Path("/media/dataset-harddisk/munikumar/datasets/hindi_dataset/spring_inx/sprint_inx_raw/SPRING_INX_Hindi_R1/eval/eval_text")


e=XlitEngine("hi")

def load_transcription(transcription_path):
    with open(transcription_path, "r", encoding="utf-8") as fp:
        reader=csv.reader(fp,delimiter='\t')
        transcriptions={transcription[0]:transcription[1] for transcription in reader}
        return transcriptions

    
for data_split in ["eval","dev","train"]:
    text_path=Path("/media/dataset-harddisk/munikumar/datasets/hindi_dataset/spring_inx/sprint_inx_raw/SPRING_INX_Hindi_R1")/data_split/f"{data_split}_text"
    save_path=Path("/media/dataset-harddisk/munikumar/datasets/hindi_dataset/spring_inx/sprint_inx_raw/SPRING_INX_Hindi_R1")/data_split/"text"
    transcriptions=load_transcription(text_path)

    transliterated_transcriptions=[]
    print(f"Transliterating {data_split} data")
    for file_id, transcription in tqdm(transcriptions.items()):
        transliterated=e.translit_sentence(transcription)["hi"]
        transcription_data=f"{file_id}\t{transliterated}"
        transliterated_transcriptions.append(transcription_data)
    with open(save_path, "w", encoding="utf-8") as fp:
        fp.write("\n".join(transliterated_transcriptions))
    
