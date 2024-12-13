import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import qrcode

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="#cfcfca")
        
        # window
        self._set_appearance_mode("light")
        self.iconbitmap(r"###Projects\1- QR Code Generator\Images\empty.ico")
        self.title('')
        self.geometry('400x400')
        
        # background
        self.bg_canvas = Background(self, image_path = r"###Projects/1- QR Code Generator/Images/Mirrored-P1304a1-1.jpg")
        # r"###Projects/1- QR Code Generator/Images/Mirrored-P1304a1-1.jpg"  
        
        self.label = ctk.CTkLabel(self, 
                                  text="Generate QR Code",
                                  text_color="black",
                                  font=("Times New Roman", 18, "bold"))
        self.label.place(relx=0.5, rely=0.15, anchor="center")
        
        # bottom pane with Entry field
        self.entry_string = ctk.StringVar()
        self.entry_string.trace_add("write", self.create_qr)
        self.bottom_pane = EntryFrame(self, self.entry_string)
        
        # QR image
        self.raw_img = None # Image.open(r"###Projects\1- QR Code Generator\Images\Placeholder.png").resize((400,400))
        self.raw_img_tk = None # ImageTk.PhotoImage(self.raw_img)
        self.qr_image = QrImage(self)
        # self.qr_image.update_image(self.raw_img_tk)

        # events
        self.bind("<Return>", self.save_image)

        # run
        self.mainloop()
        
    def create_qr(self, *args):
        current_text = self.entry_string.get()
        if current_text:
            self.raw_img = qrcode.make(current_text).resize((400,400))
            self.raw_img_tk = ImageTk.PhotoImage(self.raw_img)
            self.qr_image.update_image(self.raw_img_tk)
        else:
            self.qr_image.clear_image()
            
    def save_image(self, *event): 
        # bind method automatically inserts 1 argument to the function
        # Hence event is inserted as an argument 
        # event is made optional positional argument as the button command does not need any event to work
        if self.raw_img:
            file_path = filedialog.asksaveasfilename()
            
            if file_path:
                self.raw_img.save(file_path + ".jpg")
        
class Background(tk.Canvas):
    def __init__(self, master, **kw):
        self.kw = kw
        self.image_path = self.kw["image_path"]
        super().__init__(master=master)
        self.pack(expand=True, fill="both")
        self.background_image = Image.open(self.image_path)
        self.background_photo = None
        self.bind("<Configure>", self.stretch_image)
         
    def stretch_image(self, event):
    
        # canvas size
        width = event.width
        height = event.height
        
        # creating image
        resized_img = self.background_image.resize((width, height))
        self.background_photo = ImageTk.PhotoImage(resized_img)
        
        # placing image on the canvas
        self.create_image((0,0), image=self.background_photo, anchor="nw") 
        
class QrImage(ctk.CTkCanvas):
    def __init__(self, master):
        super().__init__(master = master, background = 'white')
        self.place(relx=0.5, rely=0.45, width=400, height=400, anchor='center')

    def update_image(self, image_tk):
        self.clear_image()
        self.create_image((0,0), image =image_tk, anchor = 'nw')
        
    def clear_image(self):
        self.delete('all')
            
class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, entry_string):
        super().__init__(master=master, fg_color="#2e2e2d")
        self.place(relx=0.5, rely=0.95, relwidth=1, relheight=0.4, anchor="center")
        
        # grid layout
        self.rowconfigure((0,1), weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        
        # bottom frame
        self.bottom_frame = ctk.CTkFrame(self, fg_color="black")
        self.bottom_frame.grid(row=1, column=0, sticky="nsew")
        self.bottom_canvas = tk.Canvas(self.bottom_frame, background="black", bd=0, highlightthickness=0, relief="ridge")
        self.bottom_canvas.pack(expand=True, fill="x")
        self.bottom_img = Image.open(r"###Projects\1- QR Code Generator\Images\gray_bg.jpg")
        self.resized_img_tk = None
        self.bottom_canvas.bind("<Configure>", self.stretch_image)
        
        # the main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        self.main_frame.columnconfigure(0, weight=1, uniform="b")
        self.main_frame.columnconfigure(1, weight=4, uniform="b")
        self.main_frame.columnconfigure(2, weight=2, uniform="b")
        self.main_frame.columnconfigure(3, weight=1, uniform="b")
        self.main_frame.rowconfigure(0, weight=1, uniform="b")
        
        # widgets
        self.entry = ctk.CTkEntry(self.main_frame, 
                                  fg_color="white",
                                  text_color="black",
                                  textvariable=entry_string
                                  )
        self.entry.grid(row=0, column=1, sticky="ew")
        
        self.button = ctk.CTkButton(self.main_frame, 
                                    text = "Save",
                                    command = lambda: master.save_image()
                                    )
        self.button.grid(row=0, column=2, padx=10)
        
    def stretch_image(self, event):
        
        # canvas size
        width = event.width
        height = event.height
        
        # creating image
        resized_img = self.bottom_img.resize((width, height))
        self.resized_img_tk = ImageTk.PhotoImage(resized_img)
        
        # placing image on the canvas
        self.bottom_canvas.create_image((0,0), image=self.resized_img_tk, anchor="nw")
        
app = App()