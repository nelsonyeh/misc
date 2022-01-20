def bytes2human(size, precision=2, max_unit='TB'):
    """
    Parameters:
        size: Size in bytes (integer).
        precision: Convert floating point number to a certain precision.
        max_unit: Specify the max unit. e.g. 'MB'
    Returns:
        (size, unit), tuple format. e.g. (1.0, 'GB')
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    suffixIndex = 0
    while size >= 1024 and suffixIndex < suffixes.index(max_unit):
        suffixIndex += 1
        size = size / 1024.0
    return (round(size, precision), suffixes[suffixIndex])
