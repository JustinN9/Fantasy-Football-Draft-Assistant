from simulation.snake_draft import SnakeDraftSimulator
from models.draft_state import DraftState

class DraftEngine:
    def __init__(self, players, num_teams=10):
        self.players = players
        self.num_teams = num_teams

    def run(self, rounds=5): 
        draft_state = DraftState() 
        
        simulator = SnakeDraftSimulator( 
            players=self.players, 
            draft_state=draft_state, 
            num_teams=self.num_teams 
        ) 
        
        for _ in range(rounds): 
            simulator.simulate_pick() 
            
        return draft_state