from pathlib import Path

import numpy as np
from tifffile import tifffile

from config import CACHED_DIR

if not CACHED_DIR.exists():
    CACHED_DIR.mkdir()


def imread(filename: Path) -> np.ndarray:
    try:
        return tifffile.imread(filename)
    except tifffile.TiffFileError as e:
        raise RuntimeError(f"TiffFileError {e.args[0]}: {filename}") from e


def load_stack(directory: Path, name_pattern: str, start: int,
               stop: int) -> np.ndarray:
    indexes = range(start, stop)
    image_0 = imread(directory / name_pattern.format(indexes[0]))

    count = len(indexes)
    width, height = image_0.shape
    image_stack = np.zeros((count, height, width), dtype=image_0.dtype)

    for i in indexes:
        image_stack[i] = imread(directory / name_pattern.format(i)).T[:, ::-1]

    return image_stack


def load_stack_c(directory: Path, name_pattern: str, start: int,
                 stop: int) -> np.ndarray:
    cache_file = CACHED_DIR / (name_pattern.format(0) + ".npy")
    if not cache_file.exists():
        data = load_stack(directory, name_pattern, start, stop)
        #data = data.astype(np.float16)
        data = convert_to_uint8(data)
        np.save(cache_file, data)
        print(f"Wrote {cache_file}")
    else:
        data = np.load(cache_file, mmap_mode='r')
        print(f"Read {cache_file}")
    return data


def convert_to_uint8(array: np.ndarray) -> np.ndarray:
    min, max = array.min(), array.max()
    print(f"Min: {min}, Max: {max}")
    data = (array - min) / (max - min) * 255
    print(f"after Min: {data.min()}, Max: {data.max()}")
    return data.astype(np.uint8)
