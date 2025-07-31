import json
from pathlib import Path
from tournament.manager import TournamentManager

SAVE_DIR = Path("saved_tournaments")
SAVE_DIR.mkdir(exist_ok=True)


def save_tournament(manager: TournamentManager, filename: str):
    try:
        path = SAVE_DIR / f"{filename}.json"
        with open(path, 'w') as f:
            json.dump(manager.to_dict(), f, indent=2)
        return True
    except Exception as e:
        print(e)
        return False


def load_tournament(filename: str) -> TournamentManager | None:
    try:
        path = SAVE_DIR / f"{filename}.json"
        with open(path, 'r') as f:
            data = json.load(f)
        return TournamentManager.from_dict(data)
    except Exception as e:
        print(e)
        return None


def get_saved_tournaments():
    return [f.stem for f in SAVE_DIR.glob("*.json")]