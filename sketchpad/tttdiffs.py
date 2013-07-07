"""
tttplaybitboard is a little fancier than optimal play requires: it
breaks ties in minimax-value according to the expected value of a
board supposing both players move blindly. This module prints out
all the cases where the tiebreaker changes its behavior.

(This isn't quite what I ought to want, which is all cases where
the tiebreaker *affects* the choice. Sometimes the arbitrary choice
among optimal moves will be the same as what the tiebreaker chooses;
we don't report those cases.)

Cases related by symmetry are deduplicated. (The symmetries could be
exploited the same way in tttplaybitboard, but this turns out to speed
things up by only 1/3 or so, so we don't bother.)
"""

from tttplaybitboard import *

def viz_diffs():
    for grid in sorted(all_diffs()):
        original = view(grid)
        succ1 = min(successors(grid), key=evaluate)
        succ2 = max_play(grid)
        v1 = view(succ1)
        v2 = view(succ2)
        improvement = drunk_value(succ1) - drunk_value(succ2)
        print abut(original, abut(v1, v2)), '  %.2g' % improvement
        print

def abut(s, t, sep='   '):
    return '\n'.join(map(sep.join, zip(s.splitlines(), t.splitlines())))

## print abut(view((0700, 0062)), view((0700, 0061))),
#.  X X X    X X X
#.  O O .    O O .
#.  . O .    . . O

def all_diffs():
    return set(map(normalize, diffs(empty_grid)))

@memo
def diffs(grid):
    "The grids in the game subtree rooted here where v2 moves differently."
    grid = normalize(grid)
    if is_won(grid) or not successors(grid):
        return set()
    succ1 = min(successors(grid), key=evaluate)
    succ2 = max_play(grid)
    diff = set([grid]) if normalize(succ1) != normalize(succ2) else set()
    return diff.union(*map(diffs, successors(grid)))


# Reduce data modulo symmetry

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
    # abc     cfi        2  4  6
    # def --> beh       -2  0  2
    # ghi     adg       -6 -4 -2
    def turn1(b):
        return (  ((b & 0001) << 6)
                | ((b & 0010) << 4)
                | ((b & 0102) << 2)
                | ((b & 0020))
                | ((b & 0204) >> 2)
                | ((b & 0040) >> 4)
                | ((b & 0400) >> 6))
    return turn1(p), turn1(q)

## print view(turn((0700, 0060)))
#.  O . .
#.  O X .
#.  O X .
#. 
## print view(flip((0700, 0060)))
#.  . . .
#.  X X .
#.  O O O
#. 

#ways_to_win = (0700, 0070, 0007, 0444, 0222, 0111, 0421, 0124)
# XXX I'd like to write
# ways_to_win = set(equivalents(0700) + equivalents(0070) + equivalents(0124))
# but equivalents takes a board, not a bitset.


if __name__ == '__main__':
    viz_diffs()
