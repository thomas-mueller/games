#!/usr/bin/env python
# -*- coding: utf-8 -*-

import backends.terminal as terminal
import copy
import time

def main():
	game = terminal.TerminalBoard(board_width=15, board_height=4, header_height=2, left_margin_width=5, right_margin_width=10, footer_height=2, frame_rate=10)
	
	board = copy.deepcopy(game.get_board())
	for x in range(15):
		tmp_board = copy.deepcopy(board)
		tmp_board[0:4, x] = "x"
		game.update_board(tmp_board)
		time.sleep(0.5)
