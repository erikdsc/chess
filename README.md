# chess
This repository contains code to automatically analyze boards in chess.com and lichess.com and sugges the best moves.  
The program can also be set to automatically move the pieces on the board for you.  

By combining [Selenium](https://selenium-python.readthedocs.io/) with [python-chess](https://python-chess.readthedocs.io/en/latest/), [stockfish](https://stockfishchess.org/download/) and native Python threads, I was able to create a script that could automatically find and perform the best chess moves available.  
With [tkinter](https://docs.python.org/3/library/tkinter.html), I was able to create an intuitive graphical interface for this script.

## Software prerequisites (to do):
#### Stockfish:
Download from https://stockfishchess.org/download/ and place it in the same directory as chesscom.py.  
NB: must be named "stockfish"

#### Python-chess  
`pip install chess `

#### Selenium
`pip install selenium `  

#### geckodriver
https://github.com/mozilla/geckodriver/releases

## Setting up automatical log ins
By adding your accounts to the csv files in the account folder, you can make the script automatically log you in.
The format is:  
`username email@domain.com password`  


## Website settings
The following settings must be set for the script to work!

### chess.com:
 * **Board and pieces**
   * **Coordinates:** Inside board
   * **Piece notation:** Text
   * **Move method:** NOT Drag pieces only
   * **Show legal moves:** On (For automatic moves) 

## Code explanation
There are three main python scripts that stands for most of the logic of this program: carlsen.py, the platform scripts, and the gui.py file.

### carlsen.py
carlsen.py is the main file of this repository and contains a class called MagnusCarlsen, which is responsible for the actual chess playing. The class inherits from threading.Thread and uses the [python-chess](https://python-chess.readthedocs.io/en/latest/) library along with information gathered from the platform-classes to solve chess positions.

### platform  
Since there are multiple chess platforms available, there are also multiple files with classes representing the platform. Common for all the classes is that they launch a Selenium instance to play chess online. The classes have specialized code to detect web elements and navigate the websites. The MagnusCarlsen class uses the platform classes to interact with the websites.

### gui.py
The guy.py file gives an alternative to the command-line interface provided by carlsen.py. This is done with the use of tkinter.
