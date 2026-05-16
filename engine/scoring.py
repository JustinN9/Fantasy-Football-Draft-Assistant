from engine.config import SCORING_WEIGHTS
from engine.positional_runs import detect_positional_runs

def get_replacement_value(players, position):
    candidates = [p for p in players if p.position == position]

    if not candidates:
        return 0

    best = max(candidates, key=lambda p: p.projected_points)
    return best.projected_points

def calculate_draft_score(player, draft_state, all_players):
    w = SCORING_WEIGHTS

    base = (
        player.vbd * w["vbd_weight"]
        + player.upside * w["upside_weight"]
        - player.risk * w["risk_weight"]
    )

    # scarcity
    drafted_same_position = sum(
        1 for p in draft_state.drafted_players
        if p.position == player.position
    )
    scarcity_bonus = drafted_same_position * w["scarcity_weight"]

    # ADP alignment (new realism layer)
    adp_pressure = max(0, 100 - abs(player.adp - draft_state.current_pick))
    adp_bonus = adp_pressure * w["adp_weight"]

    # opportunity cost (replacement value logic)
    replacement = get_replacement_value(all_players, player.position)
    opportunity = (player.projected_points - replacement) * w["opportunity_weight"]

    # positional runs
    runs = detect_positional_runs(draft_state)
    run_bonus = 0

    if player.position in runs:
        if runs[player.position] == "HOT_RUN":
            run_bonus = 25
        elif runs[player.position] == "MODERATE_RUN":
            run_bonus = 10

    return base + scarcity_bonus + adp_bonus + opportunity + run_bonus