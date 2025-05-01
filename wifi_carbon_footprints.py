import os
import tkinter as tk
from tkinter import messagebox, filedialog
import psutil
import time
import subprocess
from PIL import Image, ImageTk, ImageGrab  # For handling the background image and screenshots
from datetime import datetime

# Configuration
POWER_CONSUMPTION_WATTS = 10  # Approx. power usage (W)
EMISSION_FACTOR = 0.8  # kg CO₂ per kWh (coal-based)
INTERFACE_NAME = "Ethernet"  # Name of the Ethernet interface

# Get the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the image file exists
image_path = os.path.join(script_dir, "background.jpg")

try:
    if os.path.exists(image_path):
        bg_image = Image.open(image_path)
    else:
        print(f"Warning: Image file '{image_path}' not found. Using a blank image instead.")
        bg_image = Image.new("RGB", (1535, 813), (255, 255, 255))  # White background
except Exception as e:
    print(f"Error loading background image: {e}")
    bg_image = Image.new("RGB", (1535, 813), (255, 255, 255))  # White background

def get_interface_uptime(interface_name):
    """Get the uptime of the specified network interface."""
    net_if_stats = psutil.net_if_stats()
    net_if_addrs = psutil.net_if_addrs()
    if interface_name in net_if_stats and interface_name in net_if_addrs:
        if net_if_stats[interface_name].isup:
            boot_time = psutil.boot_time()
            current_time = time.time()
            uptime_seconds = current_time - boot_time
            return uptime_seconds / 3600
    return 0  # Interface is down or not found

def calculate_carbon_footprint(hours):
    """Calculate carbon footprint based on uptime and power consumption."""
    energy_kwh = (POWER_CONSUMPTION_WATTS * hours) / 1000
    return energy_kwh * EMISSION_FACTOR

def calculate_footprint():
    """Calculate the carbon footprint for Ethernet."""
    uptime_hours = get_interface_uptime(INTERFACE_NAME)
    if uptime_hours == 0:
        messagebox.showerror("Error", f"{INTERFACE_NAME} is not connected or not found.")
        return

    carbon_footprint = calculate_carbon_footprint(uptime_hours)
    result_label.config(text=f"Estimated Carbon Footprint: {carbon_footprint:.2f} kg CO₂")
    save_report("Ethernet", uptime_hours, carbon_footprint)

def calculate_wifi_footprint():
    """Calculate the carbon footprint for WiFi."""
    router_ip = ip_entry.get().strip()
    if not router_ip:
        messagebox.showerror("Error", "Please enter the router IP address.")
        return

    uptime_hours = get_router_uptime(router_ip)
    if uptime_hours == 0:
        messagebox.showerror("Error", "Unable to fetch router uptime. Ensure the IP address is correct and SSH is enabled on the router.")
        return

    carbon_footprint = calculate_carbon_footprint(uptime_hours)
    result_label.config(text=f"Estimated Carbon Footprint: {carbon_footprint:.2f} kg CO₂")
    save_report("WiFi", uptime_hours, carbon_footprint)

def get_router_uptime(router_ip):
    """Fetch router uptime using SSH."""
    try:
        result = subprocess.run(["ssh", f"admin@{router_ip}", "uptime -p"], capture_output=True, text=True)
        if result.returncode == 0:
            uptime_str = result.stdout.strip()
            return extract_hours(uptime_str)
    except Exception as e:
        print("Error fetching uptime:", e)
    return 0  # Return 0 if unable to fetch uptime

def extract_hours(uptime_str):
    """Convert uptime string to hours."""
    uptime_str = uptime_str.replace("up ", "")
    days, hours = 0, 0
    for part in uptime_str.split(", "):
        if "day" in part:
            days = int(part.split()[0])
        elif "hour" in part:
            hours = int(part.split()[0])
    return days * 24 + hours

def save_report(connection_type, uptime_hours, carbon_footprint):
    """Save the carbon footprint report to a file."""
    global report_text
    report_text = f"""
    ======= Carbon Footprint Report =======
    Connection Type: {connection_type}
    Uptime: {uptime_hours:.2f} hours
    Power Consumption: {POWER_CONSUMPTION_WATTS} W
    Emission Factor: {EMISSION_FACTOR} kg CO₂ per kWh
    Estimated Carbon Footprint: {carbon_footprint:.2f} kg CO₂
    =======================================
    """
    print(report_text)  # Debugging purpose

def save_screenshot():
    """Take a screenshot of the full page and save it as WiFiFootprints."""
    try:
        # Take a screenshot of the entire screen
        screenshot = ImageGrab.grab()

        # Set default file name with date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"WiFiFootprints_{current_time}.png"

        # Open file dialog to save the screenshot
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=default_filename
        )
        if file_path:
            screenshot.save(file_path)
            messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to take screenshot: {e}")

def return_to_index():
    """Return to the index page."""
    root.destroy()
    subprocess.Popen(["python", "index.py"])

# Create GUI
root = tk.Tk()
root.title("WiFi Carbon Footprint Calculator")
root.geometry("1535x813+2+42")
root.state('zoomed')

# Resize and apply background image
bg_image = bg_image.resize((1535, 813), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Add Return Button at Top-Right Corner
return_button = tk.Button(root, text="Return", command=return_to_index, font=("Times New Roman", 16), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.02, anchor="ne")

# Center Frame for Output and Buttons
center_frame = tk.Frame(root, bg="white")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Ethernet Section
tk.Label(center_frame, text="Connect to Ethernet and click Calculate", font=("Times New Roman", 16), bg="white").pack(pady=10)
calculate_button = tk.Button(center_frame, text="Calculate Ethernet Carbon Footprint", command=calculate_footprint, font=("Times New Roman", 16), bg="#4CAF50", fg="white")
calculate_button.pack(pady=20)

# WiFi Section
tk.Label(center_frame, text="Or enter the default gateway for WiFi", font=("Times New Roman", 16), bg="white").pack(pady=10)
tk.Label(center_frame, text="(Run 'ipconfig' in CMD to find the default gateway)", font=("Times New Roman", 12), bg="white").pack(pady=5)
ip_entry = tk.Entry(center_frame, width=30, font=("Times New Roman", 14))
ip_entry.pack(pady=10)
calculate_wifi_button = tk.Button(center_frame, text="Calculate WiFi Carbon Footprint", command=calculate_wifi_footprint, font=("Times New Roman", 16), bg="#4CAF50", fg="white")
calculate_wifi_button.pack(pady=20)

# Result Label
result_label = tk.Label(center_frame, text="", font=("Times New Roman", 16), bg="white")
result_label.pack(pady=10)

# Save Footprints Button
screenshot_button = tk.Button(center_frame, text="Save Footprints", command=save_screenshot, font=("Times New Roman", 16), bg="blue", fg="white")
screenshot_button.pack(pady=20)

# Run Application
root.mainloop()