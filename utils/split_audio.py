from pathlib import Path
import torchaudio

from tqdm import tqdm
from zspeech.inference import ZSpeech
from zspeech.preprocessing.utils import replace_special_characters as re_sp
from zspeech.audio.data_instance.vad import VADDataInstance,VADAudioInstance
from typing import Union

import numpy as np
from os.path import exists
from zspeech.preprocessing.utils import replace_special_characters

INPUT_FORMAT = "mp3"
OUT_FORMAT = "wav"
SPLIT_THRESHOLD = 60
INPUT_AUDIO_PATH = Path("/data1/muni/datasets/hindi/yt_data/temp")
OUTPUT_AUDIO_PATH = Path("/data1/muni/datasets/hindi/yt_data/temp_split_60")
np_float32: np.dtype = np.dtype("float32")
OUTPUT_SAMPLE_RATE = 16000


def create_dir(dir_name: Union[str, Path], create_sub_dirs: bool = True):
    """
    Create a new directory if it's not present

    Parameters
    ----------
    dir_name: ``str``
        Directory name to be created
    create_sub_dirs: ``bool``
        Flag denotes whether to create sub directories or not
    """

    if isinstance(dir_name, str):
        dir_name = Path(dir_name)

    if not dir_name.exists():
        print(f"####\t creating {dir_name} \t####")
        dir_name.mkdir(parents=create_sub_dirs)


def save_vad_segments(vad_output, audio_file_path, output_path, use_vad=False):
    try:
        sample_rate = torchaudio.info(audio_file_path).sample_rate
        audio, out_sample_rate = torchaudio.load(
            audio_file_path,
            format=INPUT_FORMAT,
            normalize=False,
            frame_offset=0,
            num_frames=-1,
        )

        for vad_segment in vad_output:
            try:
                out_file_path = (
                    output_path
                    / f"{audio_file_path.stem}_st_{re_sp(str(vad_segment.start))}.{OUT_FORMAT}"
                )

                if use_vad:
                    audio_input = vad_segment.audio_segment.reshape(
                        1, len(vad_segment.audio_segment)
                    )
                    torchaudio.save(
                        filepath=out_file_path,
                        src=audio,
                        sample_rate=16000,
                        format=OUT_FORMAT,
                    )
                else:
                    start_time = vad_segment.start
                    duration = vad_segment.segment_colln.duration
                    end_time = vad_segment.start + duration
                    start_idx, end_idx = (
                        int(start_time * sample_rate),
                        int(end_time * sample_rate),
                    )

                    output_filename = f"{audio_file_path.stem}_{start_time}_{end_time}"
                    output_filename = replace_special_characters(output_filename)
                    # print(f"audio file path : {audio_file_path.stem}")
                    # output_dir=output_path/audio_file_path.stem
                    # create_dir(output_dir)
                    target_audio_filepath = (
                        f"{str(output_path/ output_filename)}.{OUT_FORMAT}"
                    )
                    # print('target_audio path ',target_audio_filepath)
                    # sf.write(target_audio_filepath, audio_file[start_idx:end_idx], sample_rate,  format='mp3')
                    # audio = torch.from_numpy(
                    #    audio_file[start_idx:end_idx].reshape(1, len(audio_file[start_idx:end_idx]))
                    # )
                    if exists(target_audio_filepath):
                        continue
                    torchaudio.save(
                        filepath=target_audio_filepath,
                        src=audio[:, start_idx:end_idx],
                        sample_rate=out_sample_rate,
                        format=OUT_FORMAT,
                    )
            except Exception as ex:
                print(f"exception : {ex}")
    except Exception as ex:
        print(f"exception : {ex}")


"""
        out_file_path = str(out_file_path)
        # audio = vad_segment.audio_segment
        if FORMAT=='opus':
            convert_to_opus(vad_segment.audio_segment.tobytes(), out_file_path)
        else:
            audio = torch.from_numpy(
                vad_segment.audio_segment.reshape(1, len(vad_segment.audio_segment))
            )
            torchaudio.save(
                filepath=out_file_path,
                src=audio,
                sample_rate=16000,
                format=INPUT_FORMAT,
            )

        # sf.write(file=out_file_path, data = audio, samplerate=16000, format="WAV", subtype="PCM_16")
"""


def remove_noice_and_save_vad_segments(vad_output, audio_file_path, output_path):
    sample_rate = torchaudio.info(audio_file_path).sample_rate
    audio, out_sample_rate = torchaudio.load(
        audio_file_path,
        format=INPUT_FORMAT,
        normalize=False,
        frame_offset=0,
        num_frames=-1,
    )

    for vad_segment in vad_output:
        out_file_path = (
            output_path
            / f"{audio_file_path.stem}_{re_sp(str(vad_segment.start))}.{INPUT_FORMAT}"
        )
        start_time = vad_segment.start
        duration = vad_segment.segment_colln.duration
        end_time = vad_segment.start + duration

        output_filename = f"{audio_file_path.stem}_{start_time}_{end_time}"
        output_filename = replace_special_characters(output_filename)
        target_audio_filepath = f"{str(output_path / output_filename)}.{INPUT_FORMAT}"

        start_time = vad_segment.start
        prev_end = -1
        for sub_segment in vad_segment.segment_colln.segments_list:

            if sub_segment.activity == 0 and sub_segment.duration > 1:
                duration = duration - sub_segment.duration
                if prev_end != -1:
                    save_audio_segement(
                        audio,
                        output_path,
                        audio_file_path,
                        out_sample_rate,
                        1,
                        start_time,
                        prev_end,
                    )
                save_audio_segement(
                    audio,
                    output_path,
                    audio_file_path,
                    out_sample_rate,
                    0,
                    sub_segment.start,
                    sub_segment.end,
                )
                start_time = -1

            else:
                if start_time == -1:
                    start_time = sub_segment.start
                prev_end = sub_segment.end
        if start_time != -1:
            save_audio_segement(
                audio,
                output_path,
                audio_file_path,
                out_sample_rate,
                1,
                start_time,
                prev_end,
            )


def save_audio_segement(
    audio, output_path, audio_file_path, out_sample_rate, activity, start_time, end_time
):

    start_idx, end_idx = (
        int(start_time * out_sample_rate),
        int(end_time * out_sample_rate),
    )
    duration = end_time - start_time

    voice_selected_path = output_path / f"{'voice_selected'}"
    voice_rejected_path = output_path / f"{'voice_rejected'}"
    no_voice_path = output_path / f"{'no_voice'}"

    if activity == 0:
        output_path = no_voice_path
    elif duration < 5:
        output_path = voice_rejected_path
    else:
        output_path = voice_selected_path

    create_dir(output_path)

    output_filename = f"{audio_file_path.stem}_{start_time}_{end_time}"
    output_filename = replace_special_characters(output_filename)
    target_audio_filepath = f"{str(output_path / output_filename)}.{INPUT_FORMAT}"

    torchaudio.save(
        filepath=target_audio_filepath,
        src=audio[:, start_idx:end_idx],
        sample_rate=out_sample_rate,
        format=INPUT_FORMAT,
    )


def save_stereo_audio_as_separate_channel(audio_file_path):
    audio, out_sample_rate = torchaudio.load(
        audio_file_path,
        format=INPUT_FORMAT,
        normalize=False,
        frame_offset=0,
        num_frames=-1,
    )
    output_filename_1 = f"{audio_file_path.stem}_1"
    output_filename_1 = replace_special_characters(output_filename_1)
    target_audio_filepath_1 = f"{str(OUTPUT_AUDIO_PATH / output_filename_1)}.{INPUT_FORMAT}"
    output_filename_2 = f"{audio_file_path.stem}_2"
    output_filename_2 = replace_special_characters(output_filename_2)
    target_audio_filepath_2 = f"{str(OUTPUT_AUDIO_PATH / output_filename_2)}.{INPUT_FORMAT}"

    if not exists(target_audio_filepath_1):
        torchaudio.save(
            filepath=target_audio_filepath_1,
            src=audio[0:1, :],
            sample_rate=out_sample_rate,
            format=INPUT_FORMAT,
        )
    if not exists(target_audio_filepath_2):
        torchaudio.save(
            filepath=target_audio_filepath_2,
            src=audio[1:2, :],
            sample_rate=out_sample_rate,
            format=INPUT_FORMAT,
        )


def slice_audio_with_vad(zs_client, audio_file_path):
    vad_instance = VADAudioInstance(source_filepath=str(audio_file_path))
    vad_output = zs_client.split_audio(vad_instance, SPLIT_THRESHOLD)
    save_vad_segments(vad_output, audio_file_path, OUTPUT_AUDIO_PATH)


def slice_audio_with_vad_and_remove_silence(zs_client, audio_file_path):
    try:
        vad_instance = VADDataInstance(source_filepath=str(audio_file_path))
        vad_output = zs_client.split_audio(vad_instance, 15)
        remove_noice_and_save_vad_segments(vad_output, audio_file_path, OUTPUT_AUDIO_PATH)
    except Exception as ex:
        print(audio_file_path)


def check_if_already_exists(src_audio_file_path, output_file_list):
    for output_file in output_file_list:
        if replace_special_characters(
            src_audio_file_path.stem
        ) in replace_special_characters(output_file.stem):
            return True
    return False


if __name__ == "__main__":
    zs_client = ZSpeech.load()

    input_audio_files = sorted(list(INPUT_AUDIO_PATH.glob(f"*.{INPUT_FORMAT}")))

    create_dir(OUTPUT_AUDIO_PATH)

    output_file_list = list(OUTPUT_AUDIO_PATH.glob(f"*.{INPUT_FORMAT}"))
    for audio_file_path in tqdm(input_audio_files):
        if not check_if_already_exists(audio_file_path, output_file_list):
            slice_audio_with_vad(zs_client, audio_file_path)
