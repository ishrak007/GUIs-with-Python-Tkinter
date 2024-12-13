import customtkinter as ctk
from settings import *
try:
	from ctypes import windll, byref, sizeof, c_int
except:
	pass

class App(ctk.CTk):
	def __init__(self):

		# window setup 
		super().__init__(fg_color = GREEN)
		self.title('')
		self.iconbitmap('empty.ico')
		self.geometry('400x400')
		self.resizable(False, False)
		self.change_title_bar_color()

		# layout 
		self.columnconfigure(0, weight = 1)
		self.rowconfigure((0,1,2,3), weight = 1, uniform = 'a')

		# data 
		self.height_int = ctk.IntVar(value = 170)
		self.weight_float = ctk.DoubleVar(value = 65)
		self.bmi_string = ctk.StringVar()
		self.update_bmi()

		# tracing
		self.height_int.trace('w',self.update_bmi)
		self.weight_float.trace('w',self.update_bmi)

		# widgets 
		ResultText(self, self.bmi_string)
		WeightInput(self, self.weight_float)
		HeightInput(self, self.height_int)
		UnitSwitcher(self)

		self.mainloop()

	def update_bmi(self, *args):
		height_meter = self.height_int.get() / 100
		weight_kg = self.weight_float.get()
		bmi_result = round(weight_kg / height_meter ** 2,2)
		self.bmi_string.set(bmi_result)

	def change_title_bar_color(self):
		try:
			HWND = windll.user32.GetParent(self.winfo_id())
			DWMWA_ATTRIBUTE = 35
			COLOR = TITLE_HEX_COLOR
			windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
		except:
			pass

class ResultText(ctk.CTkLabel):
	def __init__(self, parent, bmi_string):
		font = ctk.CTkFont(family = FONT, size = MAIN_TEXT_SIZE, weight = 'bold')
		super().__init__(master = parent, text = 22.5, font = font, text_color = WHITE, textvariable = bmi_string)
		self.grid(column = 0, row = 0, rowspan = 2, sticky = 'nsew')

class WeightInput(ctk.CTkFrame):
	def __init__(self, parent, weight_float):
		super().__init__(master = parent, fg_color = WHITE)
		self.grid(column = 0, row = 2, sticky = 'nsew', padx = 10, pady = 10)
		self.weight_float = weight_float

		# layout 
		self.rowconfigure(0, weight = 1, uniform = 'b')
		self.columnconfigure(0, weight = 2, uniform = 'b')
		self.columnconfigure(1, weight = 1, uniform = 'b')
		self.columnconfigure(2, weight = 3, uniform = 'b')
		self.columnconfigure(3, weight = 1, uniform = 'b')
		self.columnconfigure(4, weight = 2, uniform = 'b')

		# text
		font = ctk.CTkFont(family = FONT, size = INPUT_FONT_SIZE)
		label = ctk.CTkLabel(self, text = '70kg', text_color = BLACK, font = font)
		label.grid(row = 0, column = 2)

		# buttons 
		minus_button = ctk.CTkButton(self, command = lambda: self.update_weight(('minus', 'large')), text = '-', font = font, text_color = BLACK, fg_color = LIGHT_GRAY, hover_color = GRAY, corner_radius = BUTTON_CORNER_RADIUS)
		minus_button.grid(row = 0, column = 0, sticky = 'ns', padx = 8, pady = 8)

		plus_button = ctk.CTkButton(self, command = lambda: self.update_weight(('plus', 'large')), text = '+', font = font, text_color = BLACK, fg_color = LIGHT_GRAY, hover_color = GRAY, corner_radius = BUTTON_CORNER_RADIUS)
		plus_button.grid(row = 0, column = 4, sticky = 'ns', padx = 8, pady = 8)

		small_plus_button = ctk.CTkButton(self, command = lambda: self.update_weight(('plus', 'small')), text = '+', font = font, text_color = BLACK, fg_color = LIGHT_GRAY, hover_color = GRAY, corner_radius = BUTTON_CORNER_RADIUS)
		small_plus_button.grid(row = 0, column = 3,  padx = 4, pady = 4)

		small_minus_button = ctk.CTkButton(self, command = lambda: self.update_weight(('minus', 'small')), text = '-', font = font, text_color = BLACK, fg_color = LIGHT_GRAY, hover_color = GRAY, corner_radius = BUTTON_CORNER_RADIUS)
		small_minus_button.grid(row = 0, column = 1,  padx = 4, pady = 4)

	def update_weight(self, info = None):
		amount = 1 if info[1] == 'large' else 0.1
		if info[0] == 'plus':
			self.weight_float.set(self.weight_float.get() + amount)
		else:
			self.weight_float.set(self.weight_float.get() - amount)

class HeightInput(ctk.CTkFrame):
	def __init__(self, parent, height_int):
		super().__init__(master = parent, fg_color = WHITE)
		self.grid(row = 3, column = 0, sticky = 'nsew', padx = 10, pady = 10)

		# widgets 
		slider = ctk.CTkSlider(
			master = self, 
			button_color = GREEN,
			button_hover_color = GRAY,
			progress_color = GREEN,
			fg_color = LIGHT_GRAY,
			variable = height_int,
			from_ = 100, 
			to = 250)
		slider.pack(side = 'left', fill = 'x', expand = True, pady = 10, padx = 10)

		output_text = ctk.CTkLabel(self, text = '1.80m', text_color = BLACK, font = ctk.CTkFont(family = FONT, size = INPUT_FONT_SIZE))
		output_text.pack(side = 'left', padx = 20)

class UnitSwitcher(ctk.CTkLabel):
	def __init__(self, parent):
		super().__init__(master = parent, text = 'metric', text_color = DARK_GREEN, font = ctk.CTkFont(family = FONT, size = SWITCH_FONT_SIZE, weight = 'bold'))
		self.place(relx = 0.98, rely = 0.01, anchor = 'ne')

if __name__ == '__main__':
	App()