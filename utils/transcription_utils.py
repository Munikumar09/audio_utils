from typing import Tuple
import re
from utils.file_utils import save_json
from utils.audio_utils import get_audio_info
from collections import Counter
from tqdm import tqdm
import json
_HINDI_NUKTAS_RE_PATTERN=r"[\u0929\u0931\u0958-\u095e]"
_NUKTA_SYMBOL="\u093c"

_HINDI_LANGUAGE_RE_PATTERN = r"[^\u0901-\u0903\u0905-\u090b\u090f-\u0911\u0913-\u0928\u092a-\u0930\u0932-\u0933\u0935-\u0939\u093c\u093e-\u0943\u0945\u0947-\u0949\u094b-\u094d\s]"
hindi_nuktas_decompose={
    "क़": "क" + _NUKTA_SYMBOL,
    "ख़": "ख" + _NUKTA_SYMBOL,
    "ग़": "ग" + _NUKTA_SYMBOL,
    "ज़": "ज" + _NUKTA_SYMBOL,
    "ड़": "ड" + _NUKTA_SYMBOL,
    "ढ़": "ढ" + _NUKTA_SYMBOL,
    "फ़": "फ" + _NUKTA_SYMBOL,
    "ऱ": "र" + _NUKTA_SYMBOL,
    "य़": "य" + _NUKTA_SYMBOL,
}

def clean_and_verify_transcript_hi(transcription: str) -> Tuple[str, bool]:
    """
    Clean and verify the given transcription based on the characters present in the transcription.
    If transcription contains only hindi characters then it is considered as valid otherwise invalid

    Parameters
    ----------
    transcription: ``str``
        Transcription text to validate

    Returns
    -------
    transcription: ``str``
        Cleaned and verified transcription
    check: ``bool``
        Describes whether the transcription is valid or not
    """
    transcription = re.sub(r"#[\w]*|<[\w]*>", "", transcription)
    # transcription=re.sub(_HINDI_NUKTAS_RE_PATTERN,lambda x: hindi_nuktas_decompose[x.group(0)],transcription)

    # Replacing one or more consecutive zero_width spaces or normal spaces to a single space
    transcription = re.sub(r"[\u200b\s]+", " ", transcription)

    # Searching for non hindi characters by using unicode's of hindi language
    check = re.findall(_HINDI_LANGUAGE_RE_PATTERN, transcription)

    return transcription, check


def get_transcription_info(transcription_data, audio_path, save_path, split_type):
    print(f"getting audio info about : {save_path.name} - {split_type}")
    non_hindi_chars = []
    non_hindi_transcriptions = {}
    total_duration = 0
    audio_data = []
    min_duration = 1e9
    max_duration = -1e9
    total_duration = 0
    total_loss_duration = 0
    total_file_count = 0
    loss_file_count = 0
    audio_file_duration = {}
    
    for audio_file, transcription in tqdm(transcription_data.items()):
        audio = audio_path / audio_file
        data = get_audio_info(str(audio))
        audio_data.append(data)
        duration = float(data["duration"])
        max_duration = max(duration, max_duration)
        min_duration = min(duration, min_duration)
        total_duration += duration
        audio_file_duration[audio.name] = duration
        clean_transcription, non_hindi_tokens = clean_and_verify_transcript_hi(
            transcription
        )
        total_file_count+=1
        if len(non_hindi_tokens) != 0:
            loss_file_count += 1
            non_hindi_transcriptions[audio_file] = {
                "raw_transcription": transcription,
                "clean_transcription": clean_transcription,
                "duration": duration,
                "non_hindi_chars": non_hindi_tokens,
            }
            total_loss_duration += duration

            non_hindi_chars.extend(non_hindi_tokens)

    audio_file_duration["max_duration"] = max_duration
    audio_file_duration["min_duration"] = min_duration
    audio_file_duration["total_duration"] = total_duration
    save_json(audio_data, save_path=save_path / f"{split_type}_info.json")
    save_json(audio_file_duration, save_path=save_path / f"{split_type}_duration.json")

    non_hindi_char_freq = dict(Counter(non_hindi_chars))
    non_hindi_transcriptions["total_audio_duration"] = total_duration
    non_hindi_transcriptions["loss_audio_duration"] = total_loss_duration
    non_hindi_transcriptions["total_file_count"] = total_file_count
    non_hindi_transcriptions["loss_file_count"] = loss_file_count
  
    save_json(
        non_hindi_transcriptions,
        save_path=save_path / f"{split_type}_non_hindi_transcripts.json",
        ensure_ascii=False,
    )
    save_json(
        non_hindi_char_freq,
        save_path=save_path / f"{split_type}_non_hindi_tokens.json",
        ensure_ascii=False,
    )


