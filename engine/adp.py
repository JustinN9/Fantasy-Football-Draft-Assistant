def adp_pressure(player, current_pick):
    """
    ADP-based urgency system.
    Higher score = more urgent to draft now.
    """

    if not hasattr(player, "adp") or player.adp is None:
        return 0

    gap = player.adp - current_pick

    # Already "late" on ADP → must take
    if gap <= 0:
        return 12

    # About to disappear
    if gap <= 2:
        return 10

    if gap <= 5:
        return 7

    if gap <= 10:
        return 4

    if gap <= 15:
        return 2

    # Safe buffer
    return 0