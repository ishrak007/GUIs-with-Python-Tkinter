import customtkinter as ctk
import tkinter as tk
from settings import *
from PIL import Image

class ToolPanel(ctk.CTkToplevel):
    def __init__(self, master, clear_canvas, erase_bool, color_string, brush_float):
        super().__init__()
        self.geometry('200x380')
        self.title('')
        self.resizable(False, False)
        self.iconbitmap(r'###Projects\6- Paint app\images\empty.ico')
        self.attributes('-topmost', True)
        self.protocol("WM_DELETE_WINDOW", self.close_app)
        self.master = master
        self.erase_bool = erase_bool
        self.color_string = color_string
        self.brush_float = brush_float
        self.red = tk.IntVar(value=0)
        self.green = tk.IntVar(value=0)
        self.blue = tk.IntVar(value=0)
        self.color_string.trace_add("write", self.adjust_color_sliders)
        
        # layout
        self.columnconfigure((0,1,2), weight=1, uniform="a")
        self.rowconfigure((0,1,2,3,4,5,6), weight=1, uniform="a")

        # brush size slider
        self.brush_slider_frame = ctk.CTkFrame(self)
        self.brush_slider = ctk.CTkSlider(self.brush_slider_frame, 
                                          button_corner_radius=100,
                                          progress_color=BUTTON_COLOR,
                                          button_hover_color=BUTTON_HOVER_COLOR,
                                          from_=0.2,
                                          to=1,
                                          variable=self.brush_float,
                                          width=15,
                                          height=15
                                          )
        self.brush_slider.pack(expand=True, fill="x")
        self.brush_slider_frame.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="nswe")
    
        # color panel
        self.color_panel = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        self.color_panel.grid(row=2, column=0, rowspan=3, columnspan=3, padx=5, pady=5, sticky="nswe")
        self.color_panel.rowconfigure((0,1,2,3,4,5), weight=1, uniform="a")
        self.color_panel.columnconfigure((0,1,2,3), weight=1, uniform="a")
        for row_no, row in enumerate(COLORS):
            for col_no, color in enumerate(row):
                ColorButton(self.color_panel, row_no=row_no, col_no=col_no, color=color, erase_bool=self.erase_bool)
                
        # color mixer
        self.color_mixer = ctk.CTkFrame(self, fg_color="transparent")
        self.color_mixer.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="nswe")
        self.color_mixer.columnconfigure(0, weight=1, uniform="a")
        self.color_mixer.rowconfigure((0,1,2), weight=1, uniform="a")
        for row, color in enumerate([SLIDER_RED, SLIDER_GREEN, SLIDER_BLUE]):
            slider_frame = ctk.CTkFrame(self.color_mixer, fg_color="#DDD")
            slider_frame.grid(row=row, column=0, sticky="we")
            color_name = color[0]
            color_value = color[1]
            hover_color = color[2]
            color_variable = self.red if color_name == "Red" else self.green if color_name == "Green" else self.blue
            ColorSlider(slider_frame, color_name, color_value, hover_color, color_variable, self.erase_bool).pack(expand=True, fill="both")
        
        # buttons
        draw_brush = DrawBrushButton(self, self.erase_bool)
        erase_button = EraserButton(self, self.erase_bool)
        ClearAllButton(self, clear_canvas)
            
        # brush preview
        self.brush_preview = BrushPreview(self, self.color_string, self.brush_float, self.erase_bool)
                                       
    def close_app(self):
        self.master.quit()
        
    def color_picker(self, color):
        self.color_string.set(f"#{color}")
        self.erase_bool.set(False)
        
    def color_maker(self, name, value):
        match name:
            case "Red": self.red.set(int(value))
            case "Green": self.green.set(int(value))
            case "Blue": self.blue.set(int(value))
        red = COLOR_RANGE[self.red.get()]
        green = COLOR_RANGE[self.green.get()]
        blue = COLOR_RANGE[self.blue.get()]
        self.color_string.set(f"#{red}{green}{blue}")
        self.erase_bool.set(False)

    def adjust_color_sliders(self, *args):
        current_color = self.color_string.get().split('#')[1]
        self.red.set(COLOR_RANGE.index(current_color[0]))
        self.green.set(COLOR_RANGE.index(current_color[1]))
        self.blue.set(COLOR_RANGE.index(current_color[2]))
    
