from collections import defaultdict


def build_position_tiers(all_players):
    """
    Build tier groups per position.
    Assumes player.tier exists (1 = best tier).
    """
    tiers = defaultdict(lambda: defaultdict(list))

    for p in all_players:
        if p.tier is None:
            continue
        tiers[p.position][p.tier].append(p)

    return tiers


def get_tier_info(player, tier_map, draft_state):
    """
    Returns tier context for a player.
    """

    position_tiers = tier_map.get(player.position, {})
    tier_players = position_tiers.get(player.tier, [])

    remaining = [
        p for p in tier_players
        if not draft_state.is_drafted(p)
    ]

    return {
        "tier_size": len(tier_players),
        "tier_remaining": len(remaining),
        "is_last_in_tier": len(remaining) == 1
    }


def tier_pressure_bonus(tier_info):
    """
    Rewards urgency when tiers are close to collapse.
    """

    remaining = tier_info["tier_remaining"]

    if remaining <= 1:
        return 10
    if remaining <= 2:
        return 6
    if remaining <= 4:
        return 3

    return 0


def tier_drop_risk(tier_info):
    """
    Penalizes waiting when tier is thinning.
    """

    remaining = tier_info["tier_remaining"]

    if remaining <= 2:
        return 4
    if remaining <= 4:
        return 2

    return 0