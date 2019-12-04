# -*- coding: utf-8 -*-

import atexit
import os
import subprocess
import sys


def clear_terminal():
#	print "\033[2J"
	os.system("clear")

def prepare_terminal():
	original_terminal_state = subprocess.Popen(b"stty -g", stdout=subprocess.PIPE, shell=True).communicate()[0]
	os.system(b"stty -icanon -echo -isig")
	atexit.register(_restore_terminal, original_terminal_state)

def _restore_terminal(state):
	os.system(b"stty " + state)

