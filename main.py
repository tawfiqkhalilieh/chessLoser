import chess
import chess.engine
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
from constants import board as board
from player import ACCOUNTS
from utils.login import login
from utils.move import move as chess_move
from utils.options import driver
from utils.update_board import update_board
from utils.get_last_move import get_last_move
from utils.next_game import next_game
from utils.is_ended import is_ended
from utils.first_game import join_first_game
import sys
import random

engine = chess.engine.SimpleEngine.popen_uci("fish.exe")

# pickup the user we want to use from the file call
# python main.py {account number}
if sys.argv:
    USERNAME = ACCOUNTS[int(sys.argv[1])-1][0]
    PASSWORD =  ACCOUNTS[int(sys.argv[1])-1][1]
else:
    USERNAME = ACCOUNTS[0][0]
    PASSWORD =  ACCOUNTS[0][1]

chess_board: chess.Board | None = None

# create a webdriver instance
actions: ActionChains = ActionChains(driver)

# navigate to the computer page
driver.get("https://www.chess.com/play/computer")

driver.switch_to.window(list(driver.window_handles)[0])


while driver.find_elements(By.CSS_SELECTOR, "[data-cy='modal-first-time-button']"):
    pass

# login ( using the chess.com account from player.py )
login(driver=driver)

# join the first game and wait until the game starts
join_first_game(driver=driver)

def game(play_as_white):

    def get_worst_move():
        # Get all legal moves
        moves = list(chess_board.legal_moves)

        # Evaluate each move and store the score and the move in a list
        scores = []
        for move in moves:
            chess_board.push(move) # Make the move on the board
            info = engine.analyse(chess_board, chess.engine.Limit(time=0.1)) # Analyse the position
            chess_board.pop() # Unmake the move
            scores.append((info["score"], move)) # Append the score and the move to the list

        # Sort the list by score (ascending order)
        scores.sort(key=lambda x: x[0].white() if play_as_white else x[0].black())
        
        # Pick the first element of the list, which has the lowest score
        worst_score, worst_move = scores[0]

        chess_board.push(worst_move)
        return str(worst_move) 
    
    # move the piece on chess.com
    def move_on_board(result):
        try:
            chess_move(driver=driver,actions=actions, frm=str(result)[0] + str(result)[1], to=str(result)[2] + str(result)[3], play_as= "white" if play_as_white else "black")
        except Exception as e:
            print(result)
            print(e)
            if not is_ended(driver=driver) and update_board(driver=driver, chess_board=chess_board) > 2:
                move_on_board(get_worst_move())

    move_on_board(get_worst_move())

while True:
    try:
        # input("Click to start")
        print("game started")

        print("Virtual Board Created")
        chess_board = chess.Board()

        print("fetching users")
        
        play_as_white: bool = 'flipped' not in driver.find_element(By.ID, 'board-single').get_attribute('class')

        print("Writing the opponent name")
        # write the usernames in a text file to share them with chess.com
        with open('players.txt', "a") as fhandle:
            fhandle.write("\n"+ [ k.text for k in driver.find_elements(By.CSS_SELECTOR, '[data-test-element="user-tagline-username"]')][0] )

        print("waiting for the game to start")

        if play_as_white:
            game(play_as_white)

        while not driver.find_elements(By.CLASS_NAME, "selected"):
            time.sleep(1)
            print("still waiting")
            if is_ended(driver):
                break

        print("first move played")
        while not is_ended(driver):
            try:
                if driver.find_elements(By.CLASS_NAME, 'alerts-message'):
                    driver.get(driver.current_url)
                last_move = get_last_move(driver, 'black' if play_as_white else 'white')
                # fetch the last move and push it to the virtual chess board
                while not last_move:
                    last_move = get_last_move(driver, 'black' if play_as_white else 'white')
                    if is_ended(driver):
                        break

                chess_board.push_san(
                    last_move
                )

                # play engine move
                game(play_as_white=play_as_white)
            except Exception as e:
                print(e)
                update_board(driver=driver, chess_board=chess_board)
        print("Game ended")
        next_game(driver,driver.current_url)
    except Exception as e:
        print(e)
        update_board(driver=driver, chess_board=chess_board)
        if is_ended(driver):
            next_game(driver,driver.current_url)