from engine.positional_runs import detect_positional_runs

# Roster Structure
ROSTER_LIMITS = {
    "QB": 1,
    "RB": 2,
    "WR": 2,
    "TE": 1
}

# Replacement Value
def get_replacement_value(players, position):
    pool = [p for p in players if p.position == position]
    if not pool:
        return 0
    return max(pool, key=lambda p: p.projected_points).projected_points

# Team Need Model
def team_need(player, draft_state):
    counts = {"QB": 0, "RB": 0, "WR": 0, "TE": 0}

    for p in draft_state.drafted_players:
        if p.position in counts:
            counts[p.position] += 1

    return {
        "QB": 1 - min(counts["QB"] / 1, 1),
        "RB": 1 - min(counts["RB"] / 2, 1),
        "WR": 1 - min(counts["WR"] / 2, 1),
        "TE": 1 - min(counts["TE"] / 1, 1),
    }.get(player.position, 0)

# Market Scarcity
def market_scarcity(player, all_players, draft_state):
    remaining = [
        p for p in all_players
        if p.position == player.position
        and not draft_state.is_drafted(p)
    ]

    if not remaining:
        return 0

    best_tier = min(p.tier for p in remaining)

    elite_remaining = sum(
        1 for p in remaining
        if p.tier == best_tier
    )

    return 1 / (elite_remaining + 1)

# Tier Cliff
def tier_cliff(players, draft_state, position):
    remaining = [
        p for p in players
        if p.position == position
        and not draft_state.is_drafted(p)
    ]

    if not remaining:
        return 0

    best_tier = min(p.tier for p in remaining)

    tier_count = sum(
        1 for p in remaining
        if p.tier == best_tier
    )

    return 1 / (tier_count + 1)

# Main Score Function
def calculate_draft_score(player, draft_state, all_players):

    # Base Value
    base = (
        player.vbd * 0.7
        + player.upside * 0.25
        - player.risk * 0.2
    )

    # Core Vlaue
    replacement = get_replacement_value(all_players, player.position)
    value_over_replacement = (player.projected_points - replacement) * 0.5

    # Team Need
    need = team_need(player, draft_state)

    # Market Scacity
    scarcity = market_scarcity(player, all_players, draft_state)

    # Tier CLiffs
    cliff = tier_cliff(all_players, draft_state, player.position)

    # Possession Run
    runs = detect_positional_runs(draft_state)

    run_bonus = 0
    if player.position in runs:
        run_bonus = 20 if runs[player.position] == "HOT_RUN" else 8

    # Final Score
    score = base + value_over_replacement + run_bonus + (cliff * 30)

    # multiplicative decision layer
    score *= (1 + need * 1.5)
    score *= (1 + scarcity * 1.2)

    return score