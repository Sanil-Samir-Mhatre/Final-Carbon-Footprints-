import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk

# Global variables
csv_file_path = ""
custom_threshold = 125  # Default threshold value

def upload_file():
    """Allow the user to upload a CSV file"""
    global csv_file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        csv_file_path = file_path
        file_label.config(text=f"Uploaded: {os.path.basename(file_path)}", fg="blue")  # Show file name
        messagebox.showinfo("File Uploaded", "CSV file uploaded successfully!")
        conclude_button.config(state=tk.NORMAL)  # Enable the Conclude button

def clean_csv(file_path):
    """Automatically clean and fix CSV formatting issues"""
    try:
        df = pd.read_csv(file_path)

        # Detect format: (1) Date-based or (2) Month-based
        if 'entry_date' in df.columns and 'Total_Carbon_Footprint_kgCO2' in df.columns:
            df = df[['entry_date', 'Total_Carbon_Footprint_kgCO2']]  # Keep only valid columns
            df.rename(columns={'Total_Carbon_Footprint_kgCO2': 'Carbon_Footprint'}, inplace=True)
        else:
            raise ValueError("Invalid CSV format! Must have 'entry_date' and 'Total_Carbon_Footprint_kgCO2'.\nConsider changing the column titles accordingly.")

        # Save cleaned file
        df.to_csv(file_path, index=False)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clean CSV: {e}")
        return None

def conclude():
    """Analyze the uploaded CSV and provide a threshold-based conclusion."""
    global csv_file_path, custom_threshold
    
    if not csv_file_path:
        messagebox.showwarning("No File", "Please upload a CSV file first.")
        return

    # Get user-defined threshold
    try:
        custom_threshold = float(threshold_entry.get())
        if custom_threshold <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive number for the threshold.")
        return

    # Clean CSV before processing
    df = clean_csv(csv_file_path)
    if df is None:
        return  # Stop if cleaning failed

    # Convert date column to datetime format
    try:
        df['entry_date'] = pd.to_datetime(df['entry_date'], errors='coerce')
    except Exception as e:
        messagebox.showerror("Date Error", f"Invalid date format: {e}")
        return

    # Sort data by entry_date
    df = df.sort_values(by='entry_date')

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(df['entry_date'], df['Carbon_Footprint'], marker='o', linestyle='-', color='b', label='Carbon Footprint')
    plt.axhline(y=custom_threshold, color='r', linestyle='--', label=f'{custom_threshold} kg Threshold')  # Custom Threshold Line

    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Carbon Footprint (kg)", fontsize=12)
    plt.title("Carbon Footprint Trend Over Time", fontsize=14)
    plt.legend(fontsize=10)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Determine conclusion based on threshold
    if df['Carbon_Footprint'].max() > custom_threshold:
        conclusion_text = f"⚠️ ALERT: Your carbon footprint has exceeded the {custom_threshold} kg threshold.\nConsider reducing your emissions."
        conclusion_color = "red"
    else:
        conclusion_text = f"✅ Your carbon footprint is within safe limits ({custom_threshold} kg).\nKeep up the good work!"
        conclusion_color = "green"

    # Custom conclusion message box
    conclusion_window = tk.Toplevel(root)
    conclusion_window.title("Conclusion Statement")
    conclusion_window.geometry("600x300")
    conclusion_window.configure(bg="#f4f4f4")

    label = tk.Label(conclusion_window, text=conclusion_text, font=("Arial", 16, "bold"), fg=conclusion_color, bg="#f4f4f4", wraplength=550, justify="center")
    label.pack(pady=40)

    ok_button = tk.Button(conclusion_window, text="OK", font=("Arial", 14), bg="green", fg="white", command=conclusion_window.destroy)
    ok_button.pack(pady=10)

    # Show the graph
    plt.show()

def open_solutions():
    """Close this window and open solutions.py"""
    root.destroy()
    os.system('python solutions.py')

def return_to_index():
    """Close this window and open index.py"""
    root.destroy()
    os.system('python index.py')

# Create GUI
root = tk.Tk()
root.title("Conclusion")
root.geometry("1920x1080")
root.state('zoomed')  # Maximize window

# Load and display background image
try:
    bg_image = Image.open("bgimg.jpg")  # Load the background image
    bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)  # Resize to match the window
    bg_img = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    messagebox.showerror("Image Error", f"Failed to load background image: {e}")

# Return Button (Top Right)
return_button = tk.Button(root, text="Return", command=return_to_index, 
                          font=("Arial", 14, "bold"), bg="red", fg="white", width=10, height=2)
return_button.place(relx=0.95, rely=0.02, anchor="ne")  # Position at top right corner

# Center Frame for Buttons (Stylish)
frame = tk.Frame(root, bg="white", bd=5, relief="solid")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(frame, text="Carbon Footprint Analysis", font=("Comic Sans MS", 24, "bold"), bg="white", fg="#4CAF50")
title_label.pack(pady=10)

# Upload Button
upload_button = tk.Button(frame, text="Upload Carbon Footprints Data", command=upload_file, 
                          font=("Comic Sans MS", 20), bg="#4CAF50", fg="white", width=30)
upload_button.pack(pady=20)

# Label to Show Uploaded File Name
file_label = tk.Label(frame, text="", font=("Arial", 14), bg="white", fg="blue")
file_label.pack()

# Threshold Input
threshold_label = tk.Label(frame, text="Enter Custom Threshold (kg):", font=("Arial", 16), bg="white", fg="black")
threshold_label.pack(pady=10)

threshold_entry = tk.Entry(frame, font=("Arial", 16), width=10, justify="center")
threshold_entry.insert(0, str(custom_threshold))  # Default value
threshold_entry.pack(pady=5)

# Conclude Button (Initially Disabled)
conclude_button = tk.Button(frame, text="Conclude", command=conclude, 
                            font=("Comic Sans MS", 20), bg="#4CAF50", fg="white", width=20, state=tk.DISABLED)
conclude_button.pack(pady=20)

# Solutions Button
solutions_button = tk.Button(frame, text="Solutions", command=open_solutions, 
                             font=("Comic Sans MS", 20), bg="#4CAF50", fg="white", width=20)
solutions_button.pack(pady=20)

# Run Application
root.mainloop()
