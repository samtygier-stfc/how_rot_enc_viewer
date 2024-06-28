from pathlib import Path

import numpy as np
from tifffile import tifffile
import skimage.io
from skimage.transform import resize

from config import CACHED_DIR, MAX_SIZE

if not CACHED_DIR.exists():
    CACHED_DIR.mkdir()


def imread(filename: Path) -> np.ndarray:
    if filename.suffix == '.tiff':
        try:
            data = tifffile.imread(filename)
        except tifffile.TiffFileError as e:
            raise RuntimeError(f"TiffFileError {e.args[0]}: {filename}") from e
    elif filename.suffix == '.png':
        data = skimage.io.imread(filename)

    if data.shape[0] > MAX_SIZE:
        data = resize(data, (MAX_SIZE, MAX_SIZE))

    if data.dtype == np.float32:
        data = data.astype(np.float16)

    return np.flip(data, axis=0)


def load_stack(directory: Path, name_pattern: str, start: int,
               stop: int) -> np.ndarray:
    indexes = range(start, stop)
    image_0 = imread(directory / name_pattern.format(indexes[0]))

    count = len(indexes)
    full_shape = [count, *image_0.shape]
    image_stack = np.zeros(full_shape, dtype=image_0.dtype)

    for n, i in enumerate(indexes):
        image_stack[n] = imread(directory / name_pattern.format(i))

    return image_stack


def load_stack_c(directory: Path, name_pattern: str, start: int,
                 stop: int) -> np.ndarray:
    cache_file = CACHED_DIR / (directory.name + '_' + name_pattern.format(0) +
                               ".npy")
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
