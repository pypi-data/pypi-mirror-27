import os
"""
Module for simple directory based functions
"""

def list_files(directory=os.getcwd(), file_extension=None, return_full_path=True):
    """
    List all files contained in a directory
    
    Usage:
    list_files(directory=os.getcwd(), file_extension=None, return_full_path=True)

    Input arguments:
    - directory (default=os.getcwd()): full directory path
    - file_extension (default=None): filter by file extension
    - return_full_path (default=True): full path of files (True) or relative
    """
    
    filelist = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    if file_extension is not None:
        filelist = [f for f in filelist if f.endswith('.'+file_extension)]

    if return_full_path:
        filelist = [os.path.join(directory, f) for f in filelist]

    filelist.sort()

    return filelist


def list_dirs(directory=os.getcwd(), return_full_path=True):
    """
    List all directories contained in a directory
    
    Usage:
    list_files(directory=os.getcwd(), file_extension=None, return_full_path=True)

    Input arguments:
    - directory (default=os.getcwd()): full directory path
    - file_extension (default=None): filter by file extension
    - return_full_path (default=True): full path of files (True) or relative
    """

    dirlist = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    if return_full_path:
        dirlist = [os.path.join(directory, d) for d in dirlist]

    dirlist.sort()

    return dirlist


def list_records(directory=os.getcwd(), return_full_path=True):
    """
    List all wfdb records in a directory (by finding header files).
    Wraps around list_files with .hea extension.
    
    Usage:
    list_records(directory=os.getcwd(), return_full_path=True)
    """

    filelist = list_files(directory=directory, file_extension='hea', return_full_path=return_full_path)
    recordlist = [f.split('.hea')[0] for f in filelist]

    recordlist.sort()

    return recordlist


def cat(file):
    """
    Print the contents of a file. Just like unix cat.
    """
    with open(file) as f:
        print(f.read())

    return


def read_lines(file, strip=True):
    """
    Read lines of a file into a list

    Input arguments:
    - strip (defualt=True): remove leading/trailing whitespaces and newlines
    """
    with open(file) as f:
        lines = f.readlines()
    if strip:
        lines = [l.strip() for l in lines]

    return lines


def dir_size(path, readable=False, walk=True):
    """
    Recursive size of a directory in bytes
    Like du -s with default options.
    Or just get size of local files with walk=False

    Input arguments:
    - readable (default=False): If False, return number of bytes. If True,
      return (size, units)
    - walk (default=True): If true, crawls subdirectories like du -sh.
      Otherwise only lists size of contents in immediate directory
    """
    total_size = 0

    if walk:
        for dirpath, dirnames, filenames in os.walk(path):
            for fname in filenames:
                file = os.path.join(dirpath, fname)
                total_size += os.path.getsize(file)
    else:
        total_size = sum([os.path.getsize(file) for file in list_files(path)])

    if readable:
        return readable_size(total_size)
    else:
        return total_size


# File/folder size functions
allowed_units = ['K','M','G','T']
unit_factor = dict(zip(allowed_units, [1024**i for i in range(1, len(allowed_units)+1)]))


def convert_size(nbytes, unit):
    """
    Convert number of bytes to another unit. kb, mb, gb ,tb.
    """
    if unit not in allowed_units:
        raise ValueError('units must be one of the following:', allowed_units)

    return nbytes / unit_factor[unit]


def readable_size(nbytes):
    """
    Get readable size. Returns number of _bytes, and the units.
    ie. readable_size(1024) == (1, 'K')
    """
    if nbytes < 1024:
        return nbytes, ''

    for unit in allowed_units:
        nunits = convert_size(nbytes, unit)
        if nunits < 1024:
            return nunits, unit

    raise ValueError('Size is beyond terrabytes?')
