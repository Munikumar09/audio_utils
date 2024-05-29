from audio_utils.file_utils import load_json
from collections import OrderedDict
from copy import deepcopy
from typing import Dict

def convert_to_time(audio_length:str):
    if "days" not in audio_length:
        return audio_length
    days,time=[ele.strip()for ele in audio_length.split(",")]
    days=days.split(" ")[0].strip()
    days_in_hrs=int(days)*24
    hours=int(time.split(":")[0].strip())
    return str(days_in_hrs+hours)+":"+":".join(time.split(":")[1:])

def add_audio_length(audio_length1:str,audio_length2:str):

    audio_length1=convert_to_time(audio_length1)
    audio_length2=convert_to_time(audio_length2)
    
    total_length=[float(a)+float(b) for a,b in zip(audio_length1.split(":"),audio_length2.split(":"))]
    time_format=[]
    carry=0
    for time in reversed(total_length[1:]):
        total_time=time+carry
        time_format.insert(0,total_time%60)
        carry=total_time//60
    hrs=total_length[0]+carry
    m,s= time_format
    h=hrs%24
    days=""
    if hrs>=24:
        days=str(hrs//24)+" days, "
        
    total_audio_length=f"{days}{int(h)}:{int(m)}:{s:.6f}"
    return total_audio_length

def add_dictionaries(d1:Dict[str,int],d2:Dict[str,int]):
    if len(d1)==0:
        return d2
    if len(d2)==0:
        return d1
    merge_dict=deepcopy(d1)
    for key,value in d2.items():
        if key in merge_dict:
            
            merge_dict[key]+=value
        else:
            merge_dict[key]=value
    return merge_dict

def merge_json_files(file1_path,file2_path):
    file1_data=load_json(file1_path)
    file2_data=load_json(file2_path)
    merge_data=OrderedDict()
    merge_data["total_count"]=file1_data["total_count"]+file2_data["total_count"]
    merge_data["dev_count"]=file1_data["dev_count"]+file2_data["dev_count"]
    merge_data["test_count"]=file1_data["test_count"]+file2_data["test_count"]
    merge_data["train_count"]=file1_data["train_count"]+file2_data["train_count"]
    merge_data["total_audio_length"]=add_audio_length(file1_data["total_audio_length"],file2_data["total_audio_length"])
    merge_data["total_audio_length_seconds"]=float(file1_data["total_audio_length_seconds"])+float(file2_data["total_audio_length_seconds"])

    merge_data["dev_audio_length_seconds"]=file1_data["dev_audio_length_seconds"]+file2_data["dev_audio_length_seconds"]
    merge_data["test_audio_length_seconds"]=file1_data["test_audio_length_seconds"]+file2_data["test_audio_length_seconds"]
    merge_data["avg_audio_length"]=str((float(file1_data["avg_audio_length"][:-1])+float(file2_data["avg_audio_length"][:-1]))/2)+"s"
    merge_data["total_transcription_word_count"]=file1_data["total_transcription_word_count"]+file2_data["total_transcription_word_count"]
    merge_data["avg_transcription_word_count"]=(file1_data["avg_transcription_word_count"]+file2_data["avg_transcription_word_count"])/2
    merge_data["total_transcription_length"]=file1_data["total_transcription_length"]+file2_data["total_transcription_length"]
    merge_data["avg_transcription_length"]=(file1_data["avg_transcription_length"]+file2_data["avg_transcription_length"])/2
    merge_data["min_audio_length"]=str(min(float(file1_data["min_audio_length"][:-1]),float(file2_data["min_audio_length"][:-1])))+"s"
    merge_data["max_audio_length"]=str(max(float(file1_data["max_audio_length"][:-1]),float(file2_data["max_audio_length"][:-1])))+"s"
    merge_data["min_transcription_length"]=min(file1_data["min_transcription_length"],file2_data["min_transcription_length"])
    merge_data["max_transcription_length"]=max(file1_data["max_transcription_length"],file2_data["max_transcription_length"])
    merge_data["min_transcription_word_count"]=min(file1_data["min_transcription_word_count"],file2_data["min_transcription_word_count"])
    merge_data["max_transcription_word_count"]=max(file1_data["max_transcription_word_count"],file2_data["max_transcription_word_count"])

    merge_data["language"]=add_dictionaries(file1_data["language"],file2_data["language"])
    merge_data["dialect"]=add_dictionaries(file1_data["dialect"],file2_data["dialect"])
    merge_data["gender"]=add_dictionaries(file1_data["gender"],file2_data["gender"])

    merge_data["age"]= {}
    merge_data["speakers"]= {}
    merge_data["noise_type"]= {}
    merge_data["snr"]= {}
    merge_data["original_samplerate"]= {}
    merge_data["dnsmos"]= {}
    merge_data["empty_transcription"]= {}
    merge_data["ekstep"]=merge_data["total_count"]
    return dict(merge_data)

def get_avg_bitrate(data):
    if isinstance(data,str):
        data=load_json(data)
    bitrate=0
    for audio_info in data:
        bitrate+=int(audio_info["bit_rate"].split(" ")[0])
    return f"{bitrate/len(data)} kb/s"