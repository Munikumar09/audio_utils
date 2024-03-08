from zspeech.audio.io import load_audio_using_stream_reader
from utils.file_utils import load_json
import torchaudio
import torch
from pathlib import Path
from tqdm import tqdm
import os
def convert_stereo_to_mono(input_file,output_dir):
    waveform, sample_rate = torchaudio.load(input_file)

    if waveform.shape[0]==2:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
        
    output_path=Path(output_dir)/Path(input_file).name
    
    torchaudio.save(output_path, waveform, sample_rate)

input_file=Path("/media/dataset-harddisk/munikumar/datasets/hindi_dataset/gramvaani/unlabelled/final")

output_dir=Path("/media/dataset-harddisk/munikumar/datasets/hindi_dataset/gramvaani/unlabelled/mono")
meta_file=Path("/media/dataset-harddisk/munikumar/datasets/hindi_dataset/gramvaani/unlabelled/audio_info.json")
audio_info=load_json(meta_file)
for audio_data in tqdm(audio_info):
    channels=audio_data["channels"]
    if channels==2:
        convert_stereo_to_mono(audio_data["audio_file"],output_dir)
    elif channels==1:
        os.system(f"cp {audio_data['audio_file']} {output_dir}")
    
