#!/usr/bin/env python
# -*- coding: utf-8 -*-

import backends.terminalboard as terminalboard
import backends.gamebase as gamebase
import copy
import time

class HelloWorld(gamebase.GameBase):
	def __init__(self):
		
		hello_world = terminalboard.TerminalBoard(board_width=15, board_height=4, header_height=2, left_margin_width=5, right_margin_width=10, footer_height=2, frame_rate=10)
		hello_world.start()
	
#		board = copy.deepcopy(hello_world.get_board())
#		for x in range(15):
#			tmp_board = copy.deepcopy(board)
#			tmp_board[0:4, x] = "x"
#			hello_world.update_board(tmp_board)
#			time.sleep(0.5)

		super(HelloWorld, self).__init__(hello_world)
	
	def key_pressed(self, key):
		print "key \""+key+"\" pressed. Type:", type(key)
		super(HelloWorld, self).key_pressed(key)

