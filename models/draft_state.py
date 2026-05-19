class DraftState:
    def __init__(self, num_teams=10):
        self.drafted_players = []
        self.pick_history = []
        self.current_pick = 1

        # Team rosters
        self.team_rosters = {
            i: [] for i in range(num_teams)
        }

    def draft_player(self, player, team_id):
        self.pick_history.append(player.position)
        self.drafted_players.append(player)

        self.team_rosters[team_id].append(player)

        self.current_pick += 1

    def is_drafted(self, player):
        return player in self.drafted_players

    def get_team_roster(self, team_id):
        return self.team_rosters.get(team_id, [])