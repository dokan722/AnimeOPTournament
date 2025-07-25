from typing import List, Any
import requests
from utils import check_limit_and_wait, write_lines, separator, Colors, color_text


def get_al_id(resources: List[Any]) -> str | None:
    for r in resources:
        if r['site'] == 'AniList':
            return r['external_id']
    return None


per_page = 100
correlations = []
logs = []
url = 'https://api.animethemes.moe/anime?include=resources&page[number]={page}&page[size]={size}'


for i in range(1, 1000):
    r = requests.get(url.format(page=i, size=per_page))
    data = r.json()
    animes = data['anime']
    if len(animes) == 0:
        break
    for anime in animes:
        at_id = anime['id']
        al_id = get_al_id(anime['resources'])
        if not al_id:
            logs.append(f'Skipping {anime['name']} (slug: {anime['slug']} AnimeThemesId: {anime['id']}) id for AniList not found')
            print(color_text('Skipping {anime["title"]}', Colors.red))
            continue
        correlations.append(f'{at_id}{separator}{al_id}')
        print(anime['name'], ' added')

    print(color_text(f'Page {i} finished', Colors.green))
    check_limit_and_wait(r)



write_lines('correlations.txt', correlations)
write_lines('correlation_logs.txt', logs)


