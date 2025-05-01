import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import random
import os
import json
from PIL import Image, ImageTk, ImageGrab  # Added ImageGrab for taking screenshots
import subprocess

# Carbon emission rates (kg CO₂ per page)
CARBON_STANDARD = 0.007  # Updated for standard printing
CARBON_HIGH_QUALITY = 0.012  # Updated for high-quality printing

# Default Printer IP
DEFAULT_PRINTER_IP = "127.0.0.1"

# User details (to be populated from login)
user_role = ""
user_username = ""
user_age = ""

# Load user details from file
with open("user_details.txt", "r") as file:
    user_role = file.readline().strip()
    user_username = file.readline().strip()
    user_age = file.readline().strip()

def mock_printer_data():
    """Simulates printer data instead of fetching from an API."""
    return {
        "model": "HP LaserJet Pro MFP M227fdw",
        "manufacturer": "HP",
        "status": random.choice(["Online", "Offline", "Idle", "Printing"]),
        "connectionType": "WiFi",
        "macAddress": "00:1A:2B:3C:4D:5E",
        "duplex": random.choice([True, False]),
        "pageCount": random.randint(500, 5000),
        "cartridges": {
            "Black": random.randint(20, 100),
            "Cyan": random.randint(5, 20),
            "Magenta": random.randint(20, 100),
            "Yellow": random.randint(5, 20),
        },
        "paperTrays": {
            "Tray 1": random.randint(0, 250),
            "Tray 2": random.randint(0, 250),
        },
    }

def calculate_carbon_footprint(page_count, print_type):
    """Calculate carbon footprint based on page count and print type."""
    carbon_per_page = CARBON_STANDARD if print_type == "Standard" else CARBON_HIGH_QUALITY
    return round(page_count * carbon_per_page, 4)

def fetch_and_display_data():
    """Fetch printer data and update the GUI."""
    printer_ip = ip_entry.get().strip()
    print_type = print_type_var.get()

    if not printer_ip:
        messagebox.showerror("Error", "Please enter a valid printer IP address.")
        return

    printer_data = mock_printer_data()
    page_count = printer_data["pageCount"]
    carbon_footprint = calculate_carbon_footprint(page_count, print_type)

    # Update Labels
    printer_model_var.set(f"Model: {printer_data['model']}")
    manufacturer_var.set(f"Manufacturer: {printer_data['manufacturer']}")
    status_var.set(f"Status: {printer_data['status']}")
    connection_var.set(f"Connection: {printer_data['connectionType']}")
    mac_var.set(f"MAC Address: {printer_data['macAddress']}")
    duplex_var.set(f"Duplex Printing: {'Yes' if printer_data['duplex'] else 'No'}")
    pages_var.set(f"Pages Printed: {page_count}")
    carbon_var.set(f"Carbon Footprint: {carbon_footprint} kg CO₂")

    # Update Cartridge and Paper Tray Info
    cartridge_info.set("\n".join([f"{color}: {level}%" for color, level in printer_data["cartridges"].items()]))
    tray_info.set("\n".join([f"{tray}: {capacity} sheets" for tray, capacity in printer_data["paperTrays"].items()]))

    # Save current report data
    current_report = {
        "pageCount": page_count,
        "carbonFootprint": carbon_footprint,
        "cartridges": printer_data["cartridges"],
        "paperTrays": printer_data["paperTrays"]
    }
    with open("current_report.json", "w") as file:
        json.dump(current_report, file)

    # Enable Save Footprints Button
    save_footprints_button.config(state=tk.NORMAL)
    graphical_output_button.config(state=tk.NORMAL)

def save_screenshot():
    """Take a screenshot of the full screen and open file manager to save it."""
    # Take a screenshot of the full screen
    screenshot = ImageGrab.grab()

    # Open file dialog to save the screenshot
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        initialfile=f"PrinterFootprints_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )
    if file_path:
        screenshot.save(file_path)
        messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {file_path}")

def open_graphical_output():
    """Open the graphical output page."""
    subprocess.Popen(["python", "printer_output.py"])

def return_to_index():
    """Return to the index page."""
    root.destroy()
    subprocess.Popen(["python", "index.py"])

