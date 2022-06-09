import tkinter as tk
import time
from carlsen import MagnusCarlsen
from platforms.chesscom import ChessCom
from platforms.lichess import Lichess


class App:
    def __init__(self, master):
        self.master = master
        self.engine = None
        self.platform = None
        #initial interface
        self.lbl_title = tk.Label(
            text="To start, select one of the platforms below:", 
            master=self.master,
            font=("Arial", 17)
        )
        self.lbl_title.pack()
        self.frm_body = tk.Frame(master=window, width=90, height=2)
        btn_chesscom = tk.Button(
            master=self.frm_body,
            text="chess.com",
            width=25,
            height=10,
            fg="black",
            font='sans 11 bold',
            relief=tk.RAISED,
            borderwidth=3,
            command=self.start_engine(ChessCom)
        )
        btn_chesscom.pack(side=tk.LEFT, padx=10)
        btn_lichess = tk.Button(
            master=self.frm_body,
            text="lichess.com\n(Not implemented yet)",
            width=25,
            height=10,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
        )
        btn_lichess.pack(side=tk.RIGHT, padx=10, pady=10)
        self.frm_title.pack()
        self.frm_body.pack(fill=tk.X)

    def start_engine(self, platform):
        self.platform = platform
        self.platform.log_in()
        self.engine = MagnusCarlsen(platform)
        self.engine.start()
        self.lbl_title.config(
            text="Make sure you are logged in, website settings are correct \n "+\
                "and that you have a chess board ready!\n\n"+\
                "Press 'continue' when when everything is set up"
        )
        for widget in self.frm_body.winfo_children():
            widget.pack.forget()
        btn_continue = tk.Button(
            master=self.frm_body,
            text="Continue",
            width=25,
            height=10,
            fg="black",
            font='sans 11 bold',
            borderwidth=3,
            command=self.new_game
        )
        btn_continue.pack(padx=10, pady=10)
        print("TEST")

    def new_game(self):
        print("test")
        self.engine.new_game()
        pass

    def toggle_automatic_moves(self):
        self.engine.toggle_auto()
        pass

    def terminate_game(self):
        self.engine.terminate_game()
        pass

    def terminate_program(self):
        if self.engine.is_alive():
            self.engine.stop()
            self.engine.join()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Chess cheater")
    program = App(window)
    window.mainloop()


