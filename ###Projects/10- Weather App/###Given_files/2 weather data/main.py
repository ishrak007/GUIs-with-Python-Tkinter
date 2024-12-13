import customtkinter as ctk
from settings import *
from main_widgets import *

# url request
import urllib.request
import json
from weather_data import get_weather

try:
	from ctypes import windll, byref, sizeof, c_int
except:
	pass

class App(ctk.CTk):
	def __init__(self):

		self.color = WEATHER_DATA['Clear']

		super().__init__(fg_color = self.color['main'])
		self.title_bar_color(self.color['title'])
		self.geometry('550x250')
		self.minsize(550,250)
		self.title('')
		self.iconbitmap('empty.ico')

		# start widget
		self.widget = SmallWidget(self)

		# states 
		self.height_break = 600
		self.width_break = 1000
		self.full_height_bool = ctk.BooleanVar(value = False)
		self.full_width_bool = ctk.BooleanVar(value = False)
		self.bind('<Configure>', self.check_size)
		self.full_width_bool.trace('w', self.change_size)
		self.full_height_bool.trace('w', self.change_size)

		self.mainloop()

	def title_bar_color(self, color):
		try:
			HWND = windll.user32.GetParent(self.winfo_id())
			windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(color)), sizeof(c_int))
		except:
			pass

	def check_size(self, event):
		if event.widget == self:
			# width 
			if self.full_width_bool.get():
				if event.width < self.width_break:
					self.full_width_bool.set(False)
			else:
				if event.width > self.width_break:
					self.full_width_bool.set(True)

			# height
			if self.full_height_bool.get():
				if event.height < self.height_break:
					self.full_height_bool.set(False)
			else:
				if event.height > self.height_break:
					self.full_height_bool.set(True)

	def change_size(self, *args):
		self.widget.pack_forget()

		# max widget
		if self.full_height_bool.get() and self.full_width_bool.get():
			self.widget = MaxWidget(self)

		# tall widget
		if self.full_height_bool.get() and not self.full_width_bool.get():
			self.widget = TallWidget(self)

		# wide widget
		if not self.full_height_bool.get() and self.full_width_bool.get():
			self.widget = WideWidget(self)

		# min widget
		if not self.full_height_bool.get() and not self.full_width_bool.get():
			self.widget = SmallWidget(self)

if __name__ == '__main__':
	# location 
	with urllib.request.urlopen("https://ipapi.co/json/") as url:
		data = json.loads(url.read().decode())
		city = 'London'# data['city']
		country = 'United Kingdom'# data['country_name']
		latitude = 51.5 # data['latitude']
		longitude = 0.13 # data['longitude']

	# weather information
	current_data = get_weather(latitude, longitude, 'metric', 'today')
	forecast_data = get_weather(latitude, longitude, 'metric', 'forecast')
	print(forecast_data)
	App()