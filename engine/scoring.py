from engine.positional_runs import detect_positional_runs
from engine.lookahead import calculate_lookahead_value

from engine.tiers import (
    build_position_tiers,
    get_tier_info,
    tier_pressure_bonus,
    tier_drop_risk
)

from engine.adp import adp_pressure


# =========================
# CONFIG
# =========================

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

RUN_BONUS = {
    "HOT_RUN": 4,
    "MODERATE_RUN": 2,
    "ACTIVE": 1
}


# =========================
# HELPERS
# =========================

def normalize(value, min_val, max_val):
    if value is None:
        return 0

    if max_val == min_val:
        return 50

    return ((value - min_val) / (max_val - min_val)) * 100


def safe_min_max(values):
    values = [v for v in values if v is not None]
    if not values:
        return 0, 1
    return min(values), max(values)


# =========================
# CORE SCORING
# =========================

def get_team_need_modifier(player, draft_state, team_id):
    roster = draft_state.get_team_roster(team_id)

    counts = {"QB": 0, "RB": 0, "WR": 0, "TE": 0}

    for p in roster:
        if p.position in counts:
            counts[p.position] += 1

    curve = TEAM_NEED_CURVES.get(player.position, [1.0])
    current_count = counts.get(player.position, 0)

    if current_count >= len(curve):
        return curve[-1]

    return curve[current_count]


def talent_score(player, all_players):
    vbds = [p.vbd for p in all_players if p.vbd is not None]

    vbd_min, vbd_max = safe_min_max(vbds)
    vbd_norm = normalize(player.vbd, vbd_min, vbd_max)

    upside_score = (player.upside or 0) * 10

    raw = (vbd_norm * 0.80) + (upside_score * 0.20)

    return raw * POSITION_WEIGHTS.get(player.position, 1.0)


def run_bonus(player, draft_state):
    runs = detect_positional_runs(draft_state)
    signal = runs.get(player.position)

    return RUN_BONUS.get(signal, 0)


# =========================
# MAIN SCORER
# =========================

def calculate_draft_score(
    player,
    draft_state,
    all_players,
    team_id=0
):
    # -------------------------
    # Tier system
    # -------------------------
    tier_map = build_position_tiers(all_players)
    tier_info = get_tier_info(player, tier_map, draft_state)

    tier_pressure = tier_pressure_bonus(tier_info)
    tier_risk = tier_drop_risk(tier_info)

    # -------------------------
    # ADP system
    # -------------------------
    current_pick = getattr(draft_state, "current_pick", 1)
    adp_score = adp_pressure(player, current_pick)

    # -------------------------
    # Core components
    # -------------------------
    talent = talent_score(player, all_players)

    need_modifier = get_team_need_modifier(player, draft_state, team_id)

    run = run_bonus(player, draft_state)

    lookahead = calculate_lookahead_value(
        player,
        draft_state,
        all_players,
        team_id
    )

    risk_penalty = (player.risk or 0) * 2

    # -------------------------
    # SCORING MODEL
    # -------------------------

    core = talent * need_modifier

    situational = (
        run +
        lookahead +
        adp_score
    )

    score = (
        core
        + situational
        + tier_pressure
        - tier_risk
        - risk_penalty
    )

    return round(score, 2)