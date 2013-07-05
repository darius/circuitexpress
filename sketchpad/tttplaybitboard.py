"""
Rewrite of tttplay using a bitboard representation as
inspired by https://gist.github.com/pnf/5924614
TODO: a strategy that breaks ties as Peter Fraenkel does there.
"""

def human_vs_puter():
    play(human_move, negamax_move)

def play(play_X, play_O):
    grid = empty_grid
    players = ('X', play_X), ('O', play_O)
    while True:
        print ansi_clear_screen
        show(grid, [player[0] for player in players])
        mark, strategy = players[0]
        if is_won(grid):
            print mark, "wins."
            break
        if is_drawn(grid):
            print "A draw."
            break
        grid = strategy(grid, mark)
        players = players[::-1]

ansi_clear_screen = '\x1b[2J\x1b[H'


# Strategies

def human_move(grid, mark):
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

def negamax_move(grid, mark):
    _, successor = pick_successor(grid)
    return successor

def pick_successor(grid):
    "Return (value_to_p, (obits, new_pbits) for p's best move."
    # Pre: game not over
    return max((1, successor) if is_won(successor)
               else (0, successor) if is_drawn(successor)
               else (lambda (v, _): (-v, successor))(pick_successor(successor))
               for successor in successors(grid))


# Bit-board representation: a pair of bitsets (p, q),
# p for the player to move, q for their opponent.
# Least significant bit is the lower-right square; msb is upper-left.
# (Differs from the human move numbering for the sake of nice octal constants.)

empty_grid = 0, 0

def is_drawn((p, q)):
    return (p | q) == 0777

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

def show((bits1, bits2), (mark1, mark2)):
    "Show a grid human-readably."
    bits = iter(zip(*map(player_bits, (bits1, bits2))))
    for row in range(3):
        for col in range(3):
            bit1, bit2 = next(bits)
            print mark1 if bit1 else mark2 if bit2 else '.',
        print
    print

def player_bits(bits):
    return ((bits >> i) & 1 for i in reversed(range(9)))


## show((0700, 0060), 'XO')
#. X X X
#. O O .
#. . . .
#. 
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

## show((0104, 0420), 'XO')
#. O . X
#. . O .
#. X . .
#. 
#. 
## show(negamax_move((0104, 0420), 'X'), 'OX')
#. O . X
#. . O .
#. X . X
#. 
#. 

if __name__ == '__main__':
    human_vs_puter()