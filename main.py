from utils.media_utils import get_total_audio_duration
from utils.file_utils import save_json
from utils.conversions import sec_to_time

if __name__=="__main__":
    audio_path="/home/munikumar-17774/Desktop/audio/cv-corpus-13.0-2023-03-09/hi/clips"
    audio_format="mp3"
    save_path="/home/munikumar-17774/Desktop/python_improve/audio_utils/data/duration_data/common_voice_total.json"
    duration=get_total_audio_duration(audio_path,audio_format)
    print(f'total duration : {sec_to_time(duration["total_duration"])}')
    save_json(duration,save_path)
    
    