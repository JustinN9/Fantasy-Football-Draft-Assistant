import random

from engine.scoring import (
    calculate_draft_score
)

def cpu_score(
    player,
    draft_state,
    all_players,
    current_pick,
    team_id
):

    # Base draft intelligence
    score = calculate_draft_score(
        player,
        draft_state,
        all_players,
        team_id
    )

    # ADP realism
    adp_diff = abs(
        player.adp
        - current_pick
    )

    adp_bonus = max(
        0,
        10 - (adp_diff / 6)
    )

    score += adp_bonus

    # Mild randomness
    randomness = random.uniform(
        0.94,
        1.06
    )

    score *= randomness

    return round(score, 2)