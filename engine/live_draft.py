from engine.recommendations import get_recommendations

class LiveDraftAssistant:
    def __init__(self, players, draft_state):
        self.players = players
        self.draft_state = draft_state

    def display_recommendations(self, top_n=5):
        recommendations = get_recommendations(
            self.players,
            self.draft_state,
            top_n=top_n
        )

        print("\nTop Recommendations:\n")

        for i, (player, score) in enumerate(recommendations, start=1):
            print(
                f"{i}. "
                f"{player.name} "
                f"({player.position}, {player.team}) "
                f"- Score: {score:.2f}"
            )

    def draft_player_by_name(self, name):
        name = name.strip().lower()

        matches = [
            p for p in self.players
            if p.name.lower() == name
            and not self.draft_state.is_drafted(p)
        ]

        if not matches:
            print("\nPlayer not found or already drafted.")
            return False

        player = matches[0]

        self.draft_state.draft_player(player)
        print(f"\nDrafted: {player.name}")

        return True

    def search_players(self, query, limit=5):
        query = query.lower()

        results = [
            p for p in self.players
            if query in p.name.lower()
            and not self.draft_state.is_drafted(p)
        ]

        return results[:limit]

    def show_roster(self):
        print("\nYOUR TEAM:")

        for p in self.draft_state.drafted_players:
            print(f"- {p.name} ({p.position})")