from utils.conversions import sec_to_time
def get_data_loss(total_duration,loss_duration,total_files,loss_files):
    h,m,s=sec_to_time(total_duration)
    print(f"Total duration : {int(h)}:{int(m)}:{int(s)}")
    h,m,s=sec_to_time(loss_duration)
    print(f"Loss duration : {int(h)}:{int(m)}:{int(s)}")
    h,m,s=sec_to_time(total_duration-loss_duration)
    print(f"Remaining duration : {int(h)}:{int(m)}:{int(s)}")
    print(f"Drop by percentage: {(loss_duration/total_duration)*100:.2f}")
    
    print(f"\nTotal audio files : {total_files}")
    print(f"Files that would be drop: {loss_files}")
    print(f"Remaining audio files : {total_files-loss_files}")
    print(f"Drop by percentage: {(loss_files/total_files)*100:.2f}")
    
    
def get_stats(transcription_path):
    with open(transcription_path, 'r',encoding='utf-8')as fp:
        data=json.load(fp)
    total_duration=data["total_audio_duration"]
    total_files=data["total_file_count"]
    total_loss_duration=data["loss_audio_duration"]
    total_loss_files=data["loss_file_count"]
    normalized_loss_files=0
    normalized_loss_duration=0
    non_hindi_tokens=[]
    for audio_file,info in data.items():
        if audio_file not in ["total_audio_duration","total_file_count","loss_file_count","loss_audio_duration"]:
            tokens=re.findall(r"[a-zA-Z0-9]+",info["clean_transcription"])
            non_hindi_tokens.extend(info["non_hindi_chars"])
            
            if len(tokens)!=0:
                normalized_loss_files+=1
                normalized_loss_duration+=info["duration"]
    print('*'*50)
    print("Loss of audio data without transcription normalization:")
    print("*"*50)
    get_data_loss(total_duration,total_loss_duration,total_files,total_loss_files)
    # print("\n\n")
    # print('*'*50)
    # print("Loss of audio data with transcription normalization:")
    # print('*'*50)
    # get_data_loss(total_duration,normalized_loss_duration,total_files,normalized_loss_files)
    # print("\n\n")
    # print('*'*50)
    # print("Difference between without transcription normalized data and with transcription normalized data")
    # print('*'*50)
    # h,m,s=sec_to_time(total_loss_duration-normalized_loss_duration)
    # print(f"Audio duration difference : {int(h)}:{int(m)}:{int(s)}")
    # print(f"Audio duration difference in percentage: {((total_loss_duration-normalized_loss_duration)/total_duration)*100:.2f}")
    # print(f"Audio file difference : {total_loss_files-normalized_loss_files}")
    # print(f"Audio file difference in percentage: {((total_loss_files-normalized_loss_files)/total_files)*100:.2f}")
    
    print("*"*50)
    print(f"Non hindi tokes : {sorted(list(set(non_hindi_tokens)))}")
    
def load_json_data(file_path):
    with open(file_path,'r')as fp:
        data=json.load(fp)
    return[ data["total_audio_duration"],
    data["loss_audio_duration"],
    data["total_file_count"],
    data["loss_file_count"]]
def get_total_stats(dataset_dir):
    train_file=dataset_dir/"train_non_hindi_transcripts.json"
    dev_file=dataset_dir/"dev_non_hindi_transcripts.json"
    test_file=dataset_dir/"test_non_hindi_transcripts.json"
    train_stats=load_json_data(train_file)
    dev_stats=load_json_data(dev_file)
    test_stats=load_json_data(test_file)
    total_stats=[train_stats,dev_stats,test_stats]
    new_stats=[sum(column) for column in zip(*total_stats)]
    print('*'*50)
    print("Loss of audio data for total dataset:")
    print("*"*50)
    get_data_loss(new_stats[0],new_stats[1],new_stats[2],new_stats[3],)
        
    
    