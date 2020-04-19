from typing import List, TextIO


def parse_ints(io: TextIO) -> List[int]:
    """Parse first line of io to list of integers.

    Parameters
    ----------
    io :: TextIO
        Object supporting `readline()`

    Returns
    -------
    integers :: List[int]
        A list of integers

    Examples
    --------
    >>> data = StringIO("1 2 3 4")
    >>> parse_ints(data)
    [1, 2, 3, 4]
    """
    line = io.readline()
    line = line.strip()
    parts = line.split(" ")
    ints = map(int, parts)
    return list(ints)


def parse_floats(io: TextIO) -> List[float]:
    """Parse first line of io to list of floats.

    Parameters
    ----------
    io :: TextIO
        Object supporting `readline()`

    Returns
    -------
    floats :: List[float]
        A list of floats

    Examples
    --------
    >>> data = StringIO("1.1 2.2 3.3 4.4")
    >>> parse_floats(data)
    [1.1, 2.2, 3.3, 4.4]
    """
    line = io.readline()
    line = line.strip()
    parts = line.split(" ")
    ints = map(float, parts)
    return list(ints)
