
from collections import namedtuple

Scan = namedtuple('Scan', [
    'id', 'name'
])

Chapter = namedtuple('Chapter', [
    'id', 'manga_id', 'name', 'number', 'uploads'
])

Chapters = namedtuple('Chapters', [
    'total', 'per_page', 'current_page', 'page_count', 'data'
])

Manga = namedtuple('Manga', [
    'id', 'type', 'score', 'name', 'synopsis', 'genders'
])

Mangas = namedtuple('Mangas', [
    'total', 'per_page', 'current_page', 'page_count', 'data'
])
