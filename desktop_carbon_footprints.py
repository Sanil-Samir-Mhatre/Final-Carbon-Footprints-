import tkinter as tk
from tkinter import Toplevel, messagebox, filedialog
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import timedelta, datetime
import time
import threading
import subprocess
from PIL import Image, ImageTk, ImageGrab

# Global data storage
cpu_data = []
ram_data = []
timestamps = []
boot_time = psutil.boot_time()
is_running = {"cpu": True, "ram": True}
CARBON_CONVERSION_FACTOR = 0.82  # kg CO₂ per kWh
CPU_POWER_WATTS = 65
RAM_POWER_WATTS = 4

# System uptime
def calculate_uptime():
    return str(timedelta(seconds=int(time.time() - boot_time)))

# CPU usage update
def update_cpu_data():
    while True:
        try:
            if is_running["cpu"]:
                cpu_usage = psutil.cpu_percent(interval=None)  # Non-blocking call
                cpu_data.append(cpu_usage)
                timestamps.append(time.time() - boot_time)
            time.sleep(1)
        except Exception as e:
            print(f"Error in update_cpu_data thread: {e}")
            time.sleep(1)

# RAM usage update
def update_ram_data():
    while True:
        try:
            if is_running["ram"]:
                ram = psutil.virtual_memory()
                ram_data.append(ram.percent)
            time.sleep(1)
        except Exception as e:
            print(f"Error in update_ram_data thread: {e}")
            time.sleep(1)

# Live graph popup with screenshot button
def create_live_graph(title, data_fetcher, ylabel, data_key):
    popup = Toplevel()
    popup.title(title)
    popup.configure(bg="#e0f7e9")
    popup.geometry("960x540+100+100")  # Fixed position

    figure, ax = plt.subplots(figsize=(8, 4))
    canvas = FigureCanvasTkAgg(figure, master=popup)
    canvas.get_tk_widget().pack()

    control_frame = tk.Frame(popup, bg="#e0f7e9")
    control_frame.pack(pady=10)

    def start_graph():
        is_running[data_key] = True

    def stop_graph():
        is_running[data_key] = False

    tk.Button(control_frame, text="Start", command=start_graph, bg="green", fg="white", font=("Comic Sans MS", 10)).pack(side="left", padx=10)
    tk.Button(control_frame, text="Stop", command=stop_graph, bg="red", fg="white", font=("Comic Sans MS", 10)).pack(side="left", padx=10)

    smoothing_label = tk.Label(control_frame, text="Smoothing:", bg="#e0f7e9", font=("Comic Sans MS", 10))
    smoothing_label.pack(side="left", padx=10)
    smoothing_scale = tk.Scale(control_frame, from_=1, to=10, orient="horizontal", font=("Comic Sans MS", 8))
    smoothing_scale.pack(side="left", padx=10)

    def update_graph():
        if is_running[data_key]:
            ax.clear()
            ax.set_title(title)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel(ylabel)

            data = data_fetcher()
            smoothing_factor = smoothing_scale.get()
            if data:
                smoothed_data = [sum(data[max(0, i - smoothing_factor):i + 1]) / (i - max(0, i - smoothing_factor) + 1) for i in range(len(data))]
                ax.plot(range(len(smoothed_data)), smoothed_data, marker="o", markersize=4, color="blue")

            canvas.draw()
        popup.after(1000, update_graph)

    # Add Save Footprints button to popup
    def save_screenshot():
        # Take a screenshot of the popup window
        popup.update_idletasks()  # Ensure the window is fully rendered
        x = popup.winfo_rootx()
        y = popup.winfo_rooty()
        w = popup.winfo_width()
        h = popup.winfo_height()
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))

        # Set default file name based on the page with date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"CPUFootprints_{current_time}" if "CPU" in title else f"RAMFootprints_{current_time}"

        # Open file dialog to save the screenshot
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            initialfile=f"{default_filename}.png"
        )
        if file_path:
            screenshot.save(file_path)
            messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {file_path}")

    save_button = tk.Button(popup, text="Save Footprints", command=save_screenshot, bg="#4CAF50", fg="white", font=("Comic Sans MS", 10))
    save_button.pack(pady=5)

    update_graph()

