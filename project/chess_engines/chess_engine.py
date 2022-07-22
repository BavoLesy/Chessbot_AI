#!/usr/bin/python3
from project.chess_engines.uci_engine import UciEngine
import chess
from project.chess_agents.chess_agent import ChessAgent
from project.chess_utilities.chess_utility import ChessUtility

if __name__ == "__main__":
    # Create your utility
    utility = ChessUtility()
    # Create your agent
    agent = ChessAgent(utility, 5.0)
    # Create the engine
    engine = UciEngine("Example engine", "Bavo", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
