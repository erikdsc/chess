from selenium import webdriver
import chess
import chess.engine
import os
import threading
from random import randint

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

#gocoxin352@goqoez.com

class MagnusCarlsen(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  driver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self._stop_event = threading.Event()
        self.driver = driver
        self.quit_game = False

    def stop(self):
        self.quit_game = True
        #self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    """
    Checks if the closest coordinate-digit on the board equals to 1
    Returns:
        0 if black
        1 if white
    """
    def findColor(self):
        first_digit= self.driver.find_element_by_xpath("//*[@x='0.75' and @y='90.75']")
        return first_digit.text == "1"

    """
    Returns ordered list of all moves that have been played
    """
    def readMoves(self):
        try:
            registered_moves = []
            move_list = self.driver.find_element_by_tag_name("vertical-move-list")
            whole_moves = move_list.find_elements_by_class_name("move")
            for moves in whole_moves:
                for single_move in moves.find_elements_by_xpath("div[contains(@class, ' node')]"):
                    registered_moves.append(single_move.text)
            return registered_moves
        except:
            self.quit_game = True
            time.sleep(1)
            input("trykk enter når det neste gamet er klart\n")
            t.run()

    def performMove(self, move):
        letters = {
            "a" : "1", "b" : "2", "c" : "3", "d" : "4",
            "e" : "5", "f" : "6", "g" : "7", "h" : "8"
        }

        board = self.driver.find_element_by_tag_name("chess-board")
        board_rect = board.rect
        board_x = board_rect["x"]
        board_y = board_rect["y"]
        cell_lengths = board_rect["width"] / 8

        origin = letters[move[0]] + move[1]
        board.find_element_by_xpath("div[starts-with(@class, 'piece ') and " + \
                                        "contains(@class, '%s')]" % origin).click()
        time.sleep(randint(0,100) / 1000)
        try:
            dest = letters[move[2]] + move[3]
            destination = self.driver.find_element_by_xpath("//*[starts-with(@class, "+\
                "'hint ') and contains(@class, '%s')]" % dest)
            action = webdriver.ActionChains(self.driver)
            action.move_to_element(destination).click().perform()
        except:
            dest = letters[move[2]] + move[3]
            self.driver.find_element_by_xpath("//*[starts-with(@class, 'piece ')" +\
                    "and contains(@class, 'square-"+dest+"')]").click()

    def run(self):
        self.quit_game = False
        current_movelist = self.readMoves()
        prev_movelist = []
        color = self.findColor()
        board = chess.Board()
        while not (board.is_game_over() or self.quit_game):
            while (prev_movelist == current_movelist or \
                    len(current_movelist) % 2 == color):
                time.sleep(0.2)
                current_movelist= self.readMoves()
                if (self.quit_game or board.is_game_over()):
                    return
            for i in range(len(current_movelist)-len(prev_movelist)):
                print("Detected Move: \t",end="")
                print(current_movelist[len(prev_movelist)+i])
                board.push_san(current_movelist[len(prev_movelist)+i])
            
            best_move = engine.play(board, chess.engine.Limit(time=1000*randint(1,25) / 1000)).move
            #time.sleep(randint(0,20) / 10)
            #if randint(0,10) > 9:
            #    time.sleep(5)
            best_move = str(board.parse_san(str(best_move)))
            print("Best move: \t %s" % best_move)

            if len(best_move) == 4:
                self.performMove(best_move)
            else:
                print("promote or error")

            prev_movelist = current_movelist.copy()
        print("Check mate!")
     

if __name__ == "__main__":
    try:
        path = os.getcwd()
        engine = chess.engine.SimpleEngine.popen_uci(path+'/stockfish')
        driver = webdriver.Firefox()
        driver.get("http://www.chess.com/play/computer")
        assert "Chess" in driver.title
        input("klar?")

        t = MagnusCarlsen(driver)#(target=chess_player, args=(driver, ))
        t.start()
        inp = ""
        while (inp != "q"):
            inp = input("Type 'q' for exit\nType 'n' for new\n") 
            if inp == 'n':
                t.stop()
                #t.join()
                input("trykk enter når det neste gamet er klart\n")
                t.run()
        t.stop()
        t.join()
        
    except Exception as e:
        print(e)
        t.stop()
        t.join()
    finally:
        engine.quit()
        driver.quit()
        driver.close()
