import random
from engine.cpu_logic import cpu_score

class SnakeDraftSimulator:
    def __init__(self, players, draft_state, num_teams=10):
        self.players = players
        self.draft_state = draft_state
        self.num_teams = num_teams
        self.available_players = players.copy()
        self.current_round = 1
        self.current_pick = 1
        self.direction = 1  # 1 = forward, -1 = reverse

    def get_next_pick_order(self):
        if self.direction == 1:
            return list(range(self.num_teams))
        else:
            return list(range(self.num_teams - 1, -1, -1))

    def simulate_pick(self):
        pick_order = self.get_next_pick_order()

        for team in pick_order:
            if team == 0:
                # YOUR PICK (AI-controlled team)
                from engine.recommendations import get_recommendations

                recs = get_recommendations(
                    self.available_players,
                    self.draft_state,
                    top_n=1
                )

                player = recs[0][0]

            else:
                # CPU pick (simple logic for now)
                #player = random.choice(self.available_players)
                best_player = None
                best_score = float("-inf")

                for p in self.available_players:
                    score = cpu_score(p, self.draft_state, self.current_pick)

                if score > best_score:
                    best_score = score
                    best_player = p

                player = best_player


            self.draft_state.draft_player(player)
            self.available_players.remove(player)

            print(f"Round {self.current_round} - Team {team} picked {player.name}")

        self.current_pick += 1
        self.current_round += 1
        self.direction *= -1