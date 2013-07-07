"""
My super-fancy console tic-tac-toe. A rewrite of tttplay using a bitboard
representation as inspired by https://gist.github.com/pnf/5924614
And grid_format came from
https://github.com/gigamonkey/gigamonkey-tic-tac-toe/blob/master/search.py
"""

def main(argv):
    pool = dict((name[:-5], play) for name, play in globals().items()
                if name.endswith('_play'))
    faceoff = [human_play, max_play]
    try:
        if len(argv) == 1:
            pass
        elif len(argv) == 2:
            faceoff[1] = pool[argv[1]]
        elif len(argv) == 3:
            faceoff = [pool[argv[1]], pool[argv[2]]]
        else:
            raise KeyError
    except KeyError:
        print "Usage: %s [player] [player]" % argv[0]
        print "where a player is one of:", ' '.join(sorted(pool))
        return 1
    else:
        tictactoe(*faceoff)
        return 0

def tictactoe(play_X, play_O, grid=None):
    "Put two strategies to a classic battle of wits."
    grid = grid or empty_grid
    players = ('X', play_X), ('O', play_O)
    while True:
        (mark, play), (prev_mark, _) = players
        if human_play in (play_X, play_O): print ansi_clear_screen
        print view(grid, (mark, prev_mark))
        print
        if is_won(grid):
            print prev_mark, "wins."
            break
        if not successors(grid):
            print "A draw."
            break
        grid = play(grid, mark)
        players = players[::-1]

ansi_clear_screen = '\x1b[2J\x1b[H'


# Utilities

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
    "Just ask for a move."
    while True:
        try:
            move = int(raw_input(mark + " move? [1-9] "))
        except ValueError:
            pass
        else:
            if 1 <= move <= 9:
                successor = apply_move(grid, from_human_move(move))
                if successor: return successor
        print "Hey, that's illegal. Give me one of these digits:"
        print
        print (grid_format
               % tuple(move if apply_move(grid, from_human_move(move)) else '-'
                       for move in range(1, 10)))
        print

grid_format = '\n'.join([' %s %s %s'] * 3)

def drunk_play(grid, mark):
    "Beatable, but not so stupid it seems mindless."
    return min(successors(grid), key=drunk_value)

def max_play(grid, mark):
    "Play minimax with ties broken by drunk_value."
    return best_successor(grid)

def best_successor(grid):
    return min(successors(grid),
               key=lambda succ: (evaluate(succ), drunk_value(succ)))

@memo
def drunk_value(grid):
    "Return the expected value to the player if both players play at random."
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
    return any(way == (way & q) for way in ways_to_win)

ways_to_win = (0700, 0070, 0007, 0444, 0222, 0111, 0421, 0124)

def successors(grid):
    "Return the possible grids resulting from p's moves."
    return filter(None, (apply_move(grid, move) for move in range(9)))

def apply_move((p, q), move):
    "Try to move: return a new grid, or None if illegal."
    bit = 1 << move
    return (q, p | bit) if 0 == (bit & (p | q)) else None

def from_human_move(n):
    "Convert from a move numbered 1..9 in top-left..bottom-right order."
    return 9 - n

def view((p, q), (p_mark, q_mark)):
    "Show a grid human-readably."
    squares = (p_mark if by_p else q_mark if by_q else '.'
               for by_p, by_q in zip(*map(player_bits, (p, q))))
    return grid_format % tuple(squares)

def player_bits(bits):
    return ((bits >> i) & 1 for i in reversed(range(9)))


## print view((0610, 0061), 'XO')
#.  X X .
#.  O O X
#.  . . O
#. 
## for succ in successors((0610, 0061)): print view(succ, 'XO'),'\n'
#.  O O .
#.  X X O
#.  . O X 
#. 
#.  O O .
#.  X X O
#.  O . X 
#. 
#.  O O O
#.  X X O
#.  . . X 
#. 
#. 
## print view(max_play((0610, 0061), 'X'), 'XO')
#.  O O O
#.  X X O
#.  . . X
#. 

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
