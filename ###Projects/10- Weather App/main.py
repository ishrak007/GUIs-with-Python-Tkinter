import customtkinter as ctk
from settings import *
from main_widgets import *

# url request
import urllib.request
import json
from weather_data import get_weather

# images 
from PIL import Image
from os import walk

try:
	from ctypes import windll, byref, sizeof, c_int
except:
	pass

class App(ctk.CTk):
	def __init__(self, current_data, forecast_data, city, country):

		# data 
		self.current_data = current_data
		self.forecast_data = forecast_data
		self.location = {'city': city, 'country': country}
		self.color = WEATHER_DATA[current_data['weather']]

		# image imports 
		self.forecast_images = [Image.open(f"images/{info['weather']}.png") for info in self.forecast_data.values()]
		self.today_animation = self.import_folder(self.color['path'])

		super().__init__(fg_color = self.color['main'])
		self.title_bar_color(self.color['title'])
		self.geometry('550x250')
		self.minsize(550,250)
		self.title('')
		self.iconbitmap('empty.ico')

		# start widget
		self.widget = SmallWidget(self, self.current_data, self.location, self.color, self.today_animation)

		# states 
		self.height_break = 600
		self.width_break = 1000
		self.full_height_bool = ctk.BooleanVar(value = False)
		self.full_width_bool = ctk.BooleanVar(value = False)
		self.bind('<Configure>', self.check_size)
		self.full_width_bool.trace('w', self.change_size)
		self.full_height_bool.trace('w', self.change_size)

		self.mainloop()

	def import_folder(self, path):
		for _, __, image_data in walk(path):
			sorted_data = sorted(image_data, key = lambda item:int(item.split('.')[0]))
			image_paths = [path + '/' + item for item in sorted_data]

		images = [Image.open(path) for path in image_paths]
		return images

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
			self.widget = MaxWidget(self,
				current_data = self.current_data,
				forecast_data = self.forecast_data,
				location = self.location,
				color = self.color, 
				forecast_images = self.forecast_images, 
				animation = self.today_animation)

		# tall widget
		if self.full_height_bool.get() and not self.full_width_bool.get():
			self.widget = TallWidget(self,
				current_data = self.current_data,
				forecast_data = self.forecast_data,
				location = self.location,
				color = self.color,
				forecast_images = self.forecast_images,
				animation = self.today_animation)

		# wide widget
		if not self.full_height_bool.get() and self.full_width_bool.get():
			self.widget = WideWidget(self,
				current_data = self.current_data,
				forecast_data = self.forecast_data,
				location = self.location,
				color = self.color,
				forecast_images = self.forecast_images,
				animation = self.today_animation)

		# min widget
		if not self.full_height_bool.get() and not self.full_width_bool.get():
			self.widget = SmallWidget(self, self.current_data, self.location, self.color, self.today_animation)

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
	App(current_data = current_data, forecast_data = forecast_data, city = city, country = country)