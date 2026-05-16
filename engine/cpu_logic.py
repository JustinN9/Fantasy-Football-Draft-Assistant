import random

def cpu_score(player, draft_state, current_pick):
    score = player.projected_points * 0.6  # slightly stronger signal

    adp_pressure = max(0, 120 - abs(player.adp - current_pick))
    score += adp_pressure * 0.4

    position_need = {
        "QB": 1.0,
        "RB": 1.25,
        "WR": 1.25,
        "TE": 1.05
    }

    score *= position_need[player.position]

    # IMPORTANT: move randomness earlier (not just additive noise)
    score *= random.uniform(0.92, 1.08)

    return score