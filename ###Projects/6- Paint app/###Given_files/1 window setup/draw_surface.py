from tkinter import Canvas
from settings import * 

class DrawSurface(Canvas):
	def __init__(self, parent):
		super().__init__(master = parent, background = CANVS_BG, bd = 0, highlightthickness = 0, relief = 'ridge')
		self.pack(expand = True, fill = 'both')