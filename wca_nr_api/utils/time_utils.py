def centiseconds_to_time(time: int) -> str:
    """
    Converts centiseconds to time in format minutes:seconds.centiseconds.
    Omits the digit for minutes if the time is under 1 minute.
    Omits the digit for minutes and the first digit for seconds if the time is under 10 seconds.

    :param time: (int) The centiseconds.
    :return: (str) The formatted time.
    """

    # Calculate minutes
    minutes = time // 6000
    # Calculate seconds
    seconds = (time % 6000) // 100
    # Calculate centiseconds
    centiseconds = time % 100
    # Different format based on time
    if minutes == 0:
        if seconds < 10:
            return f"{seconds:01}.{centiseconds:02}"
        return f"{seconds:02}.{centiseconds:02}"
    return f"{minutes}:{seconds:02}.{centiseconds:02}"
