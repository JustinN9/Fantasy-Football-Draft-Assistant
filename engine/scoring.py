from engine.config import SCORING_PROFILES
from engine.positional_runs import detect_positional_runs


def get_replacement_value(players, position):

    candidates = [p for p in players if p.position == position]

    if not candidates:
        return 0

    return max(candidates, key=lambda p: p.projected_points).projected_points


def calculate_draft_score(player, draft_state, all_players):

    w = SCORING_PROFILES["default"]

    # Base Value Component
    base = (
        player.vbd * w["vbd_weight"]
        + player.upside * w["upside_weight"]
        - player.risk * w["risk_weight"]
    )

    # Scarcity Component
    drafted_same_position = sum(
        1 for p in draft_state.drafted_players
        if p.position == player.position
    )

    scarcity_bonus = drafted_same_position * w["scarcity_weight"]

    # ADP Pressure
    adp_diff = abs(player.adp - draft_state.current_pick)
    adp_pressure = max(0, 1 - (adp_diff / 80))  # 0–1 scale

    adp_bonus = adp_pressure * 40 * w["adp_weight"]

    # Opportunity Cost
    replacement = get_replacement_value(all_players, player.position)

    opportunity = (
        player.projected_points - replacement
    ) * w["opportunity_weight"]

    # Positional Runs
    runs = detect_positional_runs(draft_state)

    run_bonus = 0

    if player.position in runs:
        if runs[player.position] == "HOT_RUN":
            run_bonus = 25
        elif runs[player.position] == "MODERATE_RUN":
            run_bonus = 10
        elif runs[player.position] == "ACTIVE":
            run_bonus = 5

    # Final Score
    return base + scarcity_bonus + adp_bonus + opportunity + run_bonus