# chess
This repository contains code to automatically analyze boards in chess.com and lichess.com and suggest the best moves.


## Software prerequisites:
#### Stockfish:
Download from https://stockfishchess.org/download/ and place it in the same directory as chesscom.py.  
NB: must be named "stockfish"

#### Python-chess  
`pip install chess `

#### Selenium
`pip install selenium `  

#### geckodriver
https://github.com/mozilla/geckodriver/releases

<br><br>
## Setting up automatical log ins
By adding your accounts to the csv files in the account folder, you can make the script automatically log you in.
The format is:  
`username email@domain.com password`  


## Website settings

### The following settings must be set for the script to work with chess.com:
 * **Board and pieces**
   * **Coordinates:** Inside board
   * **Piece notation:** Text
   * **Move method:** NOT Drag pieces only
   * **Show legal moves:** On (For automatic moves) 
##
