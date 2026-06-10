from engine.scoring import calculate_draft_score
from engine.explanations import explain_pick


def get_recommendations(player_pool, draft_state, all_players, team_id=0, top_n=5):
    """
    Returns ranked players with explanations.
    """

    scored_players = []

    for player in player_pool:
        score = calculate_draft_score(
            player,
            draft_state,
            all_players,
            team_id
        )

        reasons = explain_pick(
            player,
            draft_state,
            all_players,
            team_id
        )

        scored_players.append({
            "player": player,
            "score": score,
            "reasons": reasons
        })

    scored_players.sort(key=lambda x: x["score"], reverse=True)

    return scored_players[:top_n]


def print_recommendations(recommendations):
    for r in recommendations:
        p = r["player"]
        print("\n--------------------")
        print(f"{p.name} ({p.position}) - Score: {r['score']}")
        print("Why:")

        for reason in r["reasons"]:
            print(f" - {reason}")