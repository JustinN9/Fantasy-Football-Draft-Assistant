from engine.scoring import calculate_draft_score

def get_recommendations(players, draft_state, top_n=5):

    # Filter Available Players
    available = [
        p for p in players
        if not draft_state.is_drafted(p)
    ]

    if not available:
        return []

    # Score All Players
    scored = []

    for p in available:
        try:
            score = calculate_draft_score(p, draft_state, players)
            scored.append((p, score))
        except Exception as e:
            # Prevents bad player from breaking entire draft
            continue

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Return top n
    return scored[:top_n]