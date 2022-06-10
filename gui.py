import tkinter as tk
import time
import asyncio
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
        self.platform = platform()
        self.platform.log_in()
        self.engine = MagnusCarlsen(self.platform, tkinter_root=self)
        self.engine.start()
        self.switch_frame(FrmSetupConfirmation)

    def new_game(self):
        self.switch_frame(FrmGameRunning)
        self.engine.new_game()

    def toggle_automatic_moves(self):
        self.engine.toggle_auto()

    def play_best_move(self):
        self.engine.play_best_move()

    def terminate_game(self):
        self.engine.terminate_game()
        self.toggle_analyzate_button_text()

    def terminate_program(self):
        if self.engine.is_alive():
            self.engine.stop()
            self.platform.quit()
            self.engine.join()
            
    def main_menu(self):
        self.terminate_program()
        self.switch_frame(FrmStartPage)

    def set_detected_move(self, move: str):
        if isinstance(self._frame, FrmGameRunning):
            self._frame.set_detected_move(move)

    def set_best_move(self, move: str):
        if isinstance(self._frame, FrmGameRunning):
            self._frame.set_best_move(move)

    def toggle_analyzate_button_text(self):
        if isinstance(self._frame, FrmGameRunning):
            self._frame.toggle_analyze_button()

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
            text="Make sure you are logged in, website settings are correct \n"+\
                " and that you have a chess board ready with at least \n"+\
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
        self.lbl_detected_move = None
        self.lbl_best_move = None
        self.btn_analyze = None
        self.lbl_title = tk.Label(
            self,
            font=("Arial", 17),
            text="Analyzing game...\n"+\
                 "Remember to terminate game before\nleaving the board!"
        )
        self.lbl_title.pack(side="top", pady=10)
        frm_button_grid = tk.Frame(self)
        self.lbl_detected_move = tk.Label(
            frm_button_grid,
            text="Detected move:\n",
            font='sans 11 bold')
        self.lbl_best_move = tk.Label(
            frm_button_grid,
            text="Best move:\n", 
            font='sans 11 bold')
        self.lbl_detected_move.grid(row=2, column=2, sticky="NNNNNNS")
        self.lbl_best_move.grid(row=3, column=2, sticky="NNNNNNS")
        self.btn_analyze = tk.Button(
            frm_button_grid,
            text="Stop\nanalyzing",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.terminate_game
        )
        self.btn_analyze.grid(row=2, column=0,padx=5, pady=5)
        tk.Button(
            frm_button_grid,
            text="Exit\nprogram",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.terminate_program
        ).grid(row=3, column=0,padx=5, pady=5)
        frm_button_grid.pack(side="left", padx=10, pady=10, ipadx=10)
        tk.Button(
            frm_button_grid,
            text="Toggle\nautomatic\nmoves",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.toggle_automatic_moves
        ).grid(row = 2, column = 1,padx=5, pady=5)
        tk.Button(
            frm_button_grid,
            text="Play\nbest\nmove",
            width=15,
            height=5,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=master.play_best_move
        ).grid(row = 3, column = 1,padx=5, pady=5)
        tk.Button(
            self,
            text="<",
            width=1,
            height=1,
            fg="black",
            font='sans 10 bold',
            borderwidth=1,
            command=master.main_menu
        ).place(x=10, y=10)

    def set_detected_move(self, move: str):
        self.lbl_detected_move.configure(text="Detected move:\n" + move)
    
    def set_best_move(self, move: str):
        self.lbl_best_move.configure(text="Best move:\n" + move)

    def toggle_analyze_button(self):
        if self.btn_analyze.cget("text")[:4] == "Stop":
            self.lbl_title.configure(text="Analyzation stopped!\n"+\
                "Remember to terminate game before\nleaving the board!")
            self.btn_analyze.configure(text="Start\nanalyzing")
        else:
            self.lbl_title.configure(text="Analyzing game...\n"+\
                "Remember to terminate game before\nleaving the board!")
            self.btn_analyze.configure(text="Stop\nanalyzing")
            

if __name__ == "__main__":
    app = App()
    app.title("Chess cheater")
    app.mainloop()


