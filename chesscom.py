from selenium import webdriver
import chess
import chess.engine
import os
import threading
import sys
from random import randint

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time



class MagnusCarlsen(threading.Thread):
    """verdens beste sjakkspiller"""

    def __init__(self,  driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = driver
        self.auto = False
        self._stop_event = threading.Event()
        

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    """
    Converts individual letters to a string of their position in the alphabet
    """
    @staticmethod
    def a_to_n(c):
        return str(ord(c)-96)

    def toggle_auto(self):
        self.auto = not self.auto

    """
    Checks if the closest coordinate-digit on the board equals to 1
    Returns:
        false if black
        true if white
    """
    def find_color(self):
        return self.driver.find_element_by_xpath("//*[@x='0.75' and @y='90.75']") == '1'

    """
    Returns ordered list of all moves that have been played
    """
    def read_moves(self):
        try:
            registered_moves = []
            move_list = self.driver.find_element_by_tag_name("vertical-move-list")
            whole_moves = move_list.find_elements_by_class_name("move")
            for moves in whole_moves:
                for single_move in moves.find_elements_by_xpath("div[contains(@class, ' node')]"):
                    registered_moves.append(single_move.text)
            return registered_moves
        except Exception as e:
            print(e)

    def perform_move(self, move):
        board = self.driver.find_element_by_tag_name("chess-board")
        board_rect = board.rect
        board_x = board_rect["x"]
        board_y = board_rect["y"]
        cell_lengths = board_rect["width"] / 8

        origin = self.a_to_n(move[0]) + move[1]
        board.find_element_by_xpath("div[starts-with(@class, 'piece ') and " + \
                                        "contains(@class, '%s')]" % origin).click()
        time.sleep(randint(0,100) / 1000)
        try:
            dest = self.a_to_n(move[2]) + move[3]
            destination = self.driver.find_element_by_xpath("//*[starts-with(@class, "+\
                "'hint ') and contains(@class, '%s')]" % dest)
            action = webdriver.ActionChains(self.driver)
            action.move_to_element(destination).click().perform()
        except Exception as e:
            print(e)
            dest = self.a_to_n(move[2]) + move[3]
            self.driver.find_element_by_xpath("//*[starts-with(@class, 'piece ')" +\
                    "and contains(@class, 'square-"+dest+"')]").click()

    """
    Resets the previous board and inserts all moves again
    """
    def update_board(self, board, move_list):
        board.reset()
        for move in move_list:
            board.push_san(move)
        return board

    def run(self):
        #oppsett
        color = self.find_color()
        board = chess.Board()
        move_count = 0
        
        #spill
        while not (board.is_game_over() or self.stopped()):
            move_list = self.read_moves()
            #nytt trekk:
            if len(move_list) > move_count:
                print(f"Detected move: {move_list[-1]}")
                move_count = len(move_list)
                #best move
                if (move_count % 2 == color):
                    board = self.update_board(board, move_list)
                    best_move = engine.play(board, chess.engine.Limit(time=randint(50,200) / 1000)).move
                    print("Best move:     %s" % board.san(best_move))
                    if self.auto:
                        best_move = str(board.parse_san(str(best_move)))
                        if len(best_move) == 4:
                            self.perform_move(best_move)
                        else:
                            print("promote or error")
            time.sleep(0.1)


if __name__ == "__main__":
    try:
        path = os.getcwd()
        engine = chess.engine.SimpleEngine.popen_uci(path+'/stockfish')
        driver = webdriver.Firefox()
        driver.get("https://www.chess.com/login_and_go")
        
        #login
        with open("accounts.txt") as f:
            accounts = [a.split() for a in f.readlines()] 
            #select account if many are specified
            if len(accounts) > 1:
                print("Available accounts:")
                for n, a in enumerate([a for a,_,_ in accounts]):
                    print(n, ":", a)
            
                #NB: usikker konvertering
                acc_n = int(input("enter the number of the account you want to log in with"))
            else:
                acc_n = 1
            print(acc_n)
            driver.find_element_by_id("username").send_keys(accounts[acc_n-1][1])
            driver.find_element_by_id("password").send_keys(accounts[acc_n-1][2])
            driver.find_element_by_id("login").click()

        t = MagnusCarlsen(driver)
        print("Type 'q' for exit,\nType 'n' for new,\nType 'a' to toggle automatic moves:\n\n") 
        inp = ""
        while (inp != "q"):
            inp = input("")
            if inp == 'n':
                if t.is_alive():
                    t.stop()
                    t.join()
                t.start()
            elif inp == 'a':
                t.toggle_auto()
        print("\nExiting...")
        t.stop()
        t.join()
    except Exception as e:
        print(e)
        t.stop()
        t.join()
    finally:
        time.sleep(3)
        engine.quit()
        driver.quit()
