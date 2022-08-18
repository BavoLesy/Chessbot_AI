#!/usr/bin/python3
from project.chess_engines.uci_engine import UciEngine
from project.chess_agents.chess_agent import ChessAgent
from project.chess_utilities.chess_utility import ChessUtility

if __name__ == "__main__":
    # Create your utility
    utility = ChessUtility()
    # Create your agent
    agent = ChessAgent(utility, 15.0)
    # Create the engine
    engine = UciEngine("UCI Engine", "Bavo_Oliver", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
