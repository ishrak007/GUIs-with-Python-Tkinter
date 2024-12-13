import customtkinter as ctk
from settings import *

class ToolPanel(ctk.CTkToplevel):
	def __init__(self, parent, brush_float, color_string):
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
		ColorPanel(self,color_string)

	def close_app(self):
		self.parent.quit()

class ColorPanel(ctk.CTkFrame):
	def __init__(self, parent, color_string):
		super().__init__(master = parent, fg_color = 'transparent')
		self.grid(row = 1, column = 0, columnspan = 3, pady = 5, padx = 5)
		self.color_string = color_string

		# layout
		self.rowconfigure([row for row in range(COLOR_ROWS)], weight = 1, uniform = 'a')
		self.columnconfigure([col for col in range(COLOR_COLS)], weight = 1, uniform = 'a')

		# widgets 
		for row in range(COLOR_ROWS):
			for col in range(COLOR_COLS):
				color = COLORS[row][col]
				ColorFieldButton(self, row, col, color, self.pick_color)

	def pick_color(self, color):
		self.color_string.set(color)

class ColorFieldButton(ctk.CTkButton):
	def __init__(self, parent, row, col, color, pick_color):
		super().__init__(
			master = parent, 
			text = '', 
			fg_color = f'#{color}', 
			corner_radius = 1,
			command = self.click_handler)
		self.grid(row = row, column = col, padx = 0.4, pady = 0.4)

		self.pick_color = pick_color
		self.color = color

	def click_handler(self):
		self.pick_color(self.color)

class BrushSizeSlider(ctk.CTkFrame):
	def __init__(self, parent, brush_float):
		super().__init__(master = parent)
		self.grid(row = 2, column = 0, columnspan = 3, sticky = 'nsew', pady = 5, padx = 5)
		ctk.CTkSlider(self, variable = brush_float, from_ = 0.2, to = 1).pack(fill = 'x', expand = True, padx = 5)
