import pandas as pd

from models.player import Player
from engine.vbd import calculate_vbd
from models.draft_state import DraftState
from engine.recommendations import get_recommendations

draft_state = DraftState()

df = pd.read_csv("data/players.csv")

players = []

for _, row in df.iterrows():
    player = Player(
        row["name"],
        row["position"],
        row["team"],
        row["projected_points"],
        row["adp"],
        row["upside"],
        row["risk"],
        row["tier"]
    )

    players.append(player)


for player in players:
    player.vbd = calculate_vbd(player)

print(f"Loaded {len(players)} players")

print("\nPLAYER VBD VALUES\n")

for player in players:
    print(
        f"{player.name:20} "
        f"{player.position:3} "
        f"Proj: {player.projected_points:5} "
        f"VBD: {player.vbd:5.1f}"
    )

draft_state.draft_player(players[0])  # simulate CMC gone
draft_state.draft_player(players[1])  # simulate Bijan gone

recommendations = get_recommendations(players, draft_state)

print("\nTOP RECOMMENDATIONS (ADJUSTED FOR DRAFT STATE)\n")

for i, (player, score) in enumerate(recommendations, 1):
    print(f"{i}. {player.name} - {score:.2f}")