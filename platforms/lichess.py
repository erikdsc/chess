import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from random import randint

class Lichess:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.auto = False

    """
    Returns True if you are white
    """
    def find_color(self):
        return (self.driver.find_element(By.XPATH, "//coord[contains(text(), '1')]").location['y'] < \
        self.driver.find_element(By.XPATH, "//coord[contains(text(), '8')]").location['y'])

    def log_in(self):
        self.driver.get("https://lichess.org/login")
        with open("accounts/lichess.csv") as f:
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
            self.driver.find_element(By.ID, "form3-username").send_keys(accounts[acc_n-1][1])
            self.driver.find_element(By.ID, "form3-password").send_keys(accounts[acc_n-1][2])
            self.driver.find_element(By.CLASS_NAME, "submit.button").click()
        

    """
    Returns ordered list of all moves that have been played
    """
    def read_moves(self):
        try:
            registered_moves = []
            #move_list = self.driver.find_element(By.TAG_NAME, "l4x")
            moves = self.driver.find_elements(By.TAG_NAME, "u8t")
            for m in moves:
                registered_moves.append(m.text)
            return registered_moves
        except Exception as e:
            print(e)

    def perform_move(self, move):
        # TO DO
        pass

    def quit(self):
        self.driver.quit()

