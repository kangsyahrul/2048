import os
import sys

import cv2

from model.board import Board

# GAME SETTING
BOARD_SIZE_W, BOARD_SIZE_H = BOARD_SIZE = (4, 4)

# SCREEN SETTING
BLOCK_SIZE_W, BLOCK_SIZE_H = BLOCK_SIZE = (72, 72)
PADDING_X, PADDING_Y = PADDING = (24, 24)
WINDOW_SIZE_W, WINDOW_SIZE_H = WINDOW_SIZE = (PADDING_X * 2 + BOARD_SIZE_W * BLOCK_SIZE_W, PADDING_Y * 2 + BOARD_SIZE_H * BLOCK_SIZE_H)


def main():
    board = Board(WINDOW_SIZE, PADDING, BOARD_SIZE, BLOCK_SIZE)

    is_game_over = False
    while not is_game_over:
        img = board.draw_board()

        cv2.imshow('2048 Game', img)

        key = cv2.waitKey(0)
        if key == ord('q') or key == ord('Q'):
            break

        if key == ord('a'):
            print('Move left')
            is_game_over = board.move_left()

        if key == ord('s'):
            is_game_over = board.move_down()

        if key == ord('d'):
            print('Move right')
            is_game_over = board.move_right()

        if key == ord('w'):
            is_game_over = board.move_up()

    cv2.destroyAllWindows()

    if is_game_over:
        print('GAME OVER')

    else:
        print('Exit the game')

    sys.exit(0)


if __name__ == '__main__':
    main()
