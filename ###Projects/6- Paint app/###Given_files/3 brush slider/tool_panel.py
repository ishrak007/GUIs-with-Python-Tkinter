import customtkinter as ctk
from settings import *

class ToolPanel(ctk.CTkToplevel):
	def __init__(self, parent, brush_float):
		super().__init__()
		self.geometry('200x300')
		self.title('')
		self.resizable(False, False)
		self.iconbitmap('empty.ico')
		self.attributes('-topmost', True)
		self.protocol('WM_DELETE_WINDOW', self.close_app)
		self.parent = parent

		# layout 
		self.columnconfigure((0,1,2), weight = 1, uniform = 'a')
		self.rowconfigure(0, weight = 2, uniform = 'a')
		self.rowconfigure(1, weight = 3, uniform = 'a')
		self.rowconfigure((2,3), weight = 1, uniform = 'a')

		# widgets 
		BrushSizeSlider(self, brush_float)

	def close_app(self):
		self.parent.quit()

class BrushSizeSlider(ctk.CTkFrame):
	def __init__(self, parent, brush_float):
		super().__init__(master = parent)
		self.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew', pady = 5, padx = 5)
		ctk.CTkSlider(self, variable = brush_float, from_ = 0.2, to = 1).pack(fill = 'x', expand = True, padx = 5)
	# exercise:
	# create a slider
	# connect the slider to the tkinter var