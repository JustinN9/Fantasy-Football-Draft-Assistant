def cpu_score(player, draft_state, current_pick):
    score = player.projected_points * 0.5

    # ADP pressure (players "should" go around their ADP)
    adp_pressure = max(0, 100 - abs(player.adp - current_pick))
    score += adp_pressure * 0.3

    # positional scarcity (basic version)
    position_need = {
        "QB": 1.0,
        "RB": 1.2,
        "WR": 1.2,
        "TE": 1.0
    }

    score *= position_need[player.position]

    # small randomness so drafts aren't identical
    import random
    score += random.uniform(-10, 10)

    return score