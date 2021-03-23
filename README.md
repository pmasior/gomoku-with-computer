# gomoku-with-computer
Simple game in which two players alternate turns placing a stone on an empty intersection. The winner is the first player who forms an unbroken line of exactly 5 stones horizontally, vertically, or diagonally.

![Gomoku screenshot](https://pmasior.github.io/images/gomoku-with-computer.png)

## How to run?
1. Install Python 3
	* Linux (Linux Mint, Ubuntu): python3 is probably installed in your system
	* Windows: Download Python 3 installer from [python.org](https://www.python.org/downloads/) and install it
2. Clone repository
    ```bash
    git clone https://github.com/pmasior/gomoku-with-computer.git
    ```
    or download repository from [GitHub.com](https://github.com/pmasior/gomoku-with-computer/archive/refs/heads/master.zip) and extract it
3. Run console and go to folder where you cloned the repository or extracted archive (folder with file `gomoku.py`)
    ```bash
    cd gomoku-with-computer
    ```
3. Install pygame
    * Linux:
      ```bash
      python3 -m pip install pygame
      ```
    * Windows:
      ```batch
      py -m pip install pygame
      ```
4. Run app
    * Linux:
      ```bash
      python3 ./gomoku.py
      ```
    * Windows:  
      ```batch
      py .\gomoku.py
      ```
