from typing import Any
import requests

from data_collection.data_loader import get_correlations, get_top_animes
from data_collection.utils import color_text, Colors
from utils import check_limit_and_wait, write_lines, separator


def get_best_resolution(opening: Any) -> str:
    try:
        chosen = opening['animethemeentries'][0]['videos'][0]
        max_res = chosen['resolution']
        for video in opening['animethemeentries'][0]['videos']:
            if video['resolution'] > max_res:
                max_res = video['resolution']
                chosen = video

        return chosen['link']
    except:
        return None


animethemes_url = "https://api.animethemes.moe/anime/"

correlations = get_correlations()
animes = get_top_animes()
num_animes = len(animes)
added_animes = set()
opening_entries = []
logs = []

xd='xd'

for i, anime in enumerate(animes):
    al_id = anime.AniListID
    if al_id not in correlations:
        msg = f'Anime {anime.Name} (al_id: {al_id}) not found in correlations '
        print(color_text(msg, Colors.red))
        logs.append(msg)
        continue
    at_slug = correlations[al_id]
    if al_id in added_animes:
        continue

    full_url = f'{animethemes_url}{at_slug}'
    response = requests.get(full_url, params={'include': 'animethemes.animethemeentries.videos,animethemes.song.artists'})

    if response.status_code != 200:
        msg = str(['Failed to fetch page ', anime.Name, '(al_id:', str(al_id), ' at_slug:', str(at_slug) + ') error: ', response.status_code])
        logs.append(msg)
        print(color_text(msg, Colors.red))
        continue

    anime_data = response.json()
    openings = [x for x in anime_data['anime']['animethemes'] if x['type'].upper() == 'OP']
    openings.sort(key=lambda x: len(x['slug']))
    print(f'Adding openings for {anime.Name} ({i + 1} of {num_animes})')
    added_openings = set()
    for opening in openings:
        num = opening['sequence']
        if num in added_openings:
            continue
        added_openings.add(num)
        op_num = str('OP' + str(opening['sequence'] if opening['sequence'] is not None else 1))
        song = opening['song']
        opening_title = song['title'] if song['title'] else 'Unknown title'
        artist = song['artists'][0]['name'] if song['artists'] and song['artists'][0]['name'] else 'Unknown title'
        video_link = get_best_resolution(opening)
        opening_entries.append(separator.join([anime.Name, str(anime.AniListID), opening_title, op_num, artist, video_link, full_url]))
        print(color_text(f'\tAdded: {op_num}', Colors.grey))
    added_animes.add(al_id)
    check_limit_and_wait(response)

write_lines('data/openings.txt', opening_entries)

done_messege = f"Done! Fetched {len(opening_entries)} openings."
print(color_text(done_messege, Colors.green))
logs.append(done_messege)
write_lines('logs/openings_logs.txt', logs)

