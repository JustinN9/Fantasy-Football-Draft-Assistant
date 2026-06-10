import random

from data.loader import load_players
from engine.recommendations import get_recommendations
from engine.scoring import calculate_draft_score

from engine.cpu_personalities import (
    get_cpu_personality,
    apply_personality_modifier
)

from models.draft_state import DraftState

NUM_ROUNDS = 4
NUM_TEAMS = 10


def print_team_rosters(draft_state):

    print("\nCURRENT ROSTERS")

    for team_id in range(NUM_TEAMS):

        roster = draft_state.get_team_roster(team_id)

        formatted = [
            f"{p.name} ({p.position})"
            for p in roster
        ]

        print(f"Team {team_id}: {', '.join(formatted) if formatted else 'Empty'}")


def get_cpu_pick(
    available_players,
    draft_state,
    all_players,
    team_id
):

    personality = get_cpu_personality(team_id)

    best_player = None
    best_score = float("-inf")

    for player in available_players:

        base_score = calculate_draft_score(
            player,
            draft_state,
            all_players,
            team_id
        )

        final_score = apply_personality_modifier(
            player,
            base_score,
            personality
        )

        # Tie-breaking randomness (important for variation)
        if (
            final_score > best_score
            or (
                abs(final_score - best_score) < 0.5
                and random.random() < 0.5
            )
        ):
            best_score = final_score
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

        # Optional realism: slight shuffle within round order
        random.shuffle(order)

        for team_id in order:

            print(f"\n--- TEAM {team_id} ON THE CLOCK ---")

            pick = None

            # USER TEAM
            if team_id == 0:

                recommendations = get_recommendations(
                    available_players,
                    draft_state,
                    players,
                    team_id,
                    top_n=5
                )

                print("\nAI RECOMMENDATIONS:")

                for r in recommendations:
                    player = r["player"]
                    score = r["score"]
                    reasons = r["reasons"]

                    print(f"{player.name} ({player.position}) | Score: {round(score, 2)}")

                    for reason in reasons:
                        print(f"   - {reason}")

                pick = recommendations[0]["player"] if recommendations else None

                if pick:
                    print(f"\nAI PICKS: {pick.name} ({pick.position})")

            # CPU TEAMS
            else:

                pick = get_cpu_pick(
                    available_players,
                    draft_state,
                    players,
                    team_id
                )

                if pick:
                    personality = get_cpu_personality(team_id)
                    print(f"CPU PICKS: {pick.name} ({pick.position}) [{personality}]")

            if pick is None:
                continue

            draft_state.draft_player(pick, team_id)
            available_players.remove(pick)

        print_team_rosters(draft_state)

        direction *= -1

    print(f"\n{'=' * 18} DRAFT COMPLETE {'=' * 18}")


if __name__ == "__main__":
    run_debug_simulation()