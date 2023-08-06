from utils.media_utils import get_total_audio_duration
from utils.file_utils import save_json,get_audio_exceeds_length,get_total_duration
from utils.conversions import sec_to_time

if __name__=="__main__":
    audio_path="/media/dataset-harddisk/munikumar/hindi_dataset/benchmarks/ekstep/benchmark/Hindi_benchmarking_dataset_external_21-03-2022_06-46"
    audio_format="wav"
    save_path="/media/dataset-harddisk/munikumar/hindi_dataset/benchmarks/ekstep/meta/duration/hindi_benchmarking.json"
    exceed_path="/media/dataset-harddisk/munikumar/hindi_dataset/benchmarks/ekstep/meta/duration/hindi_benchmarking_exceed.json"
    # duration=get_total_audio_duration(audio_path,audio_format)
    # print(f'total duration : {sec_to_time(duration["total_duration"])}')
    # duration=get_audio_exceeds_length(save_path,30.0)
    # save_json(duration,exceed_path)
    total_duration=get_total_duration(exceed_path)
    print(f'total duration : {sec_to_time(total_duration)}')
    