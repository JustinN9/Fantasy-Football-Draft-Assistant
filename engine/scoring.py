def calculate_draft_score(player, draft_state):
    base = (
        player.vbd * 0.7
        + player.upside * 5
        - player.risk * 3
    )

    # positional scarcity bonus
    position_counts = {
        "QB": 2,
        "RB": 5,
        "WR": 5,
        "TE": 1
    }

    drafted_same_position = sum(
        1 for p in draft_state.drafted_players
        if p.position == player.position
    )

    scarcity_bonus = drafted_same_position * 2

    return base + scarcity_bonus