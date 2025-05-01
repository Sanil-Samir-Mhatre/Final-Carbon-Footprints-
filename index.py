import tkinter as tk
import os
from PIL import Image, ImageTk  # Import Pillow for image handling

def show_printer_carbon_footprints():
    root.destroy()
    os.system('python printer_carbon_footprints.py')

def show_desktop_carbon_footprints():
    root.destroy()
    os.system('python desktop_carbon_footprints.py')

def show_wifi_carbon_footprints():
    root.destroy()
    os.system('python wifi_carbon_footprints.py')

def show_manually_calculated_carbon_footprints():
    root.destroy()
    os.system('python manuallycalculated_carbon_footprints.py')

def show_database():
    root.destroy()
    os.system('python show_db.py')

def show_aiml_analysis():
    root.destroy()
    os.system('python predict.py')

def show_solutions():
    root.destroy()
    os.system('python solutions.py')

def show_conclusion():
    """Close this window and open conclusion.py."""
    root.destroy()
    os.system('python trends.py')

def return_to_login():
    root.destroy()
    os.system('python login.py')

# Create GUI
root = tk.Tk()
root.title("Calculate Carbon Footprints For")
root.geometry("1535x813+2+42")
root.state('zoomed')  # Maximize the window

# Load background image
bg_image = Image.open("background3.jpg")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Configure grid layout
for i in range(6):  # Updated to accommodate the new row
    root.grid_rowconfigure(i, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Add Title
tk.Label(root, text="Carbon Footprints of the Computer Department", font=("Comic Sans MS", 32), bg="white").grid(row=0, column=0, columnspan=3, pady=20)

# Return Button at Top-Right Corner
return_button = tk.Button(root, text="Return", command=return_to_login, font=("Comic Sans MS", 20), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.02, anchor="ne")

# Section 1: Automated Input
tk.Label(root, text="Automated Input", font=("Comic Sans MS", 28), bg="green", fg="white").grid(row=2, column=0, pady=20, sticky="nsew")
tk.Button(root, text="Printer", command=show_printer_carbon_footprints, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=3, column=0, padx=20, pady=20)
tk.Button(root, text="Desktop", command=show_desktop_carbon_footprints, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=4, column=0, padx=20, pady=20)
tk.Button(root, text="Router", command=show_wifi_carbon_footprints, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=5, column=0, padx=20, pady=10)

# Section 2: Manual Input
tk.Label(root, text="Manual Input", font=("Comic Sans MS", 28), bg="green", fg="white").grid(row=2, column=1, pady=20, sticky="nsew")
tk.Button(root, text="Take Survey", command=show_manually_calculated_carbon_footprints, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=3, column=1, padx=20, pady=20)

#  "General Solutions" Button Below "Take Survey"
tk.Button(root, text="General Solutions", command=show_solutions, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=4, column=1, padx=20, pady=20)

# Section 3: Carbon Footprints Data
tk.Label(root, text="Carbon Footprints Data", font=("Comic Sans MS", 28), bg="green", fg="white").grid(row=2, column=2, pady=20, sticky="nsew")
tk.Button(root, text="View Database", command=show_database, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=3, column=2, padx=20, pady=20)

# **AIML Data Analysis Button**
tk.Button(root, text="AIML Data Analysis", command=show_aiml_analysis, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=4, column=2, padx=20, pady=20)

# **NEW BUTTON: Conclusion (Below AIML Data Analysis)**
tk.Button(root, text="Trends Analysis\n&\nConclusion", command=show_conclusion, font=("Comic Sans MS", 24), bg="#4CAF50", fg="white").grid(row=5, column=2, padx=20, pady=40)

# Run Application
root.mainloop()
