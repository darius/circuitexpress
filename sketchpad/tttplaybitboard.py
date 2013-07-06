"""
Rewrite of tttplay using a bitboard representation as
inspired by https://gist.github.com/pnf/5924614
"""

def human_vs_puter(grid=None):
    tictactoe(human_play, negamax_play, grid)

def tictactoe(play_X, play_O, grid=None):
    grid = grid or empty_grid
    players = ('X', play_X), ('O', play_O)
    while True:
        (mark, play), (prev_mark, _) = players
        print ansi_clear_screen
        show(grid, (mark, prev_mark))
        if is_won(grid):
            print prev_mark, "wins."
            break
        if not successors(grid):
            print "A draw."
            break
        grid = play(grid, mark)
        players = players[::-1]

ansi_clear_screen = '\x1b[2J\x1b[H'


# Utility

def average(ns):
    return float(sum(ns)) / len(ns)

def memo(f):
    table = {}
    def memo_f(*args):
        try:
            return table[args]
        except KeyError:
            table[args] = value = f(*args)
            return value
    return memo_f


# Strategies. They all presume the game's not over.

def human_play(grid, mark):
    while True:
        try:
            move = int(raw_input(mark + " move? [1-9] "))
        except ValueError:
            pass
        else:
            if 1 <= move <= 9:
                successor = apply_move(grid, from_human_move_number(move))
                if successor: return successor
        print "Hey, that's illegal."

def negamax_play(grid, mark):
    return pick_successor(grid)

def pick_successor(grid):
    return min(successors(grid),
               key=lambda succ: (evaluate(succ), drunk_value(succ)))

@memo
def drunk_value(grid):
    "Return expected value to the player if both players play at random."
    if is_won(grid): return -1
    succs = successors(grid)
    return -average(map(drunk_value, succs)) if succs else 0

@memo
def evaluate(grid):
    "Return the value for the player to move, assuming perfect play."
    if is_won(grid): return -1
    succs = successors(grid)
    return -min(map(evaluate, succs)) if succs else 0
    

# Bit-board representation: a pair of bitsets (p, q),
# p for the player to move, q for their opponent.
# Least significant bit is the lower-right square; msb is upper-left.
# (Differs from the human move numbering for the sake of nice octal constants.)

empty_grid = 0, 0

def is_won((p, q)):
    "Did the latest move win the game?"
    return any((q & way) == way for way in ways_to_win)

ways_to_win = (0700, 0070, 0007, 0444, 0222, 0111, 0421, 0124)

def successors(grid):
    "Return the possible grids resulting from p's moves."
    return filter(None, (apply_move(grid, move) for move in range(9)))

def apply_move((p, q), move):
    bit = 1 << move
    return (q, p | bit) if 0 == (bit & (p | q)) else None

def from_human_move_number(n):
    "Convert from a move numbered 1..9 in top-left..bottom-right order."
    return 9 - n

def show(grid, marks='XO'):
    print view(grid, marks)
    print

def view((bits1, bits2), (mark1, mark2)):
    "Show a grid human-readably."
    squares = (mark1 if bit1 else mark2 if bit2 else '.'
               for bit1, bit2 in zip(*map(player_bits, (bits1, bits2))))
    return '\n'.join(' '.join(next(squares) for col in range(3))
                     for row in range(3))

def player_bits(bits):
    return ((bits >> i) & 1 for i in reversed(range(9)))

    
## print view((0700, 0060), 'XO')
#. X X X
#. O O .
#. . . .
#. 
## for succ in successors((0610, 0061)): show(succ, 'XO')
#. O O .
#. X X O
#. . O X
#. 
#. O O .
#. X X O
#. O . X
#. 
#. O O O
#. X X O
#. . . X
#. 
#. 

## print view((0104, 0420), 'XO')
#. O . X
#. . O .
#. X . .
#. 
## print view(negamax_play((0104, 0420), 'X'), 'OX')
#. O . X
#. . O .
#. X . X
#. 


if __name__ == '__main__':
    human_vs_puter()
