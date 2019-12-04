# -*- coding: utf-8 -*-

import sys
import threading


class GameBase(threading.Thread):
	
	def __init__(self, user_interface=None):
		super(GameBase, self).__init__()
		
		self._user_interface = user_interface
		self._terminate = False
	
	def terminate(self):
		if self._user_interface:
			self._user_interface.terminate()
		self._terminate = True
	
	def _wait_for_key(self):
		return sys.stdin.read(1)
	
	def key_pressed(self, key):
		if key == "q":
			self.terminate()
	
	def run(self):
		while not self._terminate:
			self.key_pressed(self._wait_for_key())

