import customtkinter as ctk
import datetime, calendar

class SimplePanel(ctk.CTkFrame):
	def __init__(self, parent, weather, col, row, color):
		super().__init__(master = parent, fg_color = color['main'], corner_radius = 0)
		self.grid(column = col, row = row, sticky = 'nsew')

		# layout 
		self.rowconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure((0,1), weight = 1, uniform = 'a')

		# widgets 
		temp_frame = ctk.CTkFrame(self, fg_color = 'transparent')
		ctk.CTkLabel(temp_frame, text = f"{weather['temp']}\N{DEGREE SIGN}", font = ctk.CTkFont(family = 'Calibri', size = 50), text_color = color['text']).pack()
		ctk.CTkLabel(temp_frame, text = f"feels like: {weather['feels_like']}\N{DEGREE SIGN}", font = ctk.CTkFont(family = 'Calibri', size = 16), text_color = color['text']).pack()
		temp_frame.grid(row = 0, column = 0)

class DatePanel(ctk.CTkFrame):
	def __init__(self, parent, location, col, row, color):
		super().__init__(master = parent, fg_color = color['main'], corner_radius = 0)
		self.grid(column = col, row = row, sticky = 'nsew')

		# location 
		location_frame = ctk.CTkFrame(self, fg_color = 'transparent')
		ctk.CTkLabel(
			location_frame, 
			text = f"{location['city']}, ", 
			font = ctk.CTkFont(family = 'Calibri', size = 20, weight = 'bold'),
			text_color = color['text']).pack(side = 'left')
		ctk.CTkLabel(location_frame, 
			text = f"{location['country']}",
			font = ctk.CTkFont(family = 'Calibri', size = 20),
			text_color = color['text']).pack(side = 'left')
		location_frame.pack(side = 'left', padx = 10)

		# date 
		day, weekday, suffix, month = get_time_info()
		ctk.CTkLabel(self, 
			text = f"{weekday[:3]}, {day}{suffix} {calendar.month_name[month]}",
			font = ctk.CTkFont(family = 'Calibri', size = 20),
			text_color = color['text']).pack(side = 'right', padx = 10)

def get_time_info():
	month = datetime.datetime.today().month
	day = datetime.datetime.today().day
	weekday = list(calendar.day_name)[datetime.datetime.today().weekday()]

	match day % 10:
		case 1: suffix = 'st'
		case 2: suffix = 'nd'
		case 3: suffix = 'rd'
		case _: suffix = 'th'

	return day, weekday, suffix, month