"""Utilities functions"""

import os
from multiprocessing.dummy import Pool
from tempfile import NamedTemporaryFile
import requests
from tqdm import tqdm

from vimanga.api.core import get_images


def download_image(info):
    """Download and convert image"""
    index, link = info
    success = False

    while not success:
        data = requests.get(link)
        success = data.ok

    return index, data.content


def download_chapter(chapter,
                     threads=4,
                     progress=None,
                     scan=0,
                     **kwargs):
    """Return a list of images bytes with chapter"""
    link_list = list(get_images(chapter, scan))
    enumerate_links = enumerate(link_list)

    pool = Pool(processes=threads)
    wrapper = progress or tqdm

    generator = wrapper(
        pool.imap_unordered(download_image, enumerate_links),
        desc=f'Capitulo {chapter.number}',
        total=len(link_list),
        **kwargs
    )

    return chapter, sorted((index, image) for index, image in generator)


def convert_to_pdf(name: str, images: list, directory='.'):
    """Convert a list of images in pdf"""
    try:
        from PIL import Image
        from reportlab.pdfgen.canvas import Canvas
    except ImportError:
        raise ImportError('Reportlab is required for convert to pdf')

    filename = os.path.join(directory, name)
    os.makedirs(directory, exist_ok=True)

    canva = Canvas(filename)
    for _, image in images:
        with NamedTemporaryFile(mode='wb') as tmp_image:
            tmp_image.write(image)
            img = Image.open(tmp_image.name)
            canva.setPageSize(img.size)
            canva.drawImage(tmp_image.name, 0, 0)
            canva.showPage()

    canva.save()


def convert_to_images(name: str, folder: str, images: list, directory='.'):
    """Convert to a folder of images"""
    folder = os.path.join(directory, folder)
    os.makedirs(folder, exist_ok=True)

    for idx, image in images:
        filename = os.path.join(folder, name.format(idx))
        with open(filename, 'wb') as file:
            file.write(image)
