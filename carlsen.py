import chess
import chess.engine
import os
import threading
import time
from random import randint
from platforms.chesscom import ChessCom
from platforms.lichess import Lichess

class MagnusCarlsen(threading.Thread):
    """verdens beste sjakkspiller"""

    def __init__(self, platform, tkinter_root=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.platform = platform
        self.gui = tkinter_root
        self.engine = chess.engine.SimpleEngine.popen_uci(os.getcwd()+"/stockfish")
        self.auto = False
        self.play_move = False
        self._stop_event = threading.Event()
        self._playing_event = threading.Event()

    def stop(self):
        self._stop_event.set()
        self.terminate_game()

    def stopped(self):
        return self._stop_event.is_set()

    def new_game(self):
        self._playing_event.set()

    def terminate_game(self):
        self._playing_event.clear()

    def is_playing(self):
        return self._playing_event.is_set()

    def toggle_auto(self):
        self.auto = not self.auto
        self.play_move = True

    def play_best_move(self):
        """Same as toggle_auto() but only runs once"""
        self.play_move = True

    def display_detected_move(self, move: str):
        if self.gui is None:
            print("Detected move: " + move)
        else:
            self.gui.set_detected_move(move)
            
    def display_best_move(self, move: str):
        if self.gui is None:
            print("Best move:     " + move)
        else:
            self.gui.set_best_move(move)
            
    
    def update_board(self, board, move_list):
        """Resets the previous board and inserts all moves again"""
        board.reset()
        for move in move_list:
            board.push_san(move)
        return board

    def run(self):
        while True: 
            if self.is_playing():
                #setup
                color = self.platform.find_color()
                board = chess.Board()
                move_count = 0
                #playing
                while self.is_playing():
                    move_list = self.platform.read_moves()
                    if len(move_list) > move_count or self.play_move:
                        #print(f"Detected move: {move_list[-1]}")
                        self.display_detected_move(move_list[-1])
                        move_count = len(move_list)
                        if (move_count % 2 == color):
                            board = self.update_board(board, move_list)
                            best_move = self.engine.play(board, chess.engine.Limit(time=randint(80,200) / 1000)).move
                            #print("Best move:     %s" % board.san(best_move))
                            self.display_best_move(board.san(best_move))
                            if self.auto or self.play_move:
                                best_move = str(board.parse_san(str(best_move)))
                                if len(best_move) == 4:
                                    self.platform.perform_move(best_move)
                                else:
                                    print("promote or error")
                                if self.play_move:
                                    self.play_move = False
                    time.sleep(0.1)
            if self.stopped():
                break
            time.sleep(0.5)
        self.engine.quit()
        self.platform.quit()
    
    @staticmethod
    def play(platform):
        path = os.getcwd()
        platform.log_in()
        t = MagnusCarlsen(platform)
        t.start()
        try:
            print("Enter 'q' to exit,\nEnter 's' to start analysis,\nEnter 't' to stop analysis,")
            print("Enter 'a' to toggle automatic moves:\n\n")
            inp = ""
            while (inp != "q"):
                inp = input("")
                if   inp == 's':
                    print("Analyzing game... Remember to enter 't' before exiting the board!")
                    t.new_game()
                elif inp == 'a':
                    print("Automatic moves enabled.")
                    t.toggle_auto()
                elif inp == 't':
                    t.terminate_game()
                    print("Analysis stopped.")
            print("\nExiting...")
            if t.is_alive():
                t.stop()
                t.join()
        finally:
            if t.is_alive():
                t.stop()

if __name__ == "__main__":
    MagnusCarlsen.play(ChessCom())

