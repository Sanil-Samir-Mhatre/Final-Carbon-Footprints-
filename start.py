import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import Pillow for image handling

def open_login():
    root.destroy()
    import login

def close_program():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Carbon Footprints Calculator")
root.geometry("1535x813+2+42")  # Set the window size and position
root.state('zoomed')  # Maximize the window

# Load background image
bg_image = Image.open("background.jpg")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover entire window

# Return Button
return_button = tk.Button(root, text="Return", command=close_program, font=("Comic Sans MS", 16), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.05, anchor="ne")

# Title
title_label = tk.Label(root, text="Carbon Footprints Calculator", font=("Comic Sans MS", 42, "bold"), fg="green", bg="white")
title_label.place(relx=0.5, rely=0.2, anchor="center")

# Subtitle
subtitle_label = tk.Label(root, text="For Computer Department of College with Automated and Manual Input System", font=("Comic Sans MS", 28), fg="darkgreen", bg="white")
subtitle_label.place(relx=0.5, rely=0.3, anchor="center")

# Start Button
start_button = tk.Button(root, text="Start", command=open_login, font=("Comic Sans MS", 20, "bold"), bg="green", fg="white", padx=20, pady=10)
start_button.place(relx=0.5, rely=0.5, anchor="center")

# Run the application
root.mainloop()
