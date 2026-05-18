from data.loader import load_players
from engine.draft_engine import DraftEngine
from simulation.snake_draft import SnakeDraftSimulator
from engine.recommendations import get_recommendations
from models.draft_state import DraftState
from engine.cpu_logic import cpu_score


def run_debug_simulation(rounds=4, num_teams=10):
    players = load_players()

    draft_state = DraftState()

    simulator = SnakeDraftSimulator(
        players=players,
        draft_state=draft_state,
        num_teams=num_teams
    )

    available_players = players.copy()

    print("\nSTARTING 4-ROUND DRAFT SIMULATION\n")

    for r in range(rounds):
        print(f"\n================ ROUND {r + 1} ================\n")

        pick_order = simulator.get_next_pick_order()

        for team in pick_order:
            print(f"\n--- TEAM {team} ON THE CLOCK ---")

            # User Pick
            if team == 0:
                recs = get_recommendations(
                    available_players,
                    draft_state,
                    top_n=5
                )

                print("\nAI RECOMMENDATIONS:")
                for p, score in recs:
                    print(f"{p.name} ({p.position}) | Score: {round(score, 2)}")

                pick = recs[0][0]

                print(f"\nAI PICKS: {pick.name} ({pick.position})")

            # CPU Pick
            else:
                best_player = None
                best_score = float("-inf")

                for p in available_players:
                    score = cpu_score(p, draft_state, draft_state.current_pick)

                    if score > best_score:
                        best_score = score
                        best_player = p

                pick = best_player

                print(f"\n🤖 CPU PICKS: {pick.name} ({pick.position})")

            # Update State
            draft_state.draft_player(pick)
            available_players.remove(pick)

            print(f"Drafted: {pick.name} | {pick.position}")
            print(f"Roster so far: {[p.position for p in draft_state.drafted_players]}")

    print("\nSIMULATION COMPLETE\n")

if __name__ == "__main__":
    run_debug_simulation()