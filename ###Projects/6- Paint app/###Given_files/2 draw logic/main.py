import customtkinter as ctk 
from draw_surface import DrawSurface

class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry('800x600')
		self.title('')
		self.iconbitmap('empty.ico')
		ctk.set_appearance_mode('light')

		# data 
		self.color_string = ctk.StringVar(value = '000')
		self.brush_float = ctk.DoubleVar(value = 1) # 0.2 -> 1

		# widgets 
		DrawSurface(self, self.color_string, self.brush_float)

		self.mainloop()

if __name__ == '__main__':
	App()