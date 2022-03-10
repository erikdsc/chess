import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randint

class ChessCom:
    def __init__(self):
        self.driver = webdriver.Firefox()

    """
    Checks if the closest coordinate-digit on the board equals to 1
    Returns:
        false if black
        true if white
    """
    def find_color(self):
        return self.driver.find_element(By.XPATH, "//*[@x='0.75' and @y='90.75']") == '1'

    def log_in(self):
        self.driver.get("https://www.chess.com/login_and_go")
        with open("accounts/chesscom.txt") as f:
            accounts = [a.split() for a in f.readlines()] 
            #select account if many are specified
            if len(accounts) > 1:
                print("Available accounts:")
                for n, a in enumerate([a for a,_,_ in accounts]):
                    print(n+1, ":", a) 
                #NB: usikker konvertering
                acc_n = int(input("enter the number of the account you want to log in with"))
            else:
                acc_n = 1
            self.driver.find_element(By.ID, "username").send_keys(accounts[acc_n-1][1])
            self.driver.find_element(By.ID, "password").send_keys(accounts[acc_n-1][2])
            self.driver.find_element(By.ID, "login").click()

    """
    Returns ordered list of all moves that have been played
    """
    def read_moves(self):
        try:
            registered_moves = []
            move_list = self.driver.find_element(By.TAG_NAME, "vertical-move-list")
            whole_moves = move_list.find_elements(By.CLASS_NAME, "move")
            for moves in whole_moves:
                for single_move in moves.find_elements(By.XPATH, "div[contains(@class, ' node')]"):
                    registered_moves.append(single_move.text)
            return registered_moves
        except Exception as e:
            print(e)

    def perform_move(self, move):
        board = self.driver.find_element(By.TAG_NAME, "chess-board")
        board_rect = board.rect
        board_x = board_rect["x"]
        board_y = board_rect["y"]
        cell_lengths = board_rect["width"] / 8
        origin = str(ord(move[0])-96) + move[1]
        board.find_element(By.XPATH, "div[starts-with(@class, 'piece ') and " + \
                                        "contains(@class, '%s')]" % origin).click()
        try: 
            time.sleep(randint(20,100) / 1000)
            dest = str(ord(move[2])-96) + move[3]
            destination = self.driver.find_element(By.XPATH, "//*[starts-with(@class, "+\
                "'hint ') and contains(@class, '%s')]" % dest)
            action = webdriver.ActionChains(self.driver)
            action.move_to_element(destination).click().perform()
        except Exception as e:
            print("exception in perform_move:")
            print(e)
            dest = str(ord(move[2])-96) + move[3]
            self.driver.find_element(By.XPATH, "//*[starts-with(@class, 'piece ')" +\
                    "and contains(@class, 'square-"+dest+"')]").click()

    def quit(self):
        self.driver.quit()
