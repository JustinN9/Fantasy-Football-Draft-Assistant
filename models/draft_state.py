class DraftState:
    def __init__(self):
        self.drafted_players = []
        self.pick_history = []
        self.current_pick = 1

    def draft_player(self, player):
        self.pick_history.append(player.position)
        self.drafted_players.append(player)
        self.current_pick += 1

    def is_drafted(self, player):
        return player in self.drafted_players