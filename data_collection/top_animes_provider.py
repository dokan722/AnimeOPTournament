import requests

from utils import color_text, Colors, separator, check_limit_and_wait, write_lines

anilist_url = "https://graphql.anilist.co"

query = '''
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      title {
        romaji
        english
      }
      id
    }
  }
}
'''



animes = []
logs = []
pages = 40

for page in range(1, pages + 1):
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
        logs.append(f"Failed to fetch page {page}: {response.status_code}")
        print(color_text(f"Failed to fetch page {page}", Colors.red))
        continue

    data = response.json()
    anime_page = data['data']['Page']['media']

    for anime in anime_page:
        title = anime["title"]["english"] or anime["title"]["romaji"]
        id = anime["id"]
        animes.append(f"{title}{separator}{id}")

    print(color_text(f"Fetched page {page} – added {len(animes)} animes", Colors.green))
    check_limit_and_wait(response, 3)

write_lines('data/top_animes.txt', animes)

done_messege = f"Done! Fetched {len(animes)} animes."
print(color_text(done_messege, Colors.green))
logs.append(done_messege)
write_lines('logs/top_anime_logs.txt', logs)