# Create GUI
root = tk.Tk()
root.title("Printer Carbon Footprint Analyzer")
root.geometry("1535x813+2+42")  # Set the window size and position
root.state('zoomed')  # Maximize the window

# Load background image
bg_image = Image.open("printer.jpg")  # Ensure the image file is named 'printer.jpg' and is in the same directory
bg_image = bg_image.resize((1535, 813), Image.LANCZOS)  # Resize the image to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

# Add Return Button at Top-Right Corner
return_button = tk.Button(root, text="Return", command=return_to_index, font=("Times New Roman", 16), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.02, anchor="ne")  # Position at the top-right corner

# Left Frame for Buttons
left_frame = tk.Frame(root, bg="white")
left_frame.place(relx=0.05, rely=0.1, relwidth=0.4, relheight=0.8)

# Right Frame for Printer Data
right_frame = tk.Frame(root, bg="white")
right_frame.place(relx=0.5, rely=0.1, relwidth=0.45, relheight=0.8)

# Buttons in Left Frame
tk.Label(left_frame, text="Printer IP Address:", font=("Times New Roman", 20), bg="white").pack(pady=10)
ip_entry = tk.Entry(left_frame, width=30, font=("Times New Roman", 18))
ip_entry.pack(pady=10)
ip_entry.insert(0, DEFAULT_PRINTER_IP)  # Default value

tk.Label(left_frame, text="Select Print Type:", font=("Times New Roman", 20), bg="white").pack(pady=10)
print_type_var = tk.StringVar(value="Standard")
ttk.Combobox(left_frame, textvariable=print_type_var, values=["Standard", "High-Quality"], state="readonly", font=("Times New Roman", 18)).pack(pady=10)

fetch_button = tk.Button(left_frame, text="Fetch Printer Data", command=fetch_and_display_data, font=("Times New Roman", 20), bg="#4CAF50", fg="white")
fetch_button.pack(pady=20)

# Add Save Footprints Button
save_footprints_button = tk.Button(left_frame, text="Save Footprints", command=save_screenshot, state=tk.DISABLED, font=("Times New Roman", 20), bg="#4CAF50", fg="white")
save_footprints_button.pack(pady=20)

# Add Graphical Output Button
graphical_output_button = tk.Button(left_frame, text="Graphical Output", command=open_graphical_output, state=tk.DISABLED, font=("Times New Roman", 20), bg="#4CAF50", fg="white")
graphical_output_button.pack(pady=20)

# Printer Data in Right Frame
printer_model_var = tk.StringVar(value="Model: N/A")
manufacturer_var = tk.StringVar(value="Manufacturer: N/A")
status_var = tk.StringVar(value="Status: N/A")
connection_var = tk.StringVar(value="Connection: N/A")
mac_var = tk.StringVar(value="MAC Address: N/A")
duplex_var = tk.StringVar(value="Duplex Printing: N/A")
pages_var = tk.StringVar(value="Pages Printed: N/A")
carbon_var = tk.StringVar(value="Carbon Footprint: N/A")
cartridge_info = tk.StringVar(value="N/A")
tray_info = tk.StringVar(value="N/A")

tk.Label(right_frame, textvariable=printer_model_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=manufacturer_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=status_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=connection_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=mac_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=duplex_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=pages_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)
tk.Label(right_frame, textvariable=carbon_var, font=("Times New Roman", 18), bg="white", anchor="w").pack(fill=tk.X, pady=5)

tk.Label(right_frame, text="Cartridges Info:", font=("Times New Roman", 20), bg="white").pack(pady=10, anchor="w")
tk.Label(right_frame, textvariable=cartridge_info, font=("Times New Roman", 18), bg="white", anchor="w", justify="left").pack(fill=tk.X, pady=5)

tk.Label(right_frame, text="Paper Tray Info:", font=("Times New Roman", 20), bg="white").pack(pady=10, anchor="w")
tk.Label(right_frame, textvariable=tray_info, font=("Times New Roman", 18), bg="white", anchor="w", justify="left").pack(fill=tk.X, pady=5)

# Run Application
root.mainloop()