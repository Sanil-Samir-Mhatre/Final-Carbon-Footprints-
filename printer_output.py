import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

def load_current_report():
    """Load the current report data from a JSON file."""
    with open("current_report.json", "r") as file:
        return json.load(file)

def return_to_main():
    """Close the current window."""
    root.destroy()

def show_current_report():
    """Generate and display the current report using matplotlib."""
    report = load_current_report()
    
    # Create figure with appropriate spacing
    fig, axes = plt.subplots(3, 1, figsize=(8, 10))
    fig.suptitle("Printer Carbon Footprint Report", fontsize=18, fontweight='bold', y=0.98)
    
    # Pages Printed vs Carbon Footprint
    categories = ['Pages Printed', 'Carbon Footprint']
    values = [report['pageCount'], report['carbonFootprint']]
    axes[0].bar(categories, values, color=['blue', 'green'])
    axes[0].set_ylabel("Values", fontsize=12)
    axes[0].set_title("Pages Printed vs Carbon Footprint", fontsize=14)
    axes[0].grid(axis='y', linestyle='--', alpha=0.7)

    # Cartridge Levels
    cartridge_levels = [report['cartridges'][color] for color in report['cartridges']]
    colors = ['black', 'cyan', 'magenta', 'yellow']
    axes[1].bar(colors, cartridge_levels, color=colors)
    axes[1].set_ylabel("Level (%)", fontsize=12)
    axes[1].set_title("Cartridge Levels", fontsize=14)
    axes[1].grid(axis='y', linestyle='--', alpha=0.7)

    # Paper Tray Info
    tray_labels = list(report['paperTrays'].keys())
    tray_values = list(report['paperTrays'].values())
    axes[2].bar(tray_labels, tray_values, color='orange')
    axes[2].set_ylabel("Sheets", fontsize=12)
    axes[2].set_title("Paper Tray Capacities", fontsize=14)
    axes[2].grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust layout to prevent overlap
    plt.subplots_adjust(top=0.90, hspace=0.5)
    
    # Display the figure in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=10)
    canvas.draw()

    # Display the carbon footprint in kg CO₂
    carbon_footprint_label = tk.Label(
        root,
        text=f"Total Carbon Footprint: {report['carbonFootprint']} kg CO₂",
        font=("Arial", 16),
        bg="white",
        fg="black"
    )
    carbon_footprint_label.pack(pady=10)

import datetime
from PIL import ImageGrab
from tkinter import filedialog, messagebox

# Create GUI
root = tk.Tk()
root.title("Printer Carbon Footprint Report")
root.geometry("1535x813+2+42")  # Set the window size and position
root.state('zoomed')  # Maximize the window

def save_screenshot():
    """Take a screenshot of the full screen and open file manager to save it."""
    screenshot = ImageGrab.grab()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        initialfile=f"PrinterGraphicalOutput_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )
    if file_path:
        screenshot.save(file_path)
        messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {file_path}")

# Add Return Button
return_button = tk.Button(root, text="Return", command=return_to_main, font=("Arial", 14), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.02, anchor="ne")  # Position at the top-right corner

# Add Save Footprints Button
save_footprints_button = tk.Button(root, text="Save Footprints", command=save_screenshot, font=("Arial", 14), bg="#4CAF50", fg="white")
save_footprints_button.place(relx=0.8, rely=0.02, anchor="ne")  # Position near the Return button

# Show the report immediately
show_current_report()

# Run Application
root.mainloop()
