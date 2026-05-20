POSITION_SCARCITY = {
    "QB": 0.03,
    "RB": 0.72,
    "WR": 0.40,
    "TE": 0.50
}


def calculate_next_pick_distance(
    draft_state,
    team_id,
    num_teams=10
):
    current_pick = (
        draft_state.current_pick
    )

    round_number = (
        (current_pick - 1)
        // num_teams
    ) + 1

    position_in_round = (
        current_pick - 1
    ) % num_teams

    snake_forward = (
        round_number % 2 == 1
    )

    if snake_forward:
        next_slot = (
            num_teams
            - 1
            - team_id
        )
    else:
        next_slot = team_id

    picks_until_end = (
        num_teams
        - 1
        - position_in_round
    )

    next_round_offset = abs(
        next_slot
        - team_id
    )

    wait = (
        picks_until_end
        + next_round_offset
        + 1
    )

    return max(2, wait)


def expected_remaining_vbd(
    position,
    available_players,
    next_pick
):
    future_pool = []

    for player in available_players:

        likely_gone = (
            player.adp
            <= next_pick
        )

        if likely_gone:
            continue

        if player.position == position:
            future_pool.append(
                player
            )

    if not future_pool:
        return 0

    best_remaining = max(
        future_pool,
        key=lambda p: p.vbd
    )

    return best_remaining.vbd


def calculate_lookahead_value(
    player,
    draft_state,
    all_players,
    team_id
):

    wait = (
        calculate_next_pick_distance(
            draft_state,
            team_id,
            draft_state.num_teams
        )
    )

    current_pick = (
        draft_state.current_pick
    )

    next_pick = (
        current_pick
        + wait
    )

    future_value = (
        expected_remaining_vbd(
            player.position,
            all_players,
            next_pick
        )
    )

    loss = (
        player.vbd
        - future_value
    )

    multiplier = (
        POSITION_SCARCITY.get(
            player.position,
            0.35
        )
    )

    return max(
        0,
        loss * multiplier
    )