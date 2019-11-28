#!/usr/bin/env python
# -*- coding: utf-8 -*-

import backends.terminal as terminal


def main():
	board = terminal.TerminalBoard(board_width=15, board_height=4, header_height=0, left_margin_width=0, right_margin_width=0, footer_height=0)
	board.print_frame()
	
	board = terminal.TerminalBoard(board_width=15, board_height=4, header_height=0, left_margin_width=5, right_margin_width=10, footer_height=2)
	board.print_frame()
	
	board = terminal.TerminalBoard(board_width=15, board_height=4, header_height=2, left_margin_width=0, right_margin_width=10, footer_height=2)
	board.print_frame()
	
	board = terminal.TerminalBoard(board_width=15, board_height=4, header_height=2, left_margin_width=5, right_margin_width=0, footer_height=2)
	board.print_frame()
	
	board = terminal.TerminalBoard(board_width=15, board_height=4, header_height=2, left_margin_width=5, right_margin_width=10, footer_height=0)
	board.print_frame()
	
	board = terminal.TerminalBoard(board_width=15, board_height=4, header_height=2, left_margin_width=5, right_margin_width=10, footer_height=2)
	board.print_frame()
