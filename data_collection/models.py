from dataclasses import dataclass
from typing import Optional, List


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