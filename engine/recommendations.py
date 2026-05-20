from engine.scoring import (
    calculate_draft_score
)


def get_recommendations(
    players,
    draft_state,
    top_n=5,
    team_id=0
):

    available = [
        p for p in players
        if not draft_state.is_drafted(p)
    ]

    scored = []

    for player in available:

        score = (
            calculate_draft_score(
                player,
                draft_state,
                available,
                team_id
            )
        )

        scored.append(
            (player, score)
        )

    scored.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return scored[:top_n]