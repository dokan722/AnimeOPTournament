from typing import Any
import requests
from slugify import slugify
import re
from utils import check_limit_and_wait, write_lines, separator


def clean_text(text: str) -> str:
    return re.sub(r'[./]', '', text) if text is not None else ''

def get_best_resolution(opening: Any) -> str:
    try:
        chosen = opening['animethemeentries'][0]['videos'][0]
        max_res = chosen['resolution']
        for video in opening['animethemeentries'][0]['videos']:
            if (video['resolution'] > max_res):
                max_res = video['resolution']
                chosen = video

        return chosen['link']
    except:
        return None




anilist_url = "https://graphql.anilist.co"
animethemes_url = "https://api.animethemes.moe/anime/"

query = '''
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: SCORE_DESC) {
      title {
        romaji
        english
        native
      }
    }
  }
}
'''

titles = []
added_animes = []

for page in range(1, 3):
    variables = {
        'page': page,
        'perPage': 50
    }

    response = requests.post(
        anilist_url,
        json={'query': query, 'variables': variables},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        print(f"Failed to fetch page {page}: {response.status_code}")
        continue

    data = response.json()
    media_list = data['data']['Page']['media']

    for anime in media_list:
        title = anime["title"]["english"] or anime["title"]["romaji"] or anime["title"]["native"]
        slug_rom = slugify(clean_text(anime["title"]["romaji"]), separator='_')
        slug_en = slugify(clean_text(anime["title"]["english"]), separator='_')
        slug = slug_rom
        anime_response = requests.get(animethemes_url + slug_rom, params={'include': 'animethemes.animethemeentries.videos'})
        if anime_response.status_code != 200:
            if slug_en:
                slug = slug_en
                anime_response = requests.get(animethemes_url + slug_en, params={'include': 'animethemes.animethemeentries.videos'})
                check_limit_and_wait(anime_response)
                if anime_response.status_code != 200:
                    print('Failed to fetch page ', slug_rom, ' or ', slug_en, ':', anime_response.status_code)
                    continue
            else:
                print('Failed to fetch page ', slug_rom, ':', anime_response.status_code)
                continue
        if slug in added_animes:
            continue
        added_animes.append(slug)
        anime_data = anime_response.json()
        openings = [x for x in anime_data['anime']['animethemes'] if x['type'].upper() == 'OP']
        openings.sort(key=lambda x: len(x['slug']))
        added_openings = []
        for opening in openings:
            if opening['sequence']  in added_openings:
                continue
            added_openings.append(opening['sequence'])
            titles.append(separator.join([title, slug, get_best_resolution(opening)]))
            print('Added ', title, opening['slug'])
        check_limit_and_wait(anime_response)




    print(f"Fetched page {page} – added {len(titles)} ")
    check_limit_and_wait(response)

write_lines('top_anime.txt', titles)

print("Done! Fetched ", len(titles), " openings.")