import chess
import chess.engine

# Create a board and an engine
board = chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("fish.exe")

# Get all legal moves
moves = list(board.legal_moves)

# Evaluate each move and store the score and the move in a list
scores = []
for move in moves:
    board.push(move) # Make the move on the board
    info = engine.analyse(board, chess.engine.Limit(time=0.1)) # Analyse the position
    board.pop() # Unmake the move
    scores.append((info["score"], move)) # Append the score and the move to the list

# Sort the list by score (ascending order)
scores.sort(key=lambda x: x[0].white())

# Pick the first element of the list, which has the lowest score
worst_score, worst_move = scores[0]

# Print the result
print(f"The worst move is {worst_move} with score {worst_score}")
