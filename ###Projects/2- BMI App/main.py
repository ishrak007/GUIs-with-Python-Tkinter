import tkinter as tk
import customtkinter as ctk
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = GREEN)
        
        # window setup
        self._set_appearance_mode("light")
        self.iconbitmap(r"###Projects\2- BMI App\empty.ico")
        self.title('')
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()
        
        # layout
        self.columnconfigure(0, weight =1)
        self.rowconfigure((0,1,2,3), weight =1, uniform = 'a')

        # display strings
        # mode
        self.mode_var = tk.StringVar(value="Metric")
        
        # weight
        self.weight = WEIGHT
        self.weight_str = tk.StringVar(value=WEIGHT)
        
        # height
        self.height = HEIGHT
        self.height_float = tk.DoubleVar(value=HEIGHT)
        self.height_str = tk.StringVar()
        
        # result
        self.result_str = tk.StringVar()
        self.calculate_bmi()

        # widgets
        self.result_text = ResultText(self)
        self.weight_input = WeightInput(self)
        self.height_input = HeightInput(self)
        self.mode_button = Mode(self)

        # events
        self.bind("<Escape>", lambda event: self.destroy())

        # run
        self.mainloop()
        
    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX_COLOR
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass
        
    def calculate_bmi(self):
        weight = round(self.weight, 1)
        height = round(self.height_float.get(), 2)
        bmi = weight / (height**2)
        self.result_str.set(f"{bmi:.1f}")
        
class ResultText(ctk.CTkLabel):
    def __init__(self, master):
        font = ctk.CTkFont(family = FONT, size = MAIN_TEXT_SIZE, weight="bold")
        super().__init__(master = master, 
                         font = font,
                         textvariable = master.result_str
                         )
        self.grid(column = 0, row = 0, rowspan = 2, sticky = 'nsew')

class WeightInput(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color=WHITE)
        self.grid(column = 0, row = 2, sticky = 'nsew', padx=10, pady=2)
        self.update_weight()
        self.oz = 0

        # layout
        self.columnconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        
        # widgets
        # button 1
        button_1 = ctk.CTkButton(self,
                                 fg_color=LIGHT_GRAY,
                                 font=(FONT, INPUT_FONT_SIZE),
                                 text_color=BLACK,
                                 hover_color=GRAY,
                                 text="-",
                                 command = lambda: self.change_weight(1)
                                 )
        button_1.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nswe")

        # button 2
        button_2 = ctk.CTkButton(self,
                                 fg_color=LIGHT_GRAY,
                                 font=(FONT, INPUT_FONT_SIZE),
                                 text_color=BLACK,
                                 hover_color=GRAY,
                                 text="-",
                                 command = lambda: self.change_weight(2)
                                 )
        button_2.grid(row=0, column=2, padx=5, pady=5, sticky="we")

        # button 3
        button_3 = ctk.CTkButton(self,
                                 fg_color=LIGHT_GRAY,
                                 font=(FONT, INPUT_FONT_SIZE),
                                 hover_color=GRAY,
                                 text_color=BLACK,
                                 text="+",
                                 command = lambda: self.change_weight(3)
                                 )
        button_3.grid(row=0, column=6, padx=5, pady=5, sticky="we")
        
        # button 4
        button_4 = ctk.CTkButton(self,
                                 fg_color=LIGHT_GRAY,
                                 text_color=BLACK,
                                 hover_color=GRAY,
                                 font=(FONT, INPUT_FONT_SIZE),
                                 text="+",
                                 command = lambda: self.change_weight(4)
                                 )
        button_4.grid(row=0, column=7, columnspan=2, padx=5, pady=5, sticky="nswe")

        # Weight label
        weight_label = ctk.CTkLabel(self,
                                    fg_color="transparent",
                                    text_color=BLACK,
                                    font=(FONT, INPUT_FONT_SIZE),
                                    textvariable=master.weight_str
                                    )
        weight_label.grid(row=0, column=3, columnspan=3, padx=5, pady=5, sticky="nswe")
        
    def change_weight(self, button_no):
        
        current_mode = self.master.mode_var.get()
        
        if current_mode == "Metric":
            if button_no == 1:
                self.master.weight -= 1
            elif button_no == 2:
                self.master.weight -= 0.1
            elif button_no == 3:
                self.master.weight += 0.1
            elif button_no == 4:
                self.master.weight += 1
        else:
            pounds, ounces = self.unit_converter()               
            if button_no == 1:
                pounds -= 1
                self.master.weight -= (1/2.205)
            elif button_no == 2:
                ounces -= 1
                self.master.weight -= (1/35.274)       
            elif button_no == 3:
                ounces += 1
                self.master.weight += (1/35.274)
            elif button_no == 4:
                pounds += 1
                self.master.weight += (1/2.205)
            
        # update bmi
        self.master.calculate_bmi()
        
        # update weight display
        self.update_weight()
        
    def update_weight(self):    
        if self.master.mode_var.get() == "Metric":
            weight = round(self.master.weight, 1)
            self.master.weight_str.set(f"{weight}kg")
        else:
            pounds, ounces = self.unit_converter()
            self.master.weight_str.set(f"{pounds}lb {ounces}oz")
        
    def unit_converter(self):
        imperial_lb = self.master.weight * 2.20462
        pounds = int(imperial_lb)
        ounces = int((imperial_lb - pounds) * 16)    
        return [pounds, ounces]
        
