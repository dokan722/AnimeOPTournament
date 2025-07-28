import json
from typing import Dict, Any, List
from tournament.bracket import TournamentBracket
from data_collection.models import Opening


class TournamentManager:
    def __init__(self):
        self.name = ""
        self.bracket = None
        self.current_match_index = 0
        self.openings = []

    def new_tournament(
            self,
            name: str,
            openings: List[Opening]
    ):
        self.name = name
        self.openings = openings
        self.bracket = TournamentBracket(openings)
        self.current_match_index = 0

    def get_current_match(self) -> tuple[Opening, Opening] | None:
        if not self.bracket or self.is_complete():
            return None

        matches = self.bracket.get_current_matches()
        if self.current_match_index < len(matches):
            return matches[self.current_match_index]
        return None

    def record_winner(self, winner: Opening):
        if self.bracket and not self.is_complete():
            self.bracket.record_winner(self.current_match_index, winner)
            self.current_match_index += 1

            # Advance round if needed
            if self.current_match_index >= len(self.bracket.get_current_matches()):
                self.bracket.advance_round()
                self.current_match_index = 0

    def is_complete(self):
        return self.bracket and self.bracket.is_complete()

    def get_winner(self):
        return self.bracket.get_winner() if self.bracket else None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "openings": [op.__dict__ for op in self.openings],
            "rounds": [[op.__dict__ if op is not None else None for op in round_] for round_ in self.bracket.rounds] if self.bracket else [],
            "current_round": self.bracket.current_round if self.bracket else 0,
            "current_match_index": self.current_match_index
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        manager = cls()
        manager.name = data["name"]
        manager.openings = [Opening(**op) for op in data["openings"]]

        # Create a new bracket
        manager.bracket = TournamentBracket(manager.openings)

        # Restore bracket state
        manager.bracket.rounds = [
            [Opening(**item) if item is not None else None for item in round_list]
            for round_list in data["rounds"]
        ]
        manager.bracket.current_round = data["current_round"]
        manager.current_match_index = data["current_match_index"]
        return manager