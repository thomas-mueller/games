# -*- coding: utf-8 -*-

import copy
import numpy
import sys

import os_support




class TerminalBoard(object):

	dtype = "U1"
	
	def __init__(self, board_width, board_height, header_height=0, left_margin_width=0, right_margin_width=0, footer_height=0):
		
		print_header = header_height > 0
		print_left_margin = left_margin_width > 0
		print_right_margin = right_margin_width > 0
		print_footer = footer_height > 0
		
		full_width = left_margin_width + (2 if print_left_margin else 1) + board_width + (2 if print_right_margin else 1) + right_margin_width
		full_height = header_height + (2 if print_header else 1) + board_height + (2 if print_footer else 1) + footer_height
		
		self.header_shape = (header_height, full_width-2)
		self.left_margin_shape = (board_height, left_margin_width)
		self.board_shape = (board_height, board_width)
		self.right_margin_shape = (board_height, right_margin_width)
		self.footer_shape = (footer_height, full_width-2)
		
		self.header = numpy.full(self.header_shape, " ", dtype=TerminalBoard.dtype)
		self.left_margin = numpy.full(self.left_margin_shape, " ", dtype=TerminalBoard.dtype)
		self.board = numpy.full(self.board_shape, " ", dtype=TerminalBoard.dtype)
		self.right_margin = numpy.full(self.right_margin_shape, " ", dtype=TerminalBoard.dtype)
		self.footer = numpy.full(self.footer_shape, " ", dtype=TerminalBoard.dtype)
		
		# https://unicode-table.com/de/#box-drawing
		self.horizontal_bar_top = numpy.full((1, full_width), u"\u2501", dtype=TerminalBoard.dtype)
		self.horizontal_bar_top[0][0] = u"\u250F"
		self.horizontal_bar_top[0][-1] = u"\u2513"
		if (not print_header) and print_left_margin:
			self.horizontal_bar_top[0][left_margin_width+1] = u"\u252F"
		if (not print_header) and print_right_margin:
			self.horizontal_bar_top[0][full_width-right_margin_width-2] = u"\u252F"
		
		self.horizontal_bar_bottom = numpy.full((1, full_width), u"\u2501", dtype=TerminalBoard.dtype)
		self.horizontal_bar_bottom[0][0] = u"\u2517"
		self.horizontal_bar_bottom[0][-1] = u"\u251B"
		if (not print_footer) and print_left_margin:
			self.horizontal_bar_bottom[0][left_margin_width+1] = u"\u2537"
		if (not print_footer) and print_right_margin:
			self.horizontal_bar_bottom[0][full_width-right_margin_width-2] = u"\u2537"
		
		self.horizontal_bar_header = numpy.full((1 if print_header else 0, full_width-2), u"\u2500", dtype=TerminalBoard.dtype)
		if print_header and print_left_margin:
			self.horizontal_bar_header[0][left_margin_width] = u"\u252C"
		if print_header and print_right_margin:
			self.horizontal_bar_header[0][full_width-right_margin_width-3] = u"\u252C"
		
		self.horizontal_bar_footer = numpy.full((1 if print_footer else 0, full_width-2), u"\u2500", dtype=TerminalBoard.dtype)
		if print_footer and print_left_margin:
			self.horizontal_bar_footer[0][left_margin_width] = u"\u2534"
		if print_footer and print_right_margin:
			self.horizontal_bar_footer[0][full_width-right_margin_width-3] = u"\u2534"
		
		self.vertical_bar_left = numpy.full((full_height-2, 1), u"\u2503", dtype=TerminalBoard.dtype)
		if print_header:
			self.vertical_bar_left[header_height][0] = u"\u2520"
		if print_footer:
			self.vertical_bar_left[full_height-footer_height-3][0] = u"\u2520"
		
		self.vertical_bar_right = numpy.full((full_height-2, 1), u"\u2503", dtype=TerminalBoard.dtype)
		if print_header:
			self.vertical_bar_right[header_height][0] = u"\u2528"
		if print_footer:
			self.vertical_bar_right[full_height-footer_height-3][0] = u"\u2528"
		
		self.vertical_bar_left_margin = numpy.full((board_height, 1 if print_left_margin else 0), u"\u2502", dtype=TerminalBoard.dtype)
		self.vertical_bar_right_margin = numpy.full((board_height, 1 if print_right_margin else 0), u"\u2502", dtype=TerminalBoard.dtype)
		
	
	def print_frame(self):
		frame_data = numpy.block([
				[self.horizontal_bar_top],
				[numpy.block([
						self.vertical_bar_left,
						numpy.block([
								[self.header],
								[self.horizontal_bar_header],
								[numpy.block([
										self.left_margin,
										self.vertical_bar_left_margin,
										self.board,
										self.vertical_bar_right_margin,
										self.right_margin
								])],
								[self.horizontal_bar_footer],
								[self.footer]
						]),
						self.vertical_bar_right
				])],
				[self.horizontal_bar_bottom]
		])
		frame_string = "\n".join(["".join(line) for line in frame_data])
	
		os_support.clear_terminal()
		print frame_string
