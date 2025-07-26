from dataclasses import dataclass
from random import shuffle
from typing import Dict, List, Literal

from data_collection.utils import separator

@dataclass
class Anime:
    Name: str
    AniListID: int

    def __post_init__(self):
        self.AniListID = int(self.AniListID)

@dataclass
class Opening:
    AnimeName: str
    AniListID: int
    Title: str
    Num: str
    Artist: str
    VideoLink: str
    ATLink: str

    def __post_init__(self):
        self.AniListID = int(self.AniListID)


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

def get_openings(number: int = 128, mode:str = 'top', selection: str | None = None) -> List[Opening]:
    return get_openings_all(number, mode) if selection is None else get_openings_single_per_anime(number, mode, selection)

def get_openings_all(number: int = 128, mode:str = 'top') -> List[Opening]:
    openings = []
    with open('data/openings.txt', 'r', encoding="utf-8") as file:
        for line in file:
            openings.append(Opening(*line.split(sep=separator)))
    if mode == 'random':
        shuffle(openings)
    return openings[:number]


def get_openings_single_per_anime(number: int = 128, mode: Literal['top', 'random'] = 'top', selection: Literal['first', 'random'] = None) -> List[Opening]:
    openings = {}
    with open('data/openings.txt', 'r', encoding="utf-8") as file:
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
    return result[:number]
