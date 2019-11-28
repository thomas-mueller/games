# -*- coding: utf-8 -*-

import copy
import numpy
import threading
import time

import os_support




class TerminalBoard(object):

	dtype = "U1"
	
	def __init__(self, board_width, board_height, header_height=0, left_margin_width=0, right_margin_width=0, footer_height=0, frame_rate=10):
		
		self._frame_rate = frame_rate
		
		self._thread = threading.Thread(target=self.run)
		self._thread.daemon = True
		self._thread.start()
		
		print_header = header_height > 0
		print_left_margin = left_margin_width > 0
		print_right_margin = right_margin_width > 0
		print_footer = footer_height > 0
		
		full_width = left_margin_width + (2 if print_left_margin else 1) + board_width + (2 if print_right_margin else 1) + right_margin_width
		full_height = header_height + (2 if print_header else 1) + board_height + (2 if print_footer else 1) + footer_height
		
		self._header = numpy.full((header_height, full_width-2), " ", dtype=TerminalBoard.dtype)
		self._left_margin = numpy.full((board_height, left_margin_width), " ", dtype=TerminalBoard.dtype)
		self._board = numpy.full((board_height, board_width), " ", dtype=TerminalBoard.dtype)
		self._right_margin = numpy.full((board_height, right_margin_width), " ", dtype=TerminalBoard.dtype)
		self._footer = numpy.full((footer_height, full_width-2), " ", dtype=TerminalBoard.dtype)
		
		# https://unicode-table.com/de/#box-drawing
		self._horizontal_bar_top = numpy.full((1, full_width), u"\u2501", dtype=TerminalBoard.dtype)
		self._horizontal_bar_top[0][0] = u"\u250F"
		self._horizontal_bar_top[0][-1] = u"\u2513"
		if (not print_header) and print_left_margin:
			self._horizontal_bar_top[0][left_margin_width+1] = u"\u252F"
		if (not print_header) and print_right_margin:
			self._horizontal_bar_top[0][full_width-right_margin_width-2] = u"\u252F"
		
		self._horizontal_bar_bottom = numpy.full((1, full_width), u"\u2501", dtype=TerminalBoard.dtype)
		self._horizontal_bar_bottom[0][0] = u"\u2517"
		self._horizontal_bar_bottom[0][-1] = u"\u251B"
		if (not print_footer) and print_left_margin:
			self._horizontal_bar_bottom[0][left_margin_width+1] = u"\u2537"
		if (not print_footer) and print_right_margin:
			self._horizontal_bar_bottom[0][full_width-right_margin_width-2] = u"\u2537"
		
		self._horizontal_bar_header = numpy.full((1 if print_header else 0, full_width-2), u"\u2500", dtype=TerminalBoard.dtype)
		if print_header and print_left_margin:
			self._horizontal_bar_header[0][left_margin_width] = u"\u252C"
		if print_header and print_right_margin:
			self._horizontal_bar_header[0][full_width-right_margin_width-3] = u"\u252C"
		
		self._horizontal_bar_footer = numpy.full((1 if print_footer else 0, full_width-2), u"\u2500", dtype=TerminalBoard.dtype)
		if print_footer and print_left_margin:
			self._horizontal_bar_footer[0][left_margin_width] = u"\u2534"
		if print_footer and print_right_margin:
			self._horizontal_bar_footer[0][full_width-right_margin_width-3] = u"\u2534"
		
		self._vertical_bar_left = numpy.full((full_height-2, 1), u"\u2503", dtype=TerminalBoard.dtype)
		if print_header:
			self._vertical_bar_left[header_height][0] = u"\u2520"
		if print_footer:
			self._vertical_bar_left[full_height-footer_height-3][0] = u"\u2520"
		
		self._vertical_bar_right = numpy.full((full_height-2, 1), u"\u2503", dtype=TerminalBoard.dtype)
		if print_header:
			self._vertical_bar_right[header_height][0] = u"\u2528"
		if print_footer:
			self._vertical_bar_right[full_height-footer_height-3][0] = u"\u2528"
		
		self._vertical_bar_left_margin = numpy.full((board_height, 1 if print_left_margin else 0), u"\u2502", dtype=TerminalBoard.dtype)
		self._vertical_bar_right_margin = numpy.full((board_height, 1 if print_right_margin else 0), u"\u2502", dtype=TerminalBoard.dtype)
		
		self._update = True
	
	
	def get_header(self):
		return self._header
	
	def update_header(self, header):
		if 	header.shape == self._header.shape:
			self._header = header
		elif header.shape > self._header.shape:
			self._header = header[:self._header.shape[0], :self._header.shape[1]]
		else:
			self._header[:self._header.shape[0], :self._header.shape[1]] = header
		self._update = True
	
	
	def get_left_margin(self):
		return self._left_margin
	
	def update_left_margin(self, left_margin):
		if 	left_margin.shape == self._left_margin.shape:
			self._left_margin = left_margin
		elif left_margin.shape > self._left_margin.shape:
			self._left_margin = left_margin[:self._left_margin.shape[0], :self._left_margin.shape[1]]
		else:
			self._left_margin[:self._left_margin.shape[0], :self._left_margin.shape[1]] = left_margin
		self._update = True
	
	
	def get_board(self):
		return self._board
	
	def update_board(self, board):
		if 	board.shape == self._board.shape:
			self._board = board
		elif board.shape > self._board.shape:
			self._board = board[:self._board.shape[0], :self._board.shape[1]]
		else:
			self._board[:self._board.shape[0], :self._board.shape[1]] = board
		self._update = True
	
	
	def get_right_margin(self):
		return self._right_margin
	
	def update_right_margin(self, right_margin):
		if 	right_margin.shape == self._right_margin.shape:
			self._right_margin = right_margin
		elif right_margin.shape > self._right_margin.shape:
			self._right_margin = right_margin[:self._right_margin.shape[0], :self._right_margin.shape[1]]
		else:
			self._right_margin[:self._right_margin.shape[0], :self._right_margin.shape[1]] = right_margin
		self._update = True
	
	
	def get_footer(self):
		return self._footer
	
	def update_footer(self, footer):
		if 	footer.shape == self._footer.shape:
			self._footer = footer
		elif footer.shape > self._footer.shape:
			self._footer = footer[:self._footer.shape[0], :self._footer.shape[1]]
		else:
			self._footer[:self._footer.shape[0], :self._footer.shape[1]] = footer
		self._update = True
	
	
	def update(self):
		self._update = True
	
	
	def _print_frame(self):
		frame_data = numpy.block([
				[self._horizontal_bar_top],
				[numpy.block([
						self._vertical_bar_left,
						numpy.block([
								[self._header],
								[self._horizontal_bar_header],
								[numpy.block([
										self._left_margin,
										self._vertical_bar_left_margin,
										self._board,
										self._vertical_bar_right_margin,
										self._right_margin
								])],
								[self._horizontal_bar_footer],
								[self._footer]
						]),
						self._vertical_bar_right
				])],
				[self._horizontal_bar_bottom]
		])
		frame_string = "\n".join(["".join(line) for line in frame_data])
	
		os_support.clear_terminal()
		print frame_string
		
		self._update = False
	
	
	def run(self):
		while True:
			if self._update:
				self._print_frame()
			time.sleep(1.0 / self._frame_rate)

