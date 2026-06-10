from engine.tiers import build_position_tiers, get_tier_info
from engine.adp import adp_pressure


def explain_pick(player, draft_state, all_players, team_id=0):
    """
    Generates human-readable reasoning for a draft recommendation.
    """

    explanations = []

    # -------------------------
    # Tier explanation
    # -------------------------
    tier_map = build_position_tiers(all_players)
    tier_info = get_tier_info(player, tier_map, draft_state)

    if tier_info["tier_remaining"] <= 1:
        explanations.append(
            f"LAST remaining Tier {player.tier} {player.position} → high urgency"
        )
    elif tier_info["tier_remaining"] <= 3:
        explanations.append(
            f"Tier {player.tier} {player.position} is thinning ({tier_info['tier_remaining']} left)"
        )

    # -------------------------
    # ADP explanation
    # -------------------------
    current_pick = getattr(draft_state, "current_pick", 1)
    adp_gap = player.adp - current_pick if player.adp is not None else None

    if adp_gap is not None:
        if adp_gap <= 0:
            explanations.append("ADP value: already past expected draft range (must pick)")
        elif adp_gap <= 5:
            explanations.append(f"ADP value: +{abs(adp_gap):.0f} pick urgency")
        elif adp_gap <= 10:
            explanations.append(f"ADP value: moderate reach safety (+{abs(adp_gap):.0f})")

    # -------------------------
    # Team need explanation
    # -------------------------
    roster = draft_state.get_team_roster(team_id)
    position_counts = {}

    for p in roster:
        position_counts[p.position] = position_counts.get(p.position, 0) + 1

    need = position_counts.get(player.position, 0)

    if need == 0:
        explanations.append(f"Fills critical {player.position} need")
    elif need == 1:
        explanations.append(f"Adds depth at {player.position}")

    # -------------------------
    # Risk / upside signals
    # -------------------------
    if getattr(player, "risk", 0) >= 7:
        explanations.append("High injury/volatility risk")

    if getattr(player, "upside", 0) >= 8:
        explanations.append("High upside ceiling")

    return explanations