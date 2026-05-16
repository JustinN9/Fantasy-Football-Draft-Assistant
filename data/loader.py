import pandas as pd
from models.player import Player
from engine.vbd import calculate_vbd

def load_players(path="data/players.csv"):
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise Exception(f"Player file not found at {path}")

    players = []

    for _, row in df.iterrows():
        try:
            player = Player(
                name=row["name"],
                position=row["position"],
                team=row["team"],
                projected_points=float(row["projected_points"]),
                adp=int(row["adp"]),
                upside=int(row["upside"]),
                risk=int(row["risk"]),
                tier=int(row["tier"])
            )
            player.vbd = calculate_vbd(player)
            players.append(player)

        except KeyError as e:
            raise Exception(f"Missing column in CSV: {e}")

    print(f"Loaded {len(players)} players")
    return players