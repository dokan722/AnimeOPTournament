import random
from typing import List, Tuple, Optional
from data_collection.models import Opening


class TournamentBracket:
    def __init__(self, openings: List[Opening]):
        self.openings = openings
        random.shuffle(self.openings)
        self.rounds = []
        self.current_round = 0
        self.generate_bracket()

    def generate_bracket(self):
        # Create initial bracket (round 0) as list of openings
        current_bracket = self.openings
        self.rounds.append(current_bracket)

        # Generate subsequent rounds
        while len(current_bracket) > 1:
            next_round = [None] * (len(current_bracket) // 2)
            current_bracket = next_round
            self.rounds.append(current_bracket)

    def get_current_matches(self) -> List[Tuple[Opening, Opening]]:
        if self.current_round >= len(self.rounds):
            return []

        current_round_items = self.rounds[self.current_round]
        return [
            (current_round_items[i], current_round_items[i + 1])
            for i in range(0, len(current_round_items), 2)
        ]

    def record_winner(self, match_index: int, winner: Opening):
        next_round = self.current_round + 1
        if next_round >= len(self.rounds):
            return

        # Calculate position in next round
        next_index = match_index
        self.rounds[next_round][next_index] = winner

    def advance_round(self):
        if self.current_round < len(self.rounds) - 1:
            self.current_round += 1
            return True
        return False

    def is_complete(self):
        return self.current_round == len(self.rounds) - 1 and \
            all(item is not None for item in self.rounds[-1])

    def get_winner(self) -> Optional[Opening]:
        if self.is_complete():
            return self.rounds[-1][0]
        return None