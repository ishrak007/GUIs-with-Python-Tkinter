import customtkinter as ctk
from settings import *

class App(ctk.CTk):
	def __init__(self):

		# window setup 
		super().__init__(fg_color = BLACK)
		self.title('')
		self.geometry('300x600')
		self.iconbitmap('empty.ico')
		self.resizable(False, False)

		# grid layout
		self.rowconfigure(0, weight = 5, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.rowconfigure(2, weight = 4, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')

		# fonts 
		self.button_font = ctk.CTkFont(family = FONT, size = BUTTON_FONT_SIZE)

		# widgets 
		self.control_buttons = ControlButtons(self, self.button_font)

		# run the app
		self.mainloop()

class ControlButtons(ctk.CTkFrame):
	def __init__(self, parent, font):
		super().__init__(master = parent, corner_radius = 0, fg_color = 'transparent')
		self.grid(column = 0, row = 1, sticky = 'nsew')

		# grid layout
		self.rowconfigure(0, weight = 1)
		self.columnconfigure(0, weight = 1, uniform = 'b')
		self.columnconfigure(1, weight = 9, uniform = 'b')
		self.columnconfigure(2, weight = 1, uniform = 'b')
		self.columnconfigure(3, weight = 9, uniform = 'b')
		self.columnconfigure(4, weight = 1, uniform = 'b')

		# lap/reset button
		self.lap_button = ctk.CTkButton(
			master = self,
			text = 'Lap',
			command = lambda: print('lap'),
			state = 'disabled',
			fg_color = GREY,
			font = font)
		# start/stop button 
		self.start_button = ctk.CTkButton(
			master = self,
			text = 'Start',
			command = lambda:print('start'),
			fg_color = GREEN,
			hover_color = GREEN_HIGHLIGHT,
			text_color = GREEN_TEXT,
			font = font
			)

		# place the buttons
		self.lap_button.grid(row = 0, column = 1, sticky = 'nsew')
		self.start_button.grid(row = 0, column = 3, sticky = 'nsew')

if __name__ == '__main__':
	App()