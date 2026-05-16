from engine.positional_runs import detect_positional_runs

# ROSTER STRUCTURE
ROSTER_SLOTS = {
    "QB": 1,
    "RB": 2,
    "WR": 2,
    "TE": 1,
    "K": 1,
    "DEF": 1
}

FLEX_POSITIONS = {"RB", "WR", "TE"}

# POSITION SCARCITY (GLOBAL)
POSITION_SCARCITY = {
    "RB": 1.8,
    "WR": 1.0,
    "TE": 1.6,
    "QB": 0.8,
    "K": 0.2,
    "DEF": 0.2
}

# SATURATION MODEL
def saturation_multiplier(count, limit):
    ratio = count / max(limit, 1)

    if ratio <= 0.5:
        return 1.0
    elif ratio <= 0.8:
        return 0.85
    elif ratio < 1.0:
        return 0.6
    return 0.2

# TIER CLIFF PRESSURE
def get_tier_cliff_pressure(players, draft_state, position):
    remaining = [
        p for p in players
        if p.position == position
        and not draft_state.is_drafted(p)
    ]

    if not remaining:
        return 0

    best_tier = min(p.tier for p in remaining)

    tier_size = sum(
        1 for p in remaining
        if p.tier == best_tier
    )

    return 1 / (tier_size + 1)

# REPLACEMENT VALUE
def get_replacement_value(players, position):
    candidates = [p for p in players if p.position == position]
    if not candidates:
        return 0
    return max(candidates, key=lambda p: p.projected_points).projected_points

# AVAILABILITY PRESSURE
def availability_pressure(player, draft_state, num_teams=10):
    picks_until_next = num_teams - (draft_state.current_pick % num_teams)

    adp_gap = player.adp - draft_state.current_pick

    if adp_gap < picks_until_next:
        return 1.0
    elif adp_gap < picks_until_next * 2:
        return 0.5
    return 0.1


# MAIN SCORING FUNCTION
def calculate_draft_score(player, draft_state, all_players):
    # ROSTER STATE
    position_counts = {
        pos: sum(
            1 for p in draft_state.drafted_players
            if p.position == pos
        )
        for pos in ROSTER_SLOTS.keys()
    }

    count = position_counts.get(player.position, 0)
    limit = ROSTER_SLOTS.get(player.position, 1)

    # FLEX tracking
    flex_count = sum(
        1 for p in draft_state.drafted_players
        if p.position in FLEX_POSITIONS
    )

    # HARD ROSTER RULES
    if player.position in ROSTER_SLOTS and count >= limit:
        return -9999

    # BASE VALUE
    base = (
        player.vbd * 0.6
        + player.upside * 0.3
        - player.risk * 0.2
    )

    # GLOBAL SCARCITY
    scarcity = POSITION_SCARCITY.get(player.position, 1.0)

    # ROSTER SATURATION
    roster_pressure = saturation_multiplier(count, limit)

    # REPLACEMENT VALUE
    replacement = get_replacement_value(all_players, player.position)
    opportunity = (player.projected_points - replacement) * 0.5

    # POSITIONS RUNS
    runs = detect_positional_runs(draft_state)

    run_bonus = 0
    if player.position in runs:
        if runs[player.position] == "HOT_RUN":
            run_bonus = 20
        elif runs[player.position] == "MODERATE_RUN":
            run_bonus = 8

    # TIER CLIFF LOGIC
    tier_pressure = get_tier_cliff_pressure(all_players, draft_state, player.position)
    tier_bonus = tier_pressure * 25

    # AVAILABILITY MODEL
    avail_bonus = availability_pressure(player, draft_state) * 20

    # FINAL SCORE
    score = (
        base
        + opportunity
        + run_bonus
        + tier_bonus
        + avail_bonus
    )

    score *= scarcity
    score *= roster_pressure

    return score