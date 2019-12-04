# -*- coding: utf-8 -*-

import threading
import time


class UserInterfaceBase(threading.Thread):
	
	def __init__(self, frame_rate=10):
		super(UserInterfaceBase, self).__init__()
		self.daemon = True
		
		self._frame_rate = frame_rate
		self._terminate = False
	
	def update(self):
		self._update = True
	
	def _update_board(self):
		pass
	
	def terminate(self):
		self._terminate = True
	
	def run(self):
		while not self._terminate:
			if self._update:
				self._update_board()
			time.sleep(1.0 / self._frame_rate)

