# -*- coding: utf-8 -*-

import os

if os.name == "posix":
	from posix import *
elif os.name == "nt":
	from nt import *
else:
	raise OSError(-1, "OS not supported (yet).")

