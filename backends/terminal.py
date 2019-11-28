# -*- coding: utf-8 -*-

import copy
import numpy
import sys

import os_support


class TerminalBoard(object):
	
	def __init__(self, board_width, board_height, header_height=0, left_margin_width=0, right_margin_width=0, footer_height=0):
		
		self.board_width = board_width
		self.board_height = board_height
		self.header_height = header_height
		self.left_margin_width = left_margin_width
		self.right_margin_width = right_margin_width
		self.footer_height = footer_height
	
		print_header = header_height > 0
		print_left_margin = left_margin_width > 0
		print_right_margin = right_margin_width > 0
		print_footer = footer_height > 0
		
		self.full_width = self.left_margin_width + (2 if print_left_margin else 1) + self.board_width + (2 if print_right_margin else 1) + self.right_margin_width
		self.full_height = self.header_height + (2 if print_header else 1) + self.board_height + (2 if print_footer else 1) + self.footer_height
		
		horizontal_bar_top = numpy.full((1, self.full_width), u"\u2501", dtype="U1")
		horizontal_bar_top[0][0] = u"\u250F"
		horizontal_bar_top[0][-1] = u"\u2513"
		if (not print_header) and print_left_margin:
			horizontal_bar_top[0][self.left_margin_width+1] = u"\u252F"
		if (not print_header) and print_right_margin:
			horizontal_bar_top[0][self.full_width-self.right_margin_width-2] = u"\u252F"
		
		horizontal_bar_bottom = numpy.full((1, self.full_width), u"\u2501", dtype="U1")
		horizontal_bar_bottom[0][0] = u"\u2517"
		horizontal_bar_bottom[0][-1] = u"\u251B"
		if (not print_footer) and print_left_margin:
			horizontal_bar_bottom[0][self.left_margin_width+1] = u"\u2537"
		if (not print_footer) and print_right_margin:
			horizontal_bar_bottom[0][self.full_width-self.right_margin_width-2] = u"\u2537"
		
		horizontal_bar_header = numpy.full((1 if print_header else 0, self.full_width-2), u"\u2500", dtype="U1")
		if print_header and print_left_margin:
			horizontal_bar_header[0][self.left_margin_width] = u"\u252C"
		if print_header and print_right_margin:
			horizontal_bar_header[0][self.full_width-self.right_margin_width-3] = u"\u252C"
		
		horizontal_bar_footer = numpy.full((1 if print_footer else 0, self.full_width-2), u"\u2500", dtype="U1")
		if print_footer and print_left_margin:
			horizontal_bar_footer[0][self.left_margin_width] = u"\u2534"
		if print_footer and print_right_margin:
			horizontal_bar_footer[0][self.full_width-self.right_margin_width-3] = u"\u2534"
		
		vertical_bar_left = numpy.full((self.full_height-2, 1), u"\u2503", dtype="U1")
		if print_header:
			vertical_bar_left[self.header_height][0] = u"\u2520"
		if print_footer:
			vertical_bar_left[self.full_height-self.footer_height-3][0] = u"\u2520"
		
		vertical_bar_right = numpy.full((self.full_height-2, 1), u"\u2503", dtype="U1")
		if print_header:
			vertical_bar_right[self.header_height][0] = u"\u2528"
		if print_footer:
			vertical_bar_right[self.full_height-self.footer_height-3][0] = u"\u2528"
		
		vertical_bar_left_margin = numpy.full((self.board_height, 1 if print_left_margin else 0), u"\u2502", dtype="U1")
		vertical_bar_right_margin = numpy.full((self.board_height, 1 if print_right_margin else 0), u"\u2502", dtype="U1")
		
		empty_header = numpy.full((self.header_height, self.full_width-2), " ", dtype="U1")
		empty_left_margin = numpy.full((self.board_height, self.left_margin_width), " ", dtype="U1")
		empty_board = numpy.full((self.board_height, self.board_width), " ", dtype="U1")
		empty_right_margin = numpy.full((self.board_height, self.right_margin_width), " ", dtype="U1")
		empty_footer = numpy.full((self.footer_height, self.full_width-2), " ", dtype="U1")
		
		self.frame_data = numpy.block([
				[horizontal_bar_top],
				[numpy.block([
						vertical_bar_left,
						numpy.block([
								[empty_header],
								[horizontal_bar_header],
								[numpy.block([
										empty_left_margin,
										vertical_bar_left_margin,
										empty_board,
										vertical_bar_right_margin,
										empty_right_margin
								])],
								[horizontal_bar_footer],
								[empty_footer]
						]),
						vertical_bar_right
				])],
				[horizontal_bar_bottom]
		])
	
	
	def print_frame(self):
		os_support.clear_terminal()
		print "\n".join(["".join(line) for line in self.frame_data])
