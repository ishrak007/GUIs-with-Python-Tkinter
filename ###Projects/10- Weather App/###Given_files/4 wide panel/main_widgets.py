from customtkinter import CTkFrame
from components import *

class SmallWidget(CTkFrame):
	def __init__(self, parent, current_data, location, color):
		super().__init__(master = parent, fg_color = 'transparent')
		self.pack(expand = True, fill = 'both')

		# layout 
		self.rowconfigure(0, weight = 6, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')

		# widgets 
		SimplePanel(self, current_data, 0, 0, color)
		DatePanel(self, location, 0, 1, color)

class WideWidget(CTkFrame):
	def __init__(self, parent, current_data, forecast_data, location, color):
		super().__init__(master = parent, fg_color = 'transparent')
		self.pack(expand = True, fill = 'both')

		# layout 
		self.rowconfigure(0, weight = 6, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure(1, weight = 2, uniform = 'a')

		# widgets 
		SimplePanel(self, current_data, 0, 0, color)
		DatePanel(self, location, 0, 1, color)
		HorizontalForecastPanel(self, forecast_data, 1, 0, 2, color['divider color'])

class TallWidget(CTkFrame):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'green')
		self.pack(expand = True, fill = 'both')

class MaxWidget(CTkFrame):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'yellow')
		self.pack(expand = True, fill = 'both')