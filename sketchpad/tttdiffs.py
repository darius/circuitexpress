from tttplaybitboard import *

def viz_diffs():
    for grid in sorted(all_diffs()):
        orig = view(grid, 'XO')
        succ1 = min(successors(grid), key=evaluate)
        succ2 = best_successor(grid)
        v1 = view(succ1, 'OX')
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
    if is_won(grid) or not successors(grid):
        return set()
    successor = best_successor(grid)
    succ2 = min(successors(grid), key=evaluate)
    diff = set([grid]) if normalize(successor) != normalize(succ2) else set()
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

#ways_to_win = (0700, 0070, 0007, 0444, 0222, 0111, 0421, 0124)
# XXX I'd like to write
# ways_to_win = set(equivalents(0700) + equivalents(0070) + equivalents(0124))
# but equivalents takes a board, not a bitset.


if __name__ == '__main__':
    viz_diffs()
