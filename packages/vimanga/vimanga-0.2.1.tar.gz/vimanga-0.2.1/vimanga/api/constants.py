"""Contansts api"""

HEADERS = {
    'Host': 'www.tumangaonline.com',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-VE,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Cache-mode': 'no-cache',
    'Referer': 'https://www.tumangaonline.com/biblioteca'
}
BASE_URL = 'https://www.tumangaonline.com/api/v1/'
API_URL = BASE_URL + 'mangas'
CAPS_URL = BASE_URL + 'imagenes'

MANGA_URL = API_URL + '/{}/capitulos'
IMAGES_SERVER = (
    'https://img1.tumangaonline.com/subidas/{manga}/{chapter}/{scan}/{image}'
)
