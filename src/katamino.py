"""
Katamino Simulator
"""

import copy
import datetime
import pieces


def new_board(width, height=5):
    """Make a new (empty) board"""
    board = []
    for _ in range(0, height):
        row = []
        for _ in range(0, width):
            row.append('.')
        board.append(row)
    return board


def write_board(board, out):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            out.write(col)
        out.write('\n')
    out.write('\n')


def print_board(board):
    """Friendly-print the board"""
    for row in board:
        for col in row:
            print(col, end='')
        print()
    print()


def solve(board, pieces, index, out):
    """recursive solve"""
    for rot in range(8):
        if index == 0:
            print('.', end='', flush=True)
        for y in range(len(board)):
            for x in range(len(board[0])):
                piece = pieces[index]
                if not piece.can_place(board, x, y, rot):
                    continue
                next_board = copy.deepcopy(board)
                piece.place(next_board, x, y, rot)
                if index == (len(pieces) - 1):
                    write_board(next_board, out)
                    out.flush()
                    return True
                solve(next_board, pieces, index + 1, out)
                # if sol:
                #    return True
    return False


SMALL_SLAM_3 = [
    'AHGEBFLD',
    'DECAFHGB',
    'ALEHDCFK',
    'HECDLKBG',
    'ADLFCGHB',
    'ECKHGDAB',
    'ALEFHBDK'
]


def main():
    """main"""

    with open('results.txt', 'w') as out:
        num = 0
        for sequence in SMALL_SLAM_3:
            num = num + 1
            pcs = []
            for pos in range(2):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
            pos += 1
            while pos < len(sequence):
                pcs.append(pieces.get_piece_by_name(sequence[pos]))
                board = new_board(len(pcs))
                s = str(num) + ': '
                for p in pcs:
                    s = s + p.name
                print(s, end='')
                out.write(s + '\n')
                now = datetime.datetime.now()
                solve(board, pcs, 0, out)
                after = datetime.datetime.now()

                print((after - now).seconds)
                pos += 1


if __name__ == '__main__':
    main()
