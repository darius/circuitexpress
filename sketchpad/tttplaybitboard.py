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
#        print ansi_clear_screen
        show(grid, (mark, prev_mark))
        if is_won(grid):
            print prev_mark, "wins."
            break
        if is_full(grid):
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
    _, successor = pick_successor(grid)
    _, succ2 = pick_successor_v2(grid)
    if successor != succ2:
        print 'Hey, different moves', successor, succ2
    return successor

@memo
def pick_successor(grid):
    "Return (value_to_player, successor) for the player's best move."
    return max(((1, successor) if is_won(successor)
                else (0, successor) if is_full(successor)
                else (lambda (v, _): (-v, successor))(pick_successor(successor))
                for successor in successors(grid)),
               key=lambda (score, succ): score)

@memo
def pick_successor_v2(grid):
    "Return (value_to_player, successor) for the player's best move."
    return max(((1, successor) if is_won(successor)
                else (0, successor) if is_full(successor)
                else (lambda (v, _): (-v, successor))(pick_successor_v2(successor))
                for successor in successors(grid)),
               key=lambda (score, succ): (score, -drunk_value(succ)))

def viz_diffs():
    for grid in sorted(all_diffs()):
        orig = view(grid, 'XO')
        score1, succ1 = pick_successor(grid)
        v1 = view(succ1, 'OX')
        score2, succ2 = pick_successor_v2(grid)
        v2 = view(succ2, 'OX')
        improvement = drunk_value(succ1) - drunk_value(succ2)
        print abut(orig, abut(v1, v2)), '  %.2g' % improvement
        print

def abut(s, t, sep='   '):
    return '\n'.join(map(sep.join, zip(s.splitlines(), t.splitlines())))

## print abut(view((0700, 0062), 'XO'), view((0700, 0061), 'XO')),
#. X X X   X X X
#. O O .   O O .
#. . O .   . . O

def all_diffs():
    return set(map(normalize, diffs(empty_grid)))

@memo
def diffs(grid):
    "The grids in the game subtree rooted here where v2 moves differently."
    grid = normalize(grid)
    if is_won(grid) or is_full(grid):
        return set()
    _, successor = pick_successor(grid)
    _, succ2 = pick_successor_v2(grid)
    diff = set([grid]) if normalize(successor) != normalize(succ2) else set()
    return diff.union(*map(diffs, successors(grid)))

@memo
def drunk_value(grid):
    "Return expected value to the player if both players play at random."
    if is_won(grid): return -1
    if is_full(grid): return 0
    return -average(map(drunk_value, successors(grid)))

def average(ns):
    assert ns
    return float(sum(ns)) / len(ns)


# Bit-board representation: a pair of bitsets (p, q),
# p for the player to move, q for their opponent.
# Least significant bit is the lower-right square; msb is upper-left.
# (Differs from the human move numbering for the sake of nice octal constants.)

empty_grid = 0, 0

def normalize(grid):
    "Of the grids equivalent to grid under symmetry, pick one consistently."
    return min(equivalents(grid))

def equivalents(grid):
    return spin(grid) + spin(flip(grid))

def spin(grid):
    "Return a list of the four rotations of the grid."
    result = [grid]
    for _ in range(3):
        grid = turn(grid)
        result.append(grid)
    return result

def flip((p, q)):
    "Mirror-reflect the grid vertically."
    # 0123 --> 0321
    def flip1(bits): return ((bits & 07) << 6) | (bits & 070) | ((bits & 0700) >> 6)
    return flip1(p), flip1(q)

def turn((p, q)):
    "Turn the grid a quarter turn."
    # abc     cfi
    # def --> beh
    # ghi     adg
    #
    #         2  4  6
    #        -2  0  2
    #        -6 -4 -2
    def turn1(b):
        return (  ((b & 0001) << 6)
                | ((b & 0010) << 4)
                | ((b & 0102) << 2)
                | ((b & 0020))
                | ((b & 0204) >> 2)
                | ((b & 0040) >> 4)
                | ((b & 0400) >> 6))
    return turn1(p), turn1(q)

def is_full((p, q)):
    "Is no move possible?"
    return (p | q) == 0777

def is_won((p, q)):
    "Did the latest move win the game?"
    return any((q & way) == way for way in ways_to_win)

ways_to_win = (0700, 0070, 0007, 0444, 0222, 0111, 0421, 0124)
# XXX I'd like to write
# ways_to_win = set(equivalents(0700) + equivalents(0070) + equivalents(0124))
# but equivalents takes a board, not a bitset.

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
    lines = []
    bits = iter(zip(*map(player_bits, (bits1, bits2))))
    for row in range(3):
        lines.append([])
        for col in range(3):
            bit1, bit2 = next(bits)
            lines[-1].append(mark1 if bit1 else mark2 if bit2 else '.')
        lines[-1] = ' '.join(lines[-1])
    return '\n'.join(lines)

def player_bits(bits):
    return ((bits >> i) & 1 for i in reversed(range(9)))

    
## print view((0700, 0060), 'XO')
#. X X X
#. O O .
#. . . .
#. 
## print view(turn((0700, 0060)), 'XO')
#. X . .
#. X O .
#. X O .
#. 
## print view(flip((0700, 0060)), 'XO')
#. . . .
#. O O .
#. X X X
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
    # human_vs_puter()
    viz_diffs()
