"""Api core"""

import ast
from operator import itemgetter

import requests

from vimanga.api.constants import (
    HEADERS, API_URL, MANGA_URL, CAPS_URL, IMAGES_SERVER
)
from vimanga.api.types import (
    Mangas, Manga, Chapter, Chapters, Scan
)


def call_api(url=API_URL, **params):
    """Call api and set default header"""
    return requests.get(url,
                        params=params,
                        headers=HEADERS)


def get_mangas(search='',
               categories=None,
               default=1,
               genders=None,
               per_page=10,
               page=1,
               score=0,
               search_by='nombre',
               sort_dir='asc',
               sorted_by='nombre',
               **params):
    """Get all filters mangas"""
    current_page = 0
    page_count = 1

    while current_page <= page_count:
        _params = {
            'categorias': categories or [],
            'defecto': default,
            'generos': genders or [],
            'itemsPerPage': int(per_page),
            'nameSearch': search,
            'page': int(page),
            'puntuacion': score,
            'searchBy': search_by,
            'sortDir': sort_dir,
            'sortedBy': sorted_by,
            **params
        }
        response = call_api(API_URL, **_params).json()
        current_page = response['current_page']
        page_count = response['last_page']

        data = [
            Manga(id=manga['id'],
                  type=manga['tipo'],
                  score=manga['puntuacion'],
                  name=manga['nombre'],
                  synopsis=manga['info']['sinopsis'],
                  genders=list(map(itemgetter('genero'), manga['generos'])))
            for manga in response['data']
        ]

        mangas = Mangas(
            total=response['total'],
            per_page=response['per_page'],
            current_page=current_page,
            page_count=page_count,
            data=data
        )

        page += 1
        yield mangas


def get_chapters(manga, page=1):
    """Get all chapters from a manga"""
    current_page = 0
    page_count = 1

    while current_page <= page_count:
        response = call_api(MANGA_URL.format(manga.id), page=int(page)).json()
        current_page = response['current_page']
        page_count = response['last_page']

        data = []

        for chapter in response['data']:
            uploads = []
            for upload in chapter['subidas']:
                uploads.append(Scan(
                    id=upload['idScan'],
                    name=upload['scanlation']['nombre']
                ))

            data.append(Chapter(
                id=chapter['id'],
                name=chapter['nombre'],
                manga_id=chapter['tomo']['idManga'],
                number=chapter['numCapitulo'],
                uploads=uploads
            ))

        chapters = Chapters(
            total=response['total'],
            per_page=response['per_page'],
            current_page=current_page,
            page_count=page_count,
            data=data
        )

        page += 1
        yield chapters


def get_images(chapter, scan=0):
    """Get a provide chapter"""
    scanlation = chapter.uploads[scan]
    _params = {
        'idManga': chapter.manga_id,
        'idScanlation': scanlation.id,
        'numeroCapitulo': chapter.number
    }

    response = call_api(CAPS_URL, **_params).json()
    images = response['imagenes']
    images = ast.literal_eval(images)
    params = {
        'manga': chapter.manga_id,
        'scan': scanlation.id,
        'chapter': chapter.number,
    }

    for image in images:
        yield IMAGES_SERVER.format(image=image, **params)
