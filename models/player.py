class Player:
    def __init__(
        self,
        name,
        position,
        team,
        projected_points,
        adp,
        upside,
        risk,
        tier
    ):
        self.name = name
        self.position = position
        self.team = team
        self.projected_points = float(projected_points)
        self.adp = float(adp)
        self.upside = float(upside)
        self.risk = float(risk)
        self.tier = int(tier)

        self.vbd = 0