import tkinter as tk
import customtkinter as ctk
from settings import *
from PIL import Image
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

class Calculator(ctk.CTk):
    def __init__(self):

        # display mode
        self.mode = "dark"
        super().__init__(fg_color=FG_COLORS[self.mode])
        self.set_mode()

        # window setup
        self.title("")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.iconbitmap(r"###Projects/4- Calculator/images/empty.ico")
        self.resizable(False, False)
        self.change_title_bar_color()
        
        # calculator operation variables
        self.operand_1 = False  # 1st operand
        self.operand_2 = False  # 2nd operand
        self.operand_on_hold = False  # Check if operand 1 exists
        self.operand_cur = False  # Current operand
        self.operation = None  # hold operation ["+", "-", "x", "/"] id of the previous key press
        self.old_key = None  # catch current key
        
        # input display (bottom) & calculation display (top)
        self.input_str = "0"
        self.input_display = tk.StringVar(value=self.input_str)
        self.formula_str = ""
        self.formula_disp = tk.StringVar(value=self.formula_str)
        
        # catching the key presses and passing key id to the calculator brain
        self.key_pressed = tk.StringVar()
        self.key_pressed.trace_add("write", self.calculator_brain)

        # main frame
        self.main_frame = MainFrame(self)
        
        # run
        self.mainloop()
        
    def calculator_brain(self, *args):
        
        # current key
        key = self.key_pressed.get()
        
        # calculator brain
        if key == "AC":  
            
            # Reset Everything
            self.input_str = "0"
            self.formula_str = ""
            self.operand_on_hold = False
            self.operand_1 = False
            self.operand_2 = False
            self.operand_cur = False
            self.operation = False
            self.input_display.set(self.input_str)
            self.formula_disp.set(self.formula_str)
        elif key == "inv": 
            
            # inversion logic
            display = self.input_display.get()    
            if "-" in display:  
                self.input_str = display.replace("-", "")
            else:
                self.input_str = "-" + display
            self.input_display.set(self.input_str)
        elif key in "0123456789.": 
            
            if key == ".":
                # there can only be 1 decimal in the string
                if key not in self.input_str:
                    self.input_str += key if self.input_str else f"0{key}"
            else:  # key is a digit        
                # if display is 0, replace it with a digit
                if self.input_str == "0":
                    self.input_str = key 
                # if display is -0, keep the "-" sign
                elif self.input_str == "-0":
                    self.input_str = "-" + key                
                # concatenate key with input string otherwise
                else:
                    self.input_str += key
            # dont calculate with numbers beyond 9 or so digits 
            if len(self.input_str) > 9:
                self.input_str = self.input_str[:9]
            # show the number in the display 
            self.input_display.set(self.input_str)
        else:  # key in ["+", "-", "x", "/", "%", "="]
            
            # if these keys are pressed more than once, store the operation wanted & update formula display & suppress numbers if above 8 digits & dont proceed further
            if key not in ["=", "%"] and self.old_key in ["+", "-", "x", "/"]:
                self.operation = key
                operand_1 = self.operand_1 if len(str(self.operand_1)) < 8 else f"{self.operand_1:.3e}"
                self.formula_str = f" {operand_1} {key}"
                self.formula_disp.set(self.formula_str)
                return
            
            # input extraction
            # upon press, extract the current input string (if it exists) as the current operand and turn it into float or string
            if self.input_str:  
                self.operand_cur = self.input_str 
                self.operand_cur = float(self.operand_cur) if "." in self.operand_cur else int(self.operand_cur) 
                # if any of these operation keys are pressed, its time to get a new input string    
                self.input_str = "" 
            
            # operand logic
            # if there is no existing operand, this is the first operand, else this is the 2nd one
            if not self.operand_on_hold:
                self.operand_1 = self.operand_cur  
                self.operand_on_hold = True
            else:
                self.operand_2 = self.operand_cur 
                
            # formula display
            if key in ["+", "-", "x", "/", "="]:
                operand_1 = self.operand_1 if len(str(self.operand_1)) < 8 else f"{self.operand_1:.3e}"
                if key != "=":
                    self.formula_str = f" {operand_1} {key}"
                elif self.operation:
                    operand_2 = self.operand_2 if len(str(self.operand_2)) < 8 else f"{self.operand_2:.3e}"
                    self.formula_str = f" {operand_1} {self.operation} {operand_2}"
                self.formula_disp.set(self.formula_str)
            
            # calculate according to the key pressed
            self.math(key)
            
            # note down the wanted operation if any of these operation keys are pressed
            if key in ["+", "-", "x", "/"]:
                self.operation = key
                
        # finally, hold this current key 
        self.old_key = key
    
    def math(self, key):
        """Display the result of the previous operation"""
        a = self.operand_1
        b = self.operand_2
        result = self.operand_cur # if there is no operand 2, result is the current operand
        operator = self.operation
        
        if key == "%" and self.operand_cur != 0:
            self.operand_cur *= 0.01
            result = self.operand_cur
        elif operator == "+":
            result = a + b
        elif operator == "-":
            result = a - b
        elif operator == "x":
            result = a * b
        elif operator == "/":         
            # Prevent 0 division error. Show "Error". Make input str 0          
            if b == 0:
                self.input_display.set("Error")
                return
            result = a / b

        # process result, store it as the holding operand & update the display   
        if 0.0000001 < abs(result) < 999999999 or result == 0:
            if type(result) == float:
                # Output result as an int if it has only 0 after decimal 
                if result.is_integer(): # can use is_integer() as well str(result).split('.')[1] == "0"
                    result = int(result)
                # dont allow display to have more than 10 characters
                else:                    
                    round_here = 10 - len(str(result).split(".")[0]) - 1
                    result = round(result, round_here)               
            self.input_display.set(result) 
        else:
            self.input_display.set(f"{result:.3e}") 

        self.operand_1 = result  
        self.operand_2 = False
            
    def change_title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_BAR_HEX_COLORS[self.mode]
            windll.dwmapi.DwmSetWindowAttribute(
                HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int)
            )
        except:
            pass

    def set_mode(self):
        mode = "dark" if self.mode == "dark" else "light"
        self._set_appearance_mode(mode)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        
        super().__init__(master=master, fg_color="transparent", corner_radius=0)
        self.pack(expand=True, fill="both")

        self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform="a")
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform="a")

        self.place_buttons()
        self.create_display()

    def place_buttons(self):

        # buttons light-gray
        for i in range(11):
            columnspan = 2 if i == 0 else 1
            text = "." if i == 10 else str(i)
            Buttons(self, color="light-gray", text=text, columnspan=columnspan)

        # buttons dark-gray
        for text in ["AC", "inv", "%"]:
            img_info = INVERT_IMG if text == "inv" else None
            Buttons(self, color="dark-gray", text=text, img_info=img_info)
        
        # buttons orange
        for text in ["+", "-", "x", "/", "="]:
            img_info = DIVIDE_IMG if text == "/" else None
            Buttons(self, color="orange", text=text, img_info=img_info)

    def create_display(self):

        # input display
        input_frame = ctk.CTkFrame(self, 
                                   fg_color="transparent", # blue
                                   corner_radius=0,
                                   )
        input_frame.grid(row=1, column=0, columnspan=4, sticky="nswe")
        
        self.display_label = ctk.CTkLabel(input_frame,
                                   fg_color="transparent",
                                   text_color=WHITE,
                                   text="10000",
                                   textvariable=self.master.input_display,
                                   font=(FONT, OUTPUT_FONT_SIZE)
                                   )
        self.display_label.pack(padx=12, pady=5, side="right")
        
        # calculation display
        self.calc_label = ctk.CTkLabel(self,
                                   fg_color="transparent",
                                   text_color=WHITE,
                                   text="10000",
                                   textvariable=self.master.formula_disp,
                                   font=(FONT, NORMAL_FONT_SIZE)
                                   )
        # calc_label.pack(padx=10, pady=5, side="right")
        self.calc_label.grid(row=0, column=0, columnspan=4, padx=12, pady=5, sticky="se")

