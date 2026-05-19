from engine.cpu_logic import (
    cpu_score
)

from engine.recommendations import (
    get_recommendations
)


class SnakeDraftSimulator:
    def __init__(
        self,
        players,
        draft_state,
        num_teams=10
    ):
        self.players = players
        self.draft_state = draft_state
        self.num_teams = num_teams

        self.available_players = (
            players.copy()
        )

        self.current_round = 1
        self.current_pick = 1
        self.direction = 1

    def get_next_pick_order(self):
        if self.direction == 1:
            return list(
                range(self.num_teams)
            )

        return list(
            range(
                self.num_teams - 1,
                -1,
                -1
            )
        )

    def pick_cpu_player(
        self,
        team_id
    ):
        best_player = None
        best_score = float("-inf")

        for player in (
            self.available_players
        ):

            score = cpu_score(
                player,
                self.draft_state,
                self.available_players,
                self.current_pick,
                team_id
            )

            if score > best_score:
                best_score = score
                best_player = player

        return best_player

    def simulate_pick(self):

        pick_order = (
            self.get_next_pick_order()
        )

        for team in pick_order:

            if team == 0:
                recs = (
                    get_recommendations(
                        self.available_players,
                        self.draft_state,
                        top_n=1
                    )
                )

                player = (
                    recs[0][0]
                    if recs
                    else None
                )

            else:
                player = (
                    self.pick_cpu_player(
                        team
                    )
                )

            if player is None:
                continue

            self.draft_state.draft_player(
                player,
                team
            )

            self.available_players.remove(
                player
            )

            print(
                f"Round "
                f"{self.current_round} "
                f"- Team {team} "
                f"picked "
                f"{player.name} "
                f"({player.position})"
            )

            self.current_pick += 1

        self.current_round += 1
        self.direction *= -1