import random

import cv2
import numpy as np


class Board:

    BLOCKS = {
        '0': {
            'background': (205, 191, 178),
            'text': (0, 0, 0),
        },
        '2': {
            'background': (238, 228, 218),
            'text': (34, 34, 34),
        },
        '4': {
            'background': (236, 224, 200),
            'text': (34, 34, 34),
        },
        '8': {
            'background': (242, 176, 126),
            'text': (250, 249, 247),
        },
        '16': {
            'background': (247, 150, 97),
            'text': (255, 249, 235),
        },
        '32': {
            'background': (243, 126, 91),
            'text': (255, 249, 235),
        },
        '64': {
            'background': (253, 84, 55),
            'text': (255, 249, 235),
        },
        '128': {
            'background': (243, 204, 113),
            'text': (255, 249, 235),
        },
        '256': {
            'background': (238, 202, 108),
            'text': (255, 249, 235),
        },
        '512': {
            'background': (236, 202, 79),
            'text': (255, 249, 235),
        },
        '1024': {
            'background': (232, 185, 69),
            'text': (249, 246, 242),
        },
        '2048': {
            'background': (237, 194, 46),
            'text': (249, 246, 242),
        },
        '4096': {
            'background': (60, 58, 50),
            'text': (249, 246, 242),
        },
        '8192': {
            'background': (60, 58, 50),
            'text': (249, 246, 242),
        },
        '16384': {
            'background': (60, 58, 50),
            'text': (249, 246, 242),
        },
        '32768': {
            'background': (60, 58, 50),
            'text': (249, 246, 242),
        },
        '65536': {
            'background': (60, 58, 50),
            'text': (249, 246, 242),
        },
    }

    def __init__(self, window_size, padding, board_size, block_size):
        self.window_w, self.window_h = window_size
        self.padding_w, self.padding_h = padding
        self.board_w, self.board_h = board_size
        self.block_w, self.block_h = block_size

        self.background = self.create_background()
        self.value = self.create_board()
        self.shape = self.value.shape

        self.restart()

    def create_background(self):
        img = np.zeros((self.window_h, self.window_w, 3), dtype=np.uint8)

        x1, y1 = self.padding_w, self.padding_h
        x2, y2 = self.window_w - self.padding_w, self.window_h - self.padding_h

        img = cv2.rectangle(img, (x1, y1), (x2, y2), (160, 173, 187), -1)

        return img

    def restart(self):
        for i in [0, 1]:
            self.add_number()

        # self.value = [
        #     [   8,    4,     2,     2],
        #     [  16,   32,    64,   128],
        #     [2048, 1024,   512,   256],
        #     [4096, 8192, 16384, 32768],
        # ]

        # self.value = [
        #     [2, 2, 4, 8],
        #     [2, 2, 4, 4],
        #     [2, 2, 0, 0],
        #     [4, 4, 8, 16],
        # ]

    def create_board(self):
        return np.zeros((self.board_h, self.board_w), dtype=np.uint8)

    def get_empty_positions(self):
        positions = []
        for x in range(self.board_w):
            for y in range(self.board_h):
                if self.value[y][x] == 0:
                    positions.append((x, y))
        return positions

    def random_position(self):
        positions = self.get_empty_positions()
        if len(positions) > 0:
            return random.choice(positions)
        return None, None

    def get_color(self, number, kind):
        color = list(self.BLOCKS[str(number)][kind])
        color.reverse()
        return tuple(color)

    def draw_board(self):
        img = self.background.copy()

        for x in range(self.board_w):
            for y in range(self.board_h):
                number = self.value[y][x]

                # Background
                x1, y1 = self.padding_w + x * self.block_w, self.padding_h + y * self.block_h
                x2, y2 = x1 + self.block_w, y1 + self.block_h
                img = cv2.rectangle(img, (x1 + 4, y1 + 4), (x2 - 4, y2 - 4), self.get_color(number, 'background'), -1)

                if number != 0:
                    # Number
                    text_size, text_dx = 1, 0
                    text_len = len(str(self.value[y][x]))
                    if text_len == 4:
                        text_size = 0.75
                        text_dx = 10 * (len(str(self.value[y][x]))//4)
                    elif text_len == 5:
                        text_size = 0.60
                        text_dx = 20 * (len(str(self.value[y][x]))//4)

                    xc = x1 + self.block_w // 2 - 10 * len(str(self.value[y][x])) + text_dx
                    yc = y1 + self.block_h // 2 +  8 * 1
                    img = cv2.putText(img, str(number), (xc, yc), cv2.FONT_HERSHEY_SIMPLEX, text_size, self.get_color(number, 'text'), 2, cv2.LINE_AA)

        return img

    def add_number(self, check=False):
        x, y = self.random_position()
        if None not in [x, y]:
            if not check:
                self.value[y][x] = 2
            return True
        return False

    def sum_to(self, direction, check=False):
        is_summed = False
        if direction == 'left' or direction == 'right':
            if direction == 'right':
                x_start, x_end, x_inc = 0, self.board_w, 1
            else:
                x_start, x_end, x_inc = self.board_w - 1, -1, -1

            for y_0 in range(self.board_h):
                x_0 = x_start
                while True:
                    if direction == 'right' and x_0 >= x_end:
                        break

                    if direction == 'left' and x_0 < x_end:
                        break

                    number_0 = self.value[y_0][x_0]
                    if number_0 != 0:
                        for x_1 in range(x_0 + x_inc, x_end, x_inc):
                            number_1 = self.value[y_0][x_1]
                            if number_1 == number_0:
                                if not check:
                                    self.value[y_0][x_0] = 0
                                    self.value[y_0][x_1] = number_0 + number_1
                                x_0 = x_1
                                is_summed = True
                                break

                            elif number_1 != 0:
                                break

                            else:
                                continue
                    x_0 += x_inc

        elif direction == 'up' or direction == 'down':
            if direction == 'up':
                y_start, y_end, y_inc = 0, self.board_h, 1
            else:
                y_start, y_end, y_inc = self.board_h - 1, -1, -1

            for x_0 in range(self.board_w):
                y_0 = y_start
                while True:
                    if direction == 'up' and y_0 >= y_end:
                        break

                    if direction == 'down' and y_0 < y_end:
                        break

                    number_0 = self.value[y_0][x_0]
                    if number_0 != 0:
                        for y_1 in range(y_0 + y_inc, y_end, y_inc):
                            number_1 = self.value[y_1][x_0]
                            if number_1 == number_0:
                                if not check:
                                    self.value[y_0][x_0] = 0
                                    self.value[y_1][x_0] = number_0 + number_1
                                y_0 = y_1
                                is_summed = True
                                break

                            elif number_1 != 0:
                                break

                            else:
                                continue
                    y_0 += y_inc

        return is_summed

    def align_to(self, direction, check=False):
        is_aligned = False
        if direction == 'left' or direction == 'right':
            if direction == 'left':
                x_start, x_end, x_inc = 0, self.board_w, 1
            else:
                x_start, x_end, x_inc = self.board_w - 1, - 1, - 1

            for y_0 in range(self.board_h):
                for x_0 in range(x_start, x_end, x_inc):
                    number_0 = self.value[y_0][x_0]
                    if number_0 != 0:
                        continue

                    for x_1 in range(x_0 + x_inc, x_end, x_inc):
                        number_1 = self.value[y_0][x_1]

                        if number_1 != 0:
                            if not check:
                                self.value[y_0][x_0] = number_1
                                self.value[y_0][x_1] = 0
                            is_aligned = True
                            break

        elif direction == 'up' or direction == 'down':
            if direction == 'up':
                y_start, y_end, y_inc = 0, self.board_h, 1
            else:
                y_start, y_end, y_inc = self.board_h - 1, - 1, - 1

            for x_0 in range(self.board_w):
                for y_0 in range(y_start, y_end, y_inc):
                    number_0 = self.value[y_0][x_0]
                    if number_0 != 0:
                        continue

                    for y_1 in range(y_0 + y_inc, y_end, y_inc):
                        number_1 = self.value[y_1][x_0]

                        if number_1 != 0:
                            if not check:
                                self.value[y_0][x_0] = number_1
                                self.value[y_1][x_0] = 0
                            is_aligned = True
                            break

        return is_aligned

    def move_left(self):
        return self.move_to('left')

    def move_down(self):
        return self.move_to('down')

    def move_right(self):
        return self.move_to('right')

    def move_up(self):
        return self.move_to('up')

    def move_to(self, direction):
        is_summed = self.sum_to(direction)
        is_aligned = self.align_to(direction)
        is_added = self.add_number() if is_summed or is_aligned else False
        is_game_over = False
        if not is_summed and not is_aligned and not is_added:
            return not self.is_move_able()
        return is_game_over

    def is_move_able(self):
        for direction in ['up', 'down', 'left', 'right']:
            if self.sum_to(direction, check=True) or self.align_to(direction, check=True):
                return True
        return False
