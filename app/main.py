from data.loader import load_players
from engine.draft_engine import DraftEngine

if __name__ == "__main__":
    players = load_players()

    engine = DraftEngine(players)
    engine.run(rounds=3)