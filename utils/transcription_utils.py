from typing import Tuple
import re
_HINDI_LANGUAGE_RE_PATTERN = r"[^\u0901-\u0903\u0905-\u090b\u090f-\u0911\u0913-\u0928\u092a-\u0930\u0932-\u0933\u0935-\u0939\u093c\u093e-\u0943\u0945\u0947-\u0949\u094b-\u094d\s]"

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

    # Replacing one or more consecutive zero_width spaces or normal spaces to a single space
    transcription = re.sub(r"[\u200b\s]+", " ", transcription)

    # Searching for non hindi characters by using unicode's of hindi language
    check = re.findall(_HINDI_LANGUAGE_RE_PATTERN, transcription)

    return transcription, check