import re

def play():
    grid = empty_grid
    for player in 'XO'*5:
        print ansi_clear_screen + show(grid, '\n--+---+--\n', ' | ')
        if is_full(grid) or is_won(grid): break
        if player == 'O':
            _, move = choose_move(grid, player)
        else:
            move = int(raw_input(player + ' move? [1-9] ')) - 1
        grid = update(grid, move, player)

def choose_move(grid, player):
    "Return (value_to_player, new_grid) for player's best move on grid."
    # Pre: game not over and it's player's move
    return max((1, move) if is_won(new_grid)
               else (0, move) if is_full(new_grid)
               else (lambda (v, m): (-v, move))(choose_move(new_grid, other[player]))
               for move in range(9)
               if ' ' == grid[move]
               for new_grid in [update(grid, move, player)])

empty_grid = ' ' * 9
other = {'X': 'O', 'O': 'X'}

def update(grid, square, player):
    return grid[:square] + player + grid[square+1:]

def show(grid, r, c):
    return r.join(c.join(grid[i:i+3]) for i in range(0, 9, 3))

def is_full(grid): return ' ' not in grid
def is_won(grid): return re.search(win, show(grid, ';', ''))

win = r'OOO|O...O...O|O;.O.;O|O..;.O.;..O'
win += '|' + win.replace('O', 'X')

ansi_clear_screen = '\x1b[2J\x1b[H'

if __name__ == '__main__':
    play()
