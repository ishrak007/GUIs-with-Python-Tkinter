import customtkinter as ctk 
from settings import * 

try: 
	from ctypes import windll, byref, sizeof, c_int
except:
	pass

class App(ctk.CTk):
	def __init__(self):
		super().__init__(fg_color = BG_COLOR)
		self.geometry('900x800')
		self.title('')
		self.iconbitmap('empty.ico')
		self.title_bar_color()

		self.mainloop()

	def title_bar_color(self):
		try:
			HWND = windll.user32.GetParent(self.winfo_id())
			windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(TITLE_HEX_COLOR)), sizeof(c_int))
		except:
			pass
App()