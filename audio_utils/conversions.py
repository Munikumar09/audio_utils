def sec_to_time(length: int) -> tuple[int, int, int]:
    """
    Convert seconds to hours, minutes, and seconds.

    Parameters
    ----------
    length: ``int``
        The length of the audio in seconds.

    Returns
    -------
    hours: ``int``
        The length of the audio in hours.
    mins: ``int``
        The length of the audio in minutes.
    seconds: ``int``
        The length of the audio in seconds.
    """
    
    hours = length // 3600  # calculate in hours
    length %= 3600
    mins = length // 60  # calculate in minutes
    length %= 60
    seconds = length  # calculate in seconds

    return hours, mins, seconds
