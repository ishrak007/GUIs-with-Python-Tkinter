import customtkinter as ctk
import tkinter as tk
from draw_surface import *
from settings import *
from tool_panel import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title('')
        self.iconbitmap(r'###Projects\6- Paint app\images\empty.ico')
        ctk.set_appearance_mode('light')
        
        # data
        self.brush_size = 0.2
        self.color_string = tk.StringVar(value=f"#000")
        self.brush_float = tk.DoubleVar(value=self.brush_size)
        self.erase_bool = ctk.BooleanVar()
        
        # draw surface
        self.draw_surface = DrawSurface(self)
        self.tool_panel = ToolPanel(self, self.clear_canvas, self.erase_bool, self.color_string, self.brush_float)
        self.erase_bool.set(False)
        
        # events
        self.bind("<MouseWheel>", self.adjust_brush_size)

        # run
        self.mainloop()
        
    def adjust_brush_size(self, event):
        direction = event.delta
        self.brush_size = self.brush_float.get() 
        change = 0.05 if direction > 0 else -0.05
        self.brush_size += change
        new_brush_size = max(0.2, min(1, self.brush_size))
        self.brush_float.set(new_brush_size)
        
    def clear_canvas(self):
        self.draw_surface.delete("all")
        self.erase_bool.set(False)
        self.brush_float.set(0.2)
        self.color_string.set("#000")

if __name__ == "__main__":
   App() 