import cv2.cv2 as cv2
from pathlib import Path
import numpy as np
from pdf2image import convert_from_path, convert_from_bytes


def pdf2numpy(path: [Path, bytes, str], size=(1200, 2000), first_page=None,
              last_page=None) -> list[np.array]:
    """
    Convert pdf to numpy array
    """
    images = []
    if isinstance(path, str): path = Path(path)
    if isinstance(path, Path):
        if path.suffix == '.pdf':
            images = convert_from_path(
                pdf_path=path,
                size=size,
                first_page=first_page,
                last_page=last_page
            )
    elif isinstance(path, bytes):
        images = convert_from_bytes(path, size=size, first_page=first_page, last_page=last_page)
    return [cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) for image in images]
