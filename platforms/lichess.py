import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from random import randint

class Lichess:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver = webdriver.Firefox()
        self.auto = False

    def find_color(self):
        pass

    def log_in(self):
        pass

    """
    Returns ordered list of all moves that have been played
    """
    def read_moves(self):
        pass

    def perform_move(self, move):
        pass

    def quit(self):
        self.driver.quit()
