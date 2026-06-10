from engine.stochastic import apply_noise


def get_cpu_personality(team_id):

    personalities = {
        0: "USER",
        1: "RB_HEAVY",
        2: "WR_VALUE",
        3: "BALANCED",
        4: "AGGRESSIVE",
        5: "CONSERVATIVE",
        6: "BALANCED",
        7: "WR_VALUE",
        8: "RB_HEAVY",
        9: "AGGRESSIVE"
    }

    return personalities.get(team_id, "BALANCED")


def apply_personality_modifier(player, base_score, personality):

    position = player.position
    score = base_score

    # ---------------- RB HEAVY ----------------
    if personality == "RB_HEAVY":
        if position == "RB":
            score *= 1.15
        elif position == "WR":
            score *= 0.95

    # ---------------- WR VALUE ----------------
    if personality == "WR_VALUE":
        if position == "WR":
            score *= 1.10
        elif position == "RB":
            score *= 0.97

    # ---------------- AGGRESSIVE ----------------
    if personality == "AGGRESSIVE":
        score += getattr(player, "upside", 0) * 2

    # ---------------- CONSERVATIVE ----------------
    if personality == "CONSERVATIVE":
        score -= getattr(player, "risk", 0) * 1.5

    # ---------------- RANDOMNESS LAYER ----------------
    # THIS is what creates draft variation
    score = apply_noise(score, 0.04)

    return score