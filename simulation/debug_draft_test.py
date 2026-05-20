from data.loader import load_players
from engine.recommendations import get_recommendations
from engine.cpu_logic import cpu_score
from models.draft_state import DraftState

NUM_ROUNDS = 4
NUM_TEAMS = 10

def print_team_rosters(draft_state):

    print("\nCURRENT ROSTERS")

    for team_id in range(NUM_TEAMS):

        roster = draft_state.get_team_roster(
            team_id
        )

        formatted = []

        for player in roster:
            formatted.append(
                f"{player.name} "
                f"({player.position})"
            )

        roster_text = (
            ", ".join(formatted)
            if formatted
            else "Empty"
        )

        print(
            f"Team {team_id}: "
            f"{roster_text}"
        )


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

    print(
        f"Loaded "
        f"{len(players)} players"
    )

    print(
        "\nSTARTING "
        "4-ROUND DRAFT "
        "SIMULATION\n"
    )

    draft_state = DraftState(
        num_teams=NUM_TEAMS
    )

    available_players = (
        players.copy()
    )

    direction = 1

    for round_num in range(
        1,
        NUM_ROUNDS + 1
    ):

        print(
            f"\n{'=' * 18} "
            f"ROUND {round_num} "
            f"{'=' * 18}\n"
        )

        if direction == 1:
            order = list(
                range(NUM_TEAMS)
            )
        else:
            order = list(
                range(
                    NUM_TEAMS - 1,
                    -1,
                    -1
                )
            )

        for team_id in order:

            print(
                f"\n--- TEAM "
                f"{team_id} "
                f"ON THE CLOCK ---"
            )

            # USER TEAM
            if team_id == 0:

                recommendations = (
                    get_recommendations(
                        available_players,
                        draft_state,
                        top_n=5
                    )
                )

                print(
                    "\nAI "
                    "RECOMMENDATIONS:"
                )

                for (
                    player,
                    score
                ) in recommendations:

                    print(
                        f"{player.name} "
                        f"({player.position}) "
                        f"| Score: "
                        f"{round(score, 2)}"
                    )

                pick = (
                    recommendations[0][0]
                    if recommendations
                    else None
                )

                if pick:
                    print(
                        f"\nAI PICKS: "
                        f"{pick.name} "
                        f"({pick.position})"
                    )

            # CPU TEAM
            else:

                recommendations = (
                    get_recommendations(
                        available_players,
                        draft_state,
                        top_n=5
                    )
                )

                pick = get_cpu_pick(
                    available_players,
                    draft_state,
                    draft_state.current_pick,
                    team_id
                )

                if pick:
                    print(
                        f"CPU PICKS: "
                        f"{pick.name} "
                        f"({pick.position})"
                    )

            if pick is None:
                continue

            draft_state.draft_player(
                pick,
                team_id
            )

            available_players.remove(
                pick
            )

        print_team_rosters(
            draft_state
        )

        direction *= -1

    print(
        f"\n{'=' * 18} "
        f"DRAFT COMPLETE "
        f"{'=' * 18}"
    )


if __name__ == "__main__":
    run_debug_simulation()