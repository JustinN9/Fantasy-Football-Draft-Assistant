from data.loader import load_players
from engine.recommendations import get_recommendations
from engine.cpu_logic import cpu_score
from models.draft_state import DraftState

NUM_ROUNDS = 4
NUM_TEAMS = 10


def print_team_rosters(draft_state):

    print("\nCURRENT ROSTERS")

    for team_id in range(NUM_TEAMS):

        roster = draft_state.get_team_roster(team_id)

        formatted = []

        for player in roster:
            formatted.append(
                f"{player.name} ({player.position})"
            )

        roster_text = ", ".join(formatted) if formatted else "Empty"

        print(f"Team {team_id}: {roster_text}")


def get_cpu_pick(
    available_players,
    draft_state,
    current_pick,
    team_id
):

    best_player = None
    best_score = float("-inf")

    for player in available_players:

        score = cpu_score(
            player,
            draft_state,
            available_players,
            current_pick,
            team_id
        )

        if score > best_score:
            best_score = score
            best_player = player

    return best_player


def run_debug_simulation():

    players = load_players()

    print(f"Loaded {len(players)} players")

    print("\nSTARTING 4-ROUND DRAFT SIMULATION\n")

    draft_state = DraftState(num_teams=NUM_TEAMS)

    available_players = players.copy()

    direction = 1

    for round_num in range(1, NUM_ROUNDS + 1):

        print(f"\n{'=' * 18} ROUND {round_num} {'=' * 18}\n")

        if direction == 1:
            order = list(range(NUM_TEAMS))
        else:
            order = list(range(NUM_TEAMS - 1, -1, -1))

        for team_id in order:

            print(f"\n--- TEAM {team_id} ON THE CLOCK ---")

            pick = None

            # USER TEAM
            if team_id == 0:

                recommendations = get_recommendations(
                    available_players,
                    draft_state,
                    players,     # FIX: all_players added
                    team_id,
                    top_n=5
                )

                print("\nAI RECOMMENDATIONS:")

                for r in recommendations:
                    player = r["player"]
                    score = r["score"]
                    reasons = r["reasons"]

                    print(
                        f"{player.name} ({player.position}) | Score: {round(score, 2)}"
                    )

                    for reason in reasons:
                        print(f"   - {reason}")

                pick = recommendations[0]["player"] if recommendations else None

                if pick:
                    print(f"\nAI PICKS: {pick.name} ({pick.position})")

            # CPU TEAM
            else:

                pick = get_cpu_pick(
                    available_players,
                    draft_state,
                    draft_state.current_pick,
                    team_id
                )

                if pick:
                    print(f"CPU PICKS: {pick.name} ({pick.position})")

            if pick is None:
                continue

            draft_state.draft_player(pick, team_id)
            available_players.remove(pick)

        print_team_rosters(draft_state)

        direction *= -1

    print(f"\n{'=' * 18} DRAFT COMPLETE {'=' * 18}")


if __name__ == "__main__":
    run_debug_simulation()