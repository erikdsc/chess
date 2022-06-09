import tkinter as tk
import time
from carlsen import MagnusCarlsen
from platforms.chesscom import ChessCom
from platforms.lichess import Lichess


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.engine = None
        self.platform = None
        self._frame = None
        self.switch_frame(FrmStartPage)
    
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def start_engine(self, platform):
        #self.platform = platform()
        #self.platform.log_in()
        #self.engine = MagnusCarlsen(platform)
        #self.engine.start()
        self.switch_frame(FrmSetupConfirmation)

    def new_game(self):
        print("test")
        self.switch_frame(FrmGameRunning)
        #self.engine.new_game()

    def toggle_automatic_moves(self):
        #self.engine.toggle_auto()
        self.switch_frame(FrmStartPage)
        pass

    def terminate_game(self):
        #self.engine.terminate_game()
        print("TERMINATED")

    def terminate_program(self):
        if self.engine.is_alive():
            self.engine.stop()
            self.engine.join()

class FrmStartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(
            self,
            text="To start, select one\nof the platforms below:", 
            font=("Arial", 17),
        ).pack(side="top",pady=10)
        tk.Button(
            self,
            text="chess.com",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            relief=tk.RAISED,
            borderwidth=3,
            command= lambda: master.start_engine(ChessCom)
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            self,
            text="lichess.com\n\n(Not implemented)",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
        ).pack(side=tk.RIGHT, padx=10, pady=10)


class FrmSetupConfirmation(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(
            self,
            font=("Arial", 17),
            text="Make sure you are logged in, website settings are correct \n "+\
                "and that you have a chess board ready with at least \n"+\
                "one move already made!\n\n"+\
                "Press 'continue' when when everything is set up"
        ).pack()
        tk.Button(
            self,
            text="Continue",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.new_game
        ).pack(padx=10, pady=10)


class FrmGameRunning(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.detected_move = None
        self.best_move = None
        tk.Label(
            self,
            font=("Arial", 17),
            text="Analyzing game...\n"+\
                 "Remember to terminate game before\nleaving the board!"
        ).pack(side="top", pady=10)
        frm_button_grid = tk.Frame(self)
        self.detected_move = tk.Label(
            frm_button_grid,
            text="Detected move:\n",
            font='sans 11 bold')
        self.best_move = tk.Label(
            frm_button_grid,
            text="Best move:\n", 
            font='sans 11 bold')
        self.detected_move.grid(row=2, column=2, sticky="NNNNNNS")
        self.best_move.grid(row=3, column=2, sticky="NNNNNNS")
        tk.Button(
            frm_button_grid,
            text="Toggle\nautomatic\nmoves",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.toggle_automatic_moves
        ).grid(row = 2, column = 0,padx=5, pady=5)
        tk.Button(
            frm_button_grid,
            text="Stop\nanalyzing",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.terminate_game
        ).grid(row=2, column=1,padx=5, pady=5)
        tk.Button(
            frm_button_grid,
            text="Exit\nprogram",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.terminate_program
        ).grid(row=3, column=1,padx=5, pady=5)
        frm_button_grid.pack(side="left", padx=10, pady=10, ipadx=10)
    
    def set_detected_move(self, move: str):
        self.detected_move.configure(text="Detected move:\n" + move)
    
    def set_best_move(self, move: str):
        self.detected_move.configure(text="Best move:\n" + move)


if __name__ == "__main__":
    app = App()
    app.title("Chess cheater")
    app.mainloop()


