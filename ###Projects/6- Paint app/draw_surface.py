import tkinter as tk
from settings import *

class DrawSurface(tk.Canvas):
    def __init__(self, master):
        
        # setup
        super().__init__(master=master, background=CANVS_BG, bd=0, highlightthickness=0, relief="ridge")
        self.pack(expand=True, fill="both")
        
        # data
        self.brush_float = self.master.brush_float
        self.allow_draw = False
        self.erase_bool = self.master.erase_bool

        # start pos
        self.old_x = None
        self.old_y = None
        self.end_x = None
        self.end_y = None

        # input
        self.bind('<Motion>', self.draw)
        self.bind('<Button>', self.activate_draw)
        self.bind('<ButtonRelease>', self.deactivate_draw)

    def draw(self, event):
        if self.allow_draw:
            if self.old_x and self.old_y:
                self.create_brush_line((self.old_x, self.old_y), (event.x, event.y))
            self.old_x = event.x
            self.old_y = event.y

    def create_brush_line(self, start, end):
        brush_size = self.brush_float.get() * 10 ** 2
        color = self.master.color_string.get() if not self.erase_bool.get() else "#FFF"
        self.create_line(start, end, fill = color, width = brush_size, capstyle = 'round')  
    
    
    def activate_draw(self, event):
        self.allow_draw = True
        self.create_brush_line((event.x, event.y), (event.x + 1, event.y + 1))
        
    def deactivate_draw(self, event):
        self.allow_draw = False
        self.old_x = None
        self.old_y = None