import pandas as pd

from models.player import Player
from engine.vbd import calculate_vbd
from models.draft_state import DraftState
from engine.recommendations import get_recommendations

from simulation.snake_draft import SnakeDraftSimulator
from models.draft_state import DraftState

from engine.positional_runs import detect_positional_runs
from engine.scoring import calculate_draft_score

draft_state = DraftState()

runs = detect_positional_runs(draft_state)


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

#print(f"Loaded {len(players)} players")
#print("\nPLAYER VBD VALUES\n")
#for player in players:
#    print(
#        f"{player.name:20} "
#        f"{player.position:3} "
#        f"Proj: {player.projected_points:5} "
#        f"VBD: {player.vbd:5.1f}"
#    )

simulator = SnakeDraftSimulator(
    players=players,
    draft_state=draft_state,
    num_teams=10
)

print("\nCALIBRATION VIEW\n")
for p in sorted(players, key=lambda x: x.projected_points, reverse=True)[:10]:
    score = calculate_draft_score(p, draft_state, players)
    print(f"{p.name:20} PROJ:{p.projected_points} SCORE:{score:.2f}")

# simulate 3 rounds first
for _ in range(3):
    simulator.simulate_pick()

    if runs:
        print("\nPOSITIONAL RUN ALERTS:")
        for pos, level in runs.items():
            print(f"- {pos}: {level}")

#recommendations = get_recommendations(players, draft_state)
#print("\nTOP RECOMMENDATIONS (ADJUSTED FOR DRAFT STATE)\n")
#for i, (player, score) in enumerate(recommendations, 1):
#    print(f"{i}. {player.name} - {score:.2f}")

print("\nCALIBRATION VIEW\n")
for p in sorted(players, key=lambda x: x.projected_points, reverse=True)[:10]:
    score = calculate_draft_score(p, draft_state, players)
    print(f"{p.name:20} PROJ:{p.projected_points} SCORE:{score:.2f}")
