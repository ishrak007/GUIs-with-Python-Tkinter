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
		self.control_buttons = ControlButtons(
			parent = self, 
			font = self.button_font,
			start = self.start,
			pause = self.pause,
			resume = self.resume,
			reset = self.reset,
			create_lap = self.create_lap
			)

		# run the app
		self.mainloop()

	def start(self):
		print('start')

	def pause(self):
		print('pause')

	def resume(self):
		print('resume')

	def reset(self):
		print('reset')

	def create_lap(self):
		print('lap')

class ControlButtons(ctk.CTkFrame):
	def __init__(self, parent, font, start, pause, resume, reset, create_lap):
		super().__init__(master = parent, corner_radius = 0, fg_color = 'transparent')
		self.grid(column = 0, row = 1, sticky = 'nsew')

		# interaction methods 
		self.start = start
		self.pause = pause
		self.resume = resume
		self.reset = reset
		self.create_lap = create_lap

		# state
		self.state = 'off'

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
			command = self.lap_handler,
			state = 'disabled',
			fg_color = GREY,
			font = font)
		# start/stop button 
		self.start_button = ctk.CTkButton(
			master = self,
			text = 'Start',
			command = self.start_handler,
			fg_color = GREEN,
			hover_color = GREEN_HIGHLIGHT,
			text_color = GREEN_TEXT,
			font = font
			)

		# place the buttons
		self.lap_button.grid(row = 0, column = 1, sticky = 'nsew')
		self.start_button.grid(row = 0, column = 3, sticky = 'nsew')

	def start_handler(self):
		if self.state == 'off':
			self.start()
			self.state = 'on'
		elif self.state == 'on':
			self.pause()
			self.state = 'pause'
		elif self.state == 'pause':
			self.resume()
			self.state = 'on'
		self.update_button()

	def lap_handler(self):
		if self.state == 'on':
			self.create_lap()
		else:
			self.reset()
			self.state = 'off'
		self.update_button()

	def update_button(self):
		if self.state == 'off':
			pass
		elif self.state == 'on':
			self.lap_button.configure(state = 'normal')
		elif self.state == 'pause':
			pass

if __name__ == '__main__':
	App()