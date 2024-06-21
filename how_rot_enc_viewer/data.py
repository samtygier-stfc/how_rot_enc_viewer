from pathlib import Path

import numpy as np
from tifffile import tifffile


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
