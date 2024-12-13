from customtkinter import CTkFrame

class SmallWidget(CTkFrame):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'red')
		self.pack(expand = True, fill = 'both')

class WideWidget(CTkFrame):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'blue')
		self.pack(expand = True, fill = 'both')

class TallWidget(CTkFrame):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'green')
		self.pack(expand = True, fill = 'both')

class MaxWidget(CTkFrame):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'yellow')
		self.pack(expand = True, fill = 'both')