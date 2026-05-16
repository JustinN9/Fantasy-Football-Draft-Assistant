REPLACEMENT_VALUES = {
    "QB": 250,
    "RB": 180,
    "WR": 170,
    "TE": 140
}


def calculate_vbd(player):

    position = player.position

    if position not in REPLACEMENT_VALUES:
        return 0

    replacement_value = REPLACEMENT_VALUES[position]

    return player.projected_points - replacement_value