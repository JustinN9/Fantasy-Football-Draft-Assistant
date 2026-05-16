import random


def cpu_score(player, draft_state, current_pick):

    # Base projection value
    score = player.projected_points * 0.6

    # ADP Signal
    adp_diff = abs(player.adp - current_pick)
    adp_factor = max(0, 1 - (adp_diff / 80))  # normalized 0–1

    score += adp_factor * 35

    # Positional Bias
    if current_pick < 20:
        position_need = {"QB": 0.9, "RB": 1.3, "WR": 1.3, "TE": 1.0}
    elif current_pick < 60:
        position_need = {"QB": 1.0, "RB": 1.2, "WR": 1.2, "TE": 1.1}
    else:
        position_need = {"QB": 1.2, "RB": 1.0, "WR": 1.0, "TE": 1.2}

    score *= position_need[player.position]

    # Draft state scarcity effect
    position_counts = {}

    for p in draft_state.drafted_players:
        position_counts[p.position] = position_counts.get(p.position, 0) + 1

    scarcity = position_counts.get(player.position, 0)

    # More scarcity = slightly higher urgency
    score *= (1 + scarcity * 0.03)

    # Upside / risk variance
    score *= random.uniform(0.92, 1.08)

    return score