# Data fetchers
def fetch_live_cpu_data():
    return cpu_data[-60:] if len(cpu_data) > 60 else cpu_data

def fetch_live_ram_data():
    return ram_data[-60:] if len(ram_data) > 60 else ram_data

# Carbon calculation
def calculate_carbon_footprint():
    uptime_seconds = time.time() - boot_time
    uptime_hours = uptime_seconds / 3600

    cpu_energy_kwh = (CPU_POWER_WATTS * uptime_hours) / 1000
    ram_energy_kwh = (RAM_POWER_WATTS * uptime_hours) / 1000
    total_energy_kwh = cpu_energy_kwh + ram_energy_kwh
    carbon_footprint = total_energy_kwh * CARBON_CONVERSION_FACTOR

    result = (
        f"System Uptime: {uptime_hours:.2f} hours\n"
        f"Carbon Footprint: {carbon_footprint:.2f} kg CO₂\n"
    )
    return result

# Return to index
def return_to_index(root):
    root.destroy()
    subprocess.Popen(["python", "index.py"])

# Main UI
def main():
    root = tk.Tk()
    root.title("System Monitor")
    root.geometry("1920x1080")

    # Load and set background image
    bg_image = Image.open("photu.jpg")
    bg_photo = ImageTk.PhotoImage(bg_image.resize((1920, 1080)))
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    default_font = ("Comic Sans MS", 11)

    top_frame = tk.Frame(root, bg="#d9fdd3")
    top_frame.pack(fill="x", pady=5)
    tk.Button(top_frame, text="Return", command=lambda: return_to_index(root),
              bg="crimson", fg="white", font=default_font).pack(side="right", padx=20)

    main_frame = tk.Frame(root, bg="#ffffff", bd=5)
    main_frame.place(relx=0.5, rely=0.1, anchor="n")

    tk.Label(main_frame, text="System Monitor Dashboard", font=("Comic Sans MS", 18, "bold")).pack(pady=10)

    tk.Button(main_frame, text="CPU Usage", command=lambda: create_live_graph("CPU Usage", fetch_live_cpu_data, "CPU Usage (%)", "cpu"),
              font=default_font).pack(pady=5)

    tk.Button(main_frame, text="RAM Usage", command=lambda: create_live_graph("RAM Usage", fetch_live_ram_data, "RAM Usage (%)", "ram"),
              font=default_font).pack(pady=5)

    carbon_result_label = tk.Label(root, text="", font=default_font)
    carbon_result_label.place(relx=0.5, rely=0.7, anchor="center")

    def update_carbon_label():
        result = calculate_carbon_footprint()
        carbon_result_label.config(text=result)

    tk.Button(main_frame, text="Calculate Carbon Footprint", command=update_carbon_label,
              bg="blue", fg="white", font=default_font).pack(pady=10)

    # Add Save Footprints button below Calculate Carbon Footprint
    def save_screenshot():
        # Take a screenshot of the entire screen
        root.update_idletasks()  # Ensure the window is fully rendered
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        w = root.winfo_width()
        h = root.winfo_height()
        screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))

        # Set default file name with date and time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"DesktopFootprints_{current_time}"

        # Open file dialog to save the screenshot
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")], initialfile=f"{default_filename}.png")
        if file_path:
            screenshot.save(file_path)
            messagebox.showinfo("Screenshot Saved", f"Screenshot saved as {file_path}")

    tk.Button(main_frame, text="Save Footprints", command=save_screenshot,
              bg="#4CAF50", fg="white", font=default_font).pack(pady=10)

    runtime_label = tk.Label(root, text="", font=default_font)
    runtime_label.place(relx=0.5, rely=0.8, anchor="center")

    def update_runtime_label():
        runtime_label.config(text=f"System Uptime: {calculate_uptime()}")
        runtime_label.after(1000, update_runtime_label)

    update_runtime_label()

    threads = [
        threading.Thread(target=update_cpu_data, daemon=True),
        threading.Thread(target=update_ram_data, daemon=True),
    ]
    for t in threads:
        t.start()

    root.mainloop()

if __name__ == "__main__":
    main()