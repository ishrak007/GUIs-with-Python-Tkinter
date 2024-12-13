# size
APP_SIZE = (400, 600)

# Text
FONT = "Helvetica"
OUTPUT_FONT_SIZE = 70
NORMAL_FONT_SIZE = 32

STYLING = {"gap": 0.5, "corner-radius": 0}

COLORS = {
    "light-gray": {
        "fg": ("#505050", "#D4D4D2"),
        "hover": ("#686868", "#efefed"),
        "text": ("white", "black"),
    },
    "dark-gray": {
        "fg": ("#D4D4D2", "#505050"),
        "hover": ("#efefed", "#686868"),
        "text": ("black", "white"),
    },
    "orange": {"fg": "#FF9500", "hover": "#ffb143", "text": ("black", "white")},
    "orange-highlight": {"fg": "white", "hover": "white", "text": ("black", "#FF9500")},
}

POSITIONS = {
	# 1st entry inside the tuples is the row while 2nd one is the column
	"AC": (2, 0), "inv": (2, 1), "%": (2, 2), "/": (2, 3),
	"7": (3, 0), "8": (3, 1), "9": (3, 2), "x": (3, 3),
	"4": (4, 0), "5": (4, 1), "6": (4, 2), "-": (4, 3),
	"1": (5, 0), "2": (5, 1), "3": (5, 2), "+": (5, 3),
	"0": (6, 0), ".": (6, 2), "=": (6, 3)
}


# image locations

# # Load an image using CTkImage (supports PNG, JPG)
# image = ctk.CTkImage(light_image="button_image_light.png", dark_image="button_image_dark.png", size=(40, 40))

DIVIDE_IMG = {"light_image": r"###Projects\4- Calculator\images\divide_light.png", 
          "dark_image": r"###Projects/4- Calculator/images/divide_dark.png"}

INVERT_IMG = {"light_image": r"###Projects\4- Calculator\images\invert_light.png", 
          "dark_image": r"###Projects\4- Calculator\images\invert_dark.png"}

TITLE_BAR_HEX_COLORS = {"dark": 0x00000000, "light": 0x00EEEEEE}

BLACK = "#000000"
WHITE = "#EEEEEE"

FG_COLORS = {"dark": BLACK, "light": WHITE}
