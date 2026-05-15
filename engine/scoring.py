from engine.positional_runs import detect_positional_runs

def calculate_draft_score(player, draft_state):
    base = (
        player.vbd * 0.7
        + player.upside * 5
        - player.risk * 3
    )

    # positional scarcity
    drafted_same_position = sum(
        1 for p in draft_state.drafted_players
        if p.position == player.position
    )

    scarcity_bonus = drafted_same_position * 2

    # positional run pressure
    runs = detect_positional_runs(draft_state)

    urgency_bonus = 0

    if player.position in runs:
        if runs[player.position] == "HOT_RUN":
            urgency_bonus = 25
        elif runs[player.position] == "MODERATE_RUN":
            urgency_bonus = 10

    return base + scarcity_bonus + urgency_bonus