"""
Rewrite of tttplay using a bitboard representation as
inspired by https://gist.github.com/pnf/5924614
TODO: a strategy that breaks ties as Peter Fraenkel does there.
"""

def human_vs_puter():
    tictactoe(human_play, negamax_play)

def tictactoe(play_X, play_O):
    grid = empty_grid
    players = ('X', play_X), ('O', play_O)
    while True:
        (mark, play), (prev_mark, _) = players
#        print ansi_clear_screen
        show(grid, (mark, prev_mark))
        if is_won(grid):
            print prev_mark, "wins."
            break
        if is_drawn(grid):
            print "A draw."
            break
        grid = play(grid, mark)
        players = players[::-1]

ansi_clear_screen = '\x1b[2J\x1b[H'


# Utility

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
    # (Properly we should just use one of these, and unless I coded it
    # wrong they turn out to be equivalent.)
    _, successor = pick_successor(grid)
    _, succ2 = pick_successor_v2(grid)
    if successor != succ2:
        print 'Hey, different moves', successor, succ2
    return successor

@memo
def pick_successor(grid):
    "Return (value_to_player, successor) for the player's best move."
    return max((1, successor) if is_won(successor)
               else (0, successor) if is_drawn(successor)
               else (lambda (v, _): (-v, successor))(pick_successor(successor))
               for successor in successors(grid))

@memo
def pick_successor_v2(grid):
    "Return (value_to_player, successor) for the player's best move."
    return max(((1, successor) if is_won(successor)
                else (0, successor) if is_drawn(successor)
                else (lambda (v, _): (-v, successor))(pick_successor_v2(successor))
                for successor in successors(grid)),
               key=lambda (score, succ): (score, -drunk_value(succ)))

@memo
def diffs(grid):
    "The grids in the game subtree rooted here where v2 moves differently."
    if is_won(grid) or is_drawn(grid):
        return set()
    _, successor = pick_successor(grid)
    _, succ2 = pick_successor_v2(grid)
    diff = set([grid]) if successor != succ2 else set()
    return diff.union(*map(diffs, successors(grid)))

@memo
def drunk_value(grid):
    "Return expected value to the player if both players play at random."
    if is_won(grid): return -1
    if is_drawn(grid): return 0
    return -average(map(drunk_value, successors(grid)))

def average(ns):
    return float(sum(ns)) / len(ns)


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
## show(negamax_play((0104, 0420), 'X'), 'OX')
#. O . X
#. . O .
#. X . X
#. 
#. 

if __name__ == '__main__':
    human_vs_puter()
