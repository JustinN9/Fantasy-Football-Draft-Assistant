from engine.positional_runs import (
    detect_positional_runs
)

from engine.lookahead import (
    calculate_lookahead_value
)


TEAM_NEED_CURVES = {
    "QB": [1.0, 0.08, 0.01],
    "RB": [1.0, 0.98, 0.90, 0.72, 0.50, 0.28],
    "WR": [1.0, 0.94, 0.84, 0.70, 0.48, 0.28],
    "TE": [1.0, 0.18, 0.04]
}


POSITION_WEIGHTS = {
    "QB": 0.50,
    "RB": 1.22,
    "WR": 1.10,
    "TE": 0.88
}


def normalize(
    value,
    min_val,
    max_val
):
    if max_val == min_val:
        return 50

    return (
        (
            value - min_val
        )
        /
        (
            max_val - min_val
        )
    ) * 100


def get_team_need_modifier(
    player,
    draft_state,
    team_id
):
    roster = (
        draft_state.get_team_roster(
            team_id
        )
    )

    counts = {
        "QB": 0,
        "RB": 0,
        "WR": 0,
        "TE": 0
    }

    for p in roster:
        counts[p.position] += 1

    curve = (
        TEAM_NEED_CURVES[
            player.position
        ]
    )

    current_count = (
        counts[player.position]
    )

    if current_count >= len(curve):
        return curve[-1]

    return curve[current_count]


def talent_score(
    player,
    all_players
):
    vbds = [
        p.vbd
        for p in all_players
        if p.vbd is not None
    ]

    vbd_norm = normalize(
        player.vbd,
        min(vbds),
        max(vbds)
    )

    upside_score = (
        player.upside * 10
    )

    score = (
        vbd_norm * 0.80
        + upside_score * 0.20
    )

    score *= (
        POSITION_WEIGHTS.get(
            player.position,
            1.0
        )
    )

    return score


def tier_pressure(
    player,
    all_players,
    draft_state
):
    remaining = [
        p for p in all_players
        if (
            p.position
            == player.position
            and not draft_state.is_drafted(p)
        )
    ]

    if not remaining:
        return 0

    best_tier = min(
        p.tier
        for p in remaining
    )

    tier_count = sum(
        1
        for p in remaining
        if p.tier == best_tier
    )

    if tier_count == 1:
        return 8

    if tier_count <= 3:
        return 4

    return 0


def run_bonus(
    player,
    draft_state
):
    runs = (
        detect_positional_runs(
            draft_state
        )
    )

    signal = runs.get(
        player.position
    )

    bonuses = {
        "HOT_RUN": 4,
        "MODERATE_RUN": 2,
        "ACTIVE": 1
    }

    return bonuses.get(
        signal,
        0
    )


def calculate_draft_score(
    player,
    draft_state,
    all_players,
    team_id=0
):

    talent = talent_score(
        player,
        all_players
    )

    need_modifier = (
        get_team_need_modifier(
            player,
            draft_state,
            team_id
        )
    )

    pressure = tier_pressure(
        player,
        all_players,
        draft_state
    )

    run = run_bonus(
        player,
        draft_state
    )

    lookahead = (
        calculate_lookahead_value(
            player,
            draft_state,
            all_players,
            team_id
        )
    )

    risk_penalty = (
        player.risk * 2
    )

    score = (
        talent
        * need_modifier
    )

    score += pressure
    score += run
    score += lookahead
    score -= risk_penalty

    return round(score, 2)