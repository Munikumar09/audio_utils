from pydub import AudioSegment

def get_audio_info(audio_file):
    data=AudioSegment.from_file(str(audio_file))
    channels=data.channels
    duration=data.duration_seconds
    frame_count=data.frame_count()
    sample_rate=data.frame_rate
    frame_width=data.frame_width
    sample_width=data.sample_width
    bit_depth=data.sample_width*8
    bit_rate=sample_rate*channels*bit_depth
    audio_data={
    "channels": channels,
    "duration": duration,
    "frame_count": frame_count,
    "sample_rate": sample_rate,
    "frame_width": frame_width,
    "sample width ": sample_width,
    "bit_depth or pcm ": bit_depth,
    "bit_rate": bit_rate,
    }
    return audio_data