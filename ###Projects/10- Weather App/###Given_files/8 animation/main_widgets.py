from customtkinter import CTkFrame
from components import *

class SmallWidget(CTkFrame):
	def __init__(self, parent, current_data, location, color, animation):
		super().__init__(master = parent, fg_color = 'transparent')
		self.pack(expand = True, fill = 'both')

		# layout 
		self.rowconfigure(0, weight = 6, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')

		# widgets 
		SimplePanel(self, current_data, 0, 0, color, animation)
		DatePanel(self, location, 0, 1, color)

class WideWidget(CTkFrame):
	def __init__(self, parent, current_data, forecast_data, location, color, forecast_images, animation):
		super().__init__(master = parent, fg_color = 'transparent')
		self.pack(expand = True, fill = 'both')

		# layout 
		self.rowconfigure(0, weight = 6, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure(1, weight = 2, uniform = 'a')

		# widgets 
		SimplePanel(self, current_data, 0, 0, color, animation)
		DatePanel(self, location, 0, 1, color)
		HorizontalForecastPanel(self, forecast_data, 1, 0, 2, color['divider color'], forecast_images)

class TallWidget(CTkFrame):
	def __init__(self, parent, current_data, forecast_data, location, color, forecast_images, animation):
		super().__init__(master = parent, fg_color = 'transparent')
		self.pack(expand = True, fill = 'both')

		# layout 
		self.columnconfigure(0, weight = 1, uniform = 'a')
		self.rowconfigure(0, weight = 3, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')

		# widgets 
		SimpleTallPanel(self, current_data, location, 0, 0, color, animation)
		HorizontalForecastPanel(self, forecast_data, 0, 1, 1, color['divider color'], forecast_images)

class MaxWidget(CTkFrame):
	def __init__(self, parent, current_data, forecast_data, location, color, forecast_images, animation):
		super().__init__(master = parent, fg_color = 'transparent')
		self.pack(expand = True, fill = 'both')

		# layout 
		self.columnconfigure((0,1), weight = 1, uniform = 'a')
		self.rowconfigure(0, weight = 1, uniform = 'a')

		# widgets 
		SimpleTallPanel(self, current_data, location, 0, 0, color, animation)
		VerticalForecastPanel(self, forecast_data, 1, 0, color['divider color'], forecast_images)