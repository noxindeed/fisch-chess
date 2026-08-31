# FISCH CHESS

> chess built from scratch, for the terminal.

This is a lightweight chess game written in Python and played entirely inside the terminal(v1).

## ✦ Features
```
[-] local two-player chess 
[-] simple computer opponent 
[-] legal move validation 
[-] check + checkmate 
[-] castling 
[-] en passant 
[-] pawn promotion 
[-] stalemate + draw detection 
[-] undo / redo 
[-] move history 
[-] FEN loading 
[-] puzzle mode 
```

chess logic is implemented inside the project itself insetad of relying on Stockish, Lichess, Chess(dot)com or another chess library/service
## ✦ Installation

You need:
`Python 3.11+`

Install Fisch Chess from PyPI:

> `pip install fisch-chess`

Then run:

> `fisch`

To update later:

> `pip install -U fisch-chess`

## ✦ Run from source

Clone the repo:

> `git clone https://github.com/noxindeed/fisch-chess/`
> `cd fisch-chess`

Optional, but recommended is to run it in a venv.

From the project root:

`python3 -m src.main`

You should get:

```text
FISCH CHESS
===========

1. New Game (two players, offline)
2. New Game (vs not so smart AI)
3. Load Position (FEN)
4. Puzzle Mode
5. Quit
```

## moves

Fisch uses coordinate notation.
So,

`e2e4` means: `e2 → e4`

Knight example: `g1f3`

Promotion: `e7e8q`

Promotion pieces:

- q  queen
- r  rook
- b  bishop
- n  knight

## ✦ Commands

While playing:

u  -  undo
r  -  redo
h  -  move history
f  -  show FEN
n  -  new game
q  -  back to menu

## ✦ Project structure
```
fisch-chess/
│
└── src/
    ├── main.py
    ├── engine.py
    ├── board.py
    ├── moves.py
    ├── pieces.py
    └── __init__.py
```

- main.py

    Terminal UI, menus, commands, puzzles and the computer player.

- engine.py

    Game state, legal move filtering, checks, draws, FEN, history and move application.

- board.py

    Board representation, coordinates and attack detection.

- moves.py

    Pseudo-legal move generation for every piece.

- pieces.py

    Piece/color helpers.

## ✦ Future plans
V2
```
├── online multiplayer
├── create / join game codes
├── real-time moves
├── reconnecting
├── resignation
└── draw offers
```
later
```
├── rematches
├── chess clocks
├── spectators
├── saved games
├── better puzzles
├── stronger AI
├── game history
└── web client
```