class BrushPreview(ctk.CTkCanvas):
    def __init__(self, master, color_string, brush_float, erase_bool):
        super().__init__(master=master, background=BRUSH_PREVIEW_BG, bd=0, highlightthickness=0, relief="ridge")
        self.grid(row=0, rowspan=2, column=1, columnspan=2, padx=12, pady=12, sticky="nswe")
        
        # data
        self.x = 0
        self.y = 0
        self.max_length = 0
        self.color_string = color_string
        self.brush_float = brush_float
        self.erase_bool = erase_bool
        self.bind("<Configure>", self.setup)
        self.color_string.trace_add("write", self.update)
        self.brush_float.trace_add("write", self.update)
        self.erase_bool.trace_add("write", self.update)
        
    def setup(self, event):
        self.x = event.width / 2
        self.y = event.height / 2
        self.max_length = (event.height / 2) * 0.8
        self.update()
        
    def update(self, *args):
        self.delete("all")
        current_radius = self.max_length * self.brush_float.get()
        current_color = self.color_string.get() if not self.erase_bool.get() else BRUSH_PREVIEW_BG
        outline_color = self.color_string.get() if not self.erase_bool.get() else "#000"
        self.create_oval(self.x - current_radius,
                        self.y - current_radius,
                        self.x + current_radius,
                        self.y + current_radius,
                        fill = current_color,
                        outline= outline_color
                        )
        
class ColorSlider(ctk.CTkSlider):
    def __init__(self, master, color_name, color_value, hover_color, color_variable, erase_bool):    
        self.erase_bool = erase_bool
        super().__init__(master=master,
                         button_color=color_value,
                         fg_color=BUTTON_COLOR,
                         progress_color=color_value,
                         button_hover_color=hover_color,
                         from_=0,
                         to=15,
                         number_of_steps=16,
                         variable=color_variable,
                         command=lambda value: master.master.master.color_maker(color_name, value), # lambda value: print(COLOR_RANGE[int(value)])
                         width=14,
                         height=14,
                         )
                                          
class ColorButton(ctk.CTkButton):
    def __init__(self, master, color, row_no, col_no, erase_bool):
        # hover color is 2 shades lighter unless its 0
        self.erase_bool = erase_bool
        fg_color = f"#{color}"
        self.red = COLOR_RANGE.index(color[0])
        self.green = COLOR_RANGE.index(color[1])
        self.blue = COLOR_RANGE.index(color[2])
        self.red -= 2 if self.red > 0 else -2
        self.green -= 2 if self.green > 0 else -2
        self.blue -= 2 if self.blue > 0 else -2
        hover_color = f"#{COLOR_RANGE[self.red]}{COLOR_RANGE[self.green]}{COLOR_RANGE[self.blue]}"
        super().__init__(master=master,
                         text="", 
                         fg_color=fg_color,
                         hover_color=hover_color,
                         corner_radius=0,
                         command=lambda: master.master.color_picker(color)
                         )
        self.grid(row=row_no, column=col_no, padx=2, pady=2, sticky="nswe")
        
class Button(ctk.CTkButton):
    def __init__(self, master, image_path, col, func):
        image = ctk.CTkImage(light_image = Image.open(image_path), dark_image = Image.open(image_path))
        super().__init__(master = master, command=func, text = '', image = image, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR)
        self.grid(row = 6, column = col, sticky = 'nsew', padx = 5, pady = 5)
        
class DrawBrushButton(Button):
    def __init__(self, master, erase_bool):
        super().__init__(master, func=lambda: self.activate_brush(), image_path=r"###Projects\6- Paint app\images\brush.png", col=0)
        self.erase_bool = erase_bool
        self.erase_bool.trace_add("write", self.update_state)
        
    def activate_brush(self):
        self.erase_bool.set(False)
        
    def update_state(self, *args):
        if not self.erase_bool.get():
            self.configure(fg_color = BUTTON_ACTIVE_COLOR)
        else:
            self.configure(fg_color = BUTTON_COLOR)

class EraserButton(Button):
    def __init__(self, master, erase_bool):
        super().__init__(master, func=lambda: self.activate_erase(), image_path=r"###Projects\6- Paint app\images\eraser.png", col=1)
        self.erase_bool = erase_bool
        self.erase_bool.trace_add("write", self.update_state)
        
    def activate_erase(self):
        self.erase_bool.set(True)
        
    def update_state(self, *args):
        if self.erase_bool.get():
            self.configure(fg_color = BUTTON_ACTIVE_COLOR)
        else:
            self.configure(fg_color = BUTTON_COLOR)

class ClearAllButton(Button):
    def __init__(self, master, clear_canvas):
        super().__init__(master, func=clear_canvas, image_path=r"###Projects\6- Paint app\images\clear.png", col=2)
        
        
        