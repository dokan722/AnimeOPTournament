from pathlib import Path
from random import shuffle
from typing import Dict, List, Literal

from data_collection.models import Anime, Opening
from data_collection.utils import separator

def get_correlations() -> Dict[int, int]:
    result = {}
    with open('data/correlations.txt', 'r', encoding="utf-8") as file:
        for line in file:
            at_slug, al_id = line.split(sep=separator)
            result[int(al_id)] = at_slug

    return result

def get_top_animes() -> List[Anime]:
    result = []
    with open('data/top_animes.txt', 'r', encoding="utf-8") as file:
        for line in file:
            result.append(Anime(*line.split(sep=separator)))
    return result

def get_openings(take: int = 128, choose: int = 128,  mode:Literal['top', 'random'] = 'top', selection: Literal['all', 'first', 'random'] = 'all') -> List[Opening]:
    base_path = Path(__file__).parent
    file_path = base_path / 'data' / 'openings.txt'
    return get_openings_all(file_path, take, choose, mode) if selection == 'all' else get_openings_single_per_anime(file_path, take, choose, mode, selection)

def get_openings_all(path: Path, take: int = 128, choose = 128, mode:str = 'top') -> List[Opening]:
    openings = []
    with path.open('r', encoding="utf-8") as file:
        for line in file:
            openings.append(Opening(*line.split(sep=separator)))
    if mode == 'random':
        shuffle(openings)
    if take != choose:
        openings = openings[:take]
        shuffle(openings)
    return openings[:choose]


def get_openings_single_per_anime(path: Path, take: int = 128, choose: int = 128, mode: Literal['top', 'random'] = 'top', selection: Literal['first', 'random'] = None) -> List[Opening]:
    openings = {}
    with path.open('r', encoding="utf-8") as file:
        for line in file:
            op = Opening(*line.split(sep=separator))
            if op.AniListID in openings:
                openings[op.AniListID].append(op)
            else:
                openings[op.AniListID] = [op]
    result =[]
    for key, value in openings.items():
        if selection == 'random':
            shuffle(value)
        result.append(value[0])
    if mode == 'random':
        shuffle(result)
    if take != choose:
        result = result[:take]
        shuffle(result)
    return result[:choose]

def get_counts():
    base_path = Path(__file__).parent
    file_path = base_path / 'data' / 'counts.txt'
    counts = []
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            counts.append(int(line))
    return counts
