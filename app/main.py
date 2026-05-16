from data.loader import load_players
from models.draft_state import DraftState
from engine.live_draft import LiveDraftAssistant


def main():
    players = load_players()
    draft_state = DraftState()

    assistant = LiveDraftAssistant(players, draft_state)

    print("\nFANTASY FOOTBALL DRAFT ASSISTANT\n")

    while True:
        assistant.display_recommendations()
        assistant.show_roster()

        print("\nCommands:")
        print("- Enter player name to draft")
        print("- 'search <name>' to find players")
        print("- 'exit' to quit")

        user_input = input("\n> ").strip()

        if user_input.lower() == "exit":
            break

        # SEARCH MODE
        if user_input.lower().startswith("search "):
            query = user_input[7:]
            results = assistant.search_players(query)

            print("\nSearch results:")
            for p in results:
                print(f"- {p.name} ({p.position}, {p.team})")

            continue

        # SHOW ROSTER ONLY
        if user_input.lower() == "roster":
            assistant.show_roster()
            continue

        # DRAFT PLAYER
        assistant.draft_player_by_name(user_input)


if __name__ == "__main__":
    main()