class Buttons(ctk.CTkButton):
    # kw = [fg_color, text_color, text, pos, ...]
    def __init__(self, master, columnspan=1, img_info=None, **kw):
        self.kw = kw
        self.text = kw["text"]  # 1
        self.id = self.text
        self.color = COLORS[kw["color"]]
        self.font = ctk.CTkFont(family=FONT, size=NORMAL_FONT_SIZE, weight="normal")
        self.pos = POSITIONS[self.text]
        self.row = self.pos[0]
        self.column = self.pos[1]
        self.columnspan = columnspan
        self.corner_radius = STYLING["corner-radius"]
        self.padx = STYLING["gap"]
        self.pady = STYLING["gap"]
        if self.text == "/" or self.text == "inv":
            self.text = ""
        self.img_info = img_info
        self.image = None
        if self.img_info:
            self.image = ctk.CTkImage(light_image=Image.open(self.img_info["dark_image"]),
                                      dark_image=Image.open(self.img_info["light_image"]))
        super().__init__(
            master=master,
            fg_color=self.color["fg"],
            text_color=self.color["text"],
            hover_color=self.color["hover"],
            corner_radius=self.corner_radius,
            font=self.font,
            text=self.text,
            image=self.image,
            command=lambda: master.master.key_pressed.set(self.id)
        )
        self.grid(
            row=self.row,
            column=self.column,
            columnspan=self.columnspan,
            sticky="nswe",
            padx=self.padx,
            pady=self.pady,
        )

if __name__ == "__main__":
    Calculator()