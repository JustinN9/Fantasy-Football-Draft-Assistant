from engine.scoring import calculate_draft_score


def cpu_score(player, draft_state, all_players, current_pick, team_id):
    """
    Unified CPU scoring.

    This now directly uses the main draft intelligence engine.
    """

    return calculate_draft_score(
        player,
        draft_state,
        all_players,
        team_id
    )