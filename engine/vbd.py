REPLACEMENT_VALUES = {
    "QB": 250,
    "RB": 180,
    "WR": 170,
    "TE": 140
}

def calculate_vbd(player):
    replacement = REPLACEMENT_VALUES[player.position]
    return player.projected_points - replacement