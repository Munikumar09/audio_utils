from pydub import AudioSegment
import mutagen
from pathlib import Path
from typing import Dict, List
from tqdm import tqdm
from audio_utils.common import resolve_path
import subprocess
import re
import json


def get_audio_info(audio_file: str | Path) -> Dict[str, str | int | float]:
    """
    Retrieves information about an audio file using ffprobe. The information contains the number of audio channels, the duration of the audio file, the sample rate, the codec used for encoding the audio, the bit depth of the audio file, and the bit rate of the audio file.

    Parameters
    ----------
    audio_file: ``str | Path``
        The path to the audio file for which to retrieve information.

    Returns
    -------
    audio_data: ``Dict[str, str | int | float]``
        The information about the audio file.
    """
    cmd = [
        "ffprobe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(audio_file),
    ]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, _ = p.communicate()

    audio_info = json.loads(out)
    sample_fmt = audio_info["streams"][0]["sample_fmt"]
    bit_depth = 0

    if sample_fmt == "fltp":
        bit_depth = 16
    elif sample_fmt == "s16":
        bit_depth = 16
    elif sample_fmt == "s32":
        bit_depth = 32

    bit_rate = audio_info["streams"][0].get("bit_rate", None)

    if bit_rate == None:
        bit_rate = audio_info["format"].get("bit_rate")
    if bit_rate != None:
        bit_rate = f"{int(bit_rate)//1000} kb/s"

    audio_data = {
        "audio_file": str(audio_file),
        "channels": audio_info["streams"][0]["channels"],
        "duration": audio_info["streams"][0]["duration"],
        "sample_rate": audio_info["streams"][0]["sample_rate"],
        "codec": audio_info["streams"][0]["codec_name"],
        "bit_depth or pcm ": bit_depth,
        "bit_rate": bit_rate,
    }

    return audio_data


def get_total_audio_info(audio_folder: List[str] | str | Path):
    """
    Retrieves audio information for all files in the specified folder.

    Parameters
    ----------
    audio_folder: ``List[str] | str | Path``
        The path to the folder containing the audio files for which to retrieve information.

    Returns
    -------
    audio_info: ``List[Dict[str, Union[str, int, float]]]``
        The information about the audio files in the folder.

    """
    audio_files = audio_folder

    if isinstance(audio_folder, str) or isinstance(audio_folder, Path):
        audio_folder = resolve_path(audio_folder)
        audio_files = list(Path(audio_folder).rglob("*"))

    audio_info = []

    for file in audio_files:
        info = get_audio_info(str(file))
        audio_info.append(info)

    return audio_info


def get_duration_ffprobe(file_path: str | Path) -> float:
    """
    Get the duration of an audio file using ffprobe.

    Parameters
    ----------
    file_path: ``str | Path``
        The path to the audio file for which to retrieve the duration.

    Returns
    -------
    duration: ``float``
        Duration of the audio file.
    """
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", str(file_path)]

    output = subprocess.check_output(cmd).decode("utf-8")
    duration = re.search(r"duration=(.+)", output).group(1)
    return float(duration)


def get_duration_mutagen(file_path: str | Path) -> float:
    """
    Get the duration of an audio file using mutagen.

    Parameters
    ----------
    file_path: ``str | Path``
        The path to the audio file for which to retrieve the duration.

    Returns
    -------
    duration: ``float``
        Duration of the audio file.
    """

    data = mutagen.File(file_path)
    duration = data.info.length
    return duration


def get_total_audio_duration(
    audio_path: str | Path | List[str], format: str = "wav"
) -> Dict[str, float]:
    """
    Get the duration of each audio file in the specified folder along with the total duration, the minimum duration, and the maximum duration.


    Parameters
    ----------
    audio_path: ``str | Path | List[str]``
        The path to the folder containing the audio files for which to retrieve the duration.
    format: ``str``, ( default = wav )
        The format of the audio files in the folder.

    Returns
    -------
    audio_file_duration: ``Dict[str, float]``
        The duration of each audio file in the folder along with the total duration, the minimum duration, and the maximum duration.
    """
    if not isinstance(audio_path, list):
        audio_path = resolve_path(audio_path)
        audio_path = list(Path(audio_path).rglob(f"*.{format}"))
    total_duration = 0
    min_duration = 1e10
    max_duration = 1e-10

    audio_file_duration = {}
    for file_path in tqdm(audio_path):

        if Path(file_path).suffix == ".m4a":
            duration = get_duration_ffprobe(str(file_path))
        else:
            duration = get_duration_mutagen(file_path)
        min_duration = min(min_duration, duration)
        max_duration = max(max_duration, duration)
        total_duration += duration
        audio_file_duration[file_path.name] = duration

    audio_file_duration["max_duration"] = max_duration
    audio_file_duration["min_duration"] = min_duration
    audio_file_duration["total_duration"] = total_duration
    return audio_file_duration


def convert_audio_format(src, dst, format="wav"):
    sound = AudioSegment.from_file(str(src))
    file_path = Path(dst) / f"{src.stem}.{format}"
    sound.export(file_path, format="wav")