class HeightInput(ctk.CTkFrame):
    def __init__(self, master):
        self.font = ctk.CTkFont(family=FONT, size=INPUT_FONT_SIZE)
        super().__init__(master=master, fg_color=WHITE)
        self.grid(row=3, column=0, sticky = 'nsew', padx=10, pady=8)
        self.update_height()

        # layout
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform="a")

        # widgets
        # slider
        self.height_slider = ctk.CTkSlider(self,
                               button_color=GREEN,
                               progress_color=GREEN,
                               button_hover_color=DARK_GREEN,
                               fg_color=LIGHT_GRAY,
                               width=18,
                               from_=0.5,
                               to=3,
                               variable=self.master.height_float,
                               command = lambda height: self.change_height(height)
                               )
        self.height_slider.grid(row=0, column=0, columnspan=7, sticky="we", padx=5, pady=5)

        # height_label
        self.height_label = ctk.CTkLabel(self,
                                    fg_color="transparent",
                                    text_color=BLACK,
                                    text="0",
                                    font=self.font,
                                    textvariable = self.master.height_str
                                    )
        self.height_label.grid(row=0, column=7, columnspan=2, sticky="we", padx=5, pady=5)
        
    def change_height(self, height):
        
        # change height
        self.master.height = height
        
        # update bmi
        self.master.calculate_bmi()
        
        # update height display
        self.update_height()
        
    def update_height(self):
        
        if self.master.mode_var.get() == "Metric":
            self.master.height_str.set(f"{self.master.height:.2f}m")
        else:
            imperial_ft = self.master.height * 3.28084
            feet = int(imperial_ft)
            inches = int((imperial_ft - feet) * 12)
            self.master.height_str.set(f"{feet}'{inches}\"")

class Mode(ctk.CTkFrame):
    def __init__(self, master):
        self.font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight="bold")
        super().__init__(master=master, fg_color="transparent")
        self.place(relx=1, rely=0, anchor="ne")
        
        # mode button
        self.mode_button = ctk.CTkButton(master=self, 
                                         fg_color="transparent",
                                         font=self.font,
                                         text_color=DARK_GREEN,
                                         hover=False,
                                         textvariable=self.master.mode_var,
                                         anchor="left",
                                         command=self.change_mode
                                         )
        self.mode_button.pack()
        
    def change_mode(self):
        
        # setting the modes
        if self.master.mode_var.get() == "Metric":
            self.master.mode_var.set("Imperial")
        else:
            self.master.mode_var.set("Metric")

        # update the displays
        self.master.weight_input.update_weight()
        self.master.height_input.update_height()

if __name__ == '__main__':
    app = App()
    