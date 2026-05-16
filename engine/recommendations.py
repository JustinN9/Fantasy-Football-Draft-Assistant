from engine.scoring import calculate_draft_score

def get_recommendations(players, draft_state, top_n=5):
    available = [
        p for p in players
        if not draft_state.is_drafted(p)
    ]

    scored = [
        (p, calculate_draft_score(p, draft_state, players))
        for p in available
    ]

    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:top_n]