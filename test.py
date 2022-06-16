import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


root = tk.Tk()


# Load the JPG file
img_canada_flag = Image.open(os.path.dirname(__file__).replace("\\", "/") + "/adol_0.png")
img_canada_flag= img_canada_flag.resize((42,42))

# Convert the JPG image to a PhotoImage instance that tkinter can use.
image_tk = ImageTk.PhotoImage(img_canada_flag)

# Define columns
column_names = ("dwelling_type_column", "location_column")

# Pass the column names when we make the treeview.
treeview_places = ttk.Treeview(columns=column_names)

# Create the column texts that the user will see.
treeview_places.heading("dwelling_type_column", text="Dwelling Type")
treeview_places.heading("location_column", text="Location")


treeview_places.insert(parent="",
                     index="end",
                     image=image_tk,
                     values=("House", "Fantasy Land"))


treeview_places.pack(expand=True, fill=tk.BOTH)

root.mainloop()
