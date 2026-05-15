class DraftState:
    def __init__(self):
        self.drafted_players = []
        self.current_pick = 1

    def draft_player(self, player):
        self.drafted_players.append(player)

    def is_drafted(self, player):
        return player in self.drafted_players