import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import mysql.connector
import csv
import re
from datetime import datetime
import os

# Database Connection Function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sanil@1750",
        database="carbon_footprints_db"
    )

# Function to validate date format (DD-MM-YYYY)
def validate_date_format(date_text):
    pattern = r"^\d{2}-\d{2}-\d{4}$"
    if not re.match(pattern, date_text):
        return False
    try:
        datetime.strptime(date_text, "%d-%m-%Y")
        return True
    except ValueError:
        return False

# Function to insert data into MySQL
def insert_data():
    date = entry_date.get().strip()
    footprint = entry_footprint.get().strip()

    if not date or not footprint:
        messagebox.showerror("Input Error", "Both fields are required!")
        return

    if not validate_date_format(date):
        messagebox.showerror("Input Error", "Invalid date format! Use DD-MM-YYYY.")
        return

    try:
        formatted_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        footprint = float(footprint)
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO carbon_footprints (entry_date, total_carbon_footprint_kgCO2) VALUES (%s, %s) "
            "ON DUPLICATE KEY UPDATE total_carbon_footprint_kgCO2 = VALUES(total_carbon_footprint_kgCO2)",
            (formatted_date, footprint),
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data inserted successfully!")
        fetch_data()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Function to fetch data
def fetch_data():
    for row in tree.get_children():
        tree.delete(row)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT entry_date, total_carbon_footprint_kgCO2 FROM carbon_footprints ORDER BY entry_date")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            formatted_date = datetime.strptime(str(row[0]), "%Y-%m-%d").strftime("%d-%m-%Y")
            tree.insert("", "end", values=(formatted_date, row[1]))
    except Exception as e:
        messagebox.showerror("Fetch Error", str(e))

# Function to export data to CSV
def export_to_csv():
    try:
        # Generate a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"CarbonFootprintsData_{timestamp}.csv"

        # Open a file dialog to choose the save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=default_filename
        )
        if not file_path:
            return  # User canceled the save dialog

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT entry_date, total_carbon_footprint_kgCO2 FROM carbon_footprints ORDER BY entry_date")
        rows = cursor.fetchall()
        conn.close()

        with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["entry_date", "Total_Carbon_Footprint_kgCO2"])  # Write headers
            for row in rows:
                formatted_date = datetime.strptime(str(row[0]), "%Y-%m-%d").strftime("%d-%m-%Y")
                csv_writer.writerow([formatted_date, row[1]])  # Write rows

        messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))

# Function to delete all data
def delete_all_data():
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete all data?")
    if confirm:
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM carbon_footprints")
            conn.commit()
            conn.close()
            fetch_data()
            messagebox.showinfo("Success", "All data deleted successfully!")
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))

# Function to return to the main page
def return_to_main():
    root.destroy()  # Close the current window

# GUI Setup
root = tk.Tk()
root.title("Carbon Footprint Tracker")
root.geometry("1920x1080")
root.configure(bg="#4CAF50")

# Return Button
return_button = tk.Button(root, text="Return", command=return_to_main, bg="red", fg="white", 
                          font=("Comic Sans MS", 14, "bold"), width=8, height=1)
return_button.place(relx=0.92, rely=0.02)

# Main Layout Frame
main_frame = tk.Frame(root, bg="white", bd=2)
main_frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.10)

# Table Frame
table_frame = tk.Frame(main_frame, bg="white")
table_frame.place(relx=0.05, rely=0.1, relwidth=0.6, relheight=0.85)

# Define columns with correct headings
columns = ("entry_date", "Total_Carbon_Footprint_kgCO2")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")

# Set column headings
for col in columns:
    tree.heading(col, text=col)  # Use the column names as headings
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)

# Input & Buttons Frame
button_frame = tk.Frame(main_frame, bg="white")
button_frame.place(relx=0.7, rely=0.1, relwidth=0.25, relheight=0.85)

tk.Label(button_frame, text="Date (DD-MM-YYYY):", bg="white", font=("Comic Sans MS", 12)).pack(pady=10)
entry_date = tk.Entry(button_frame, font=("Comic Sans MS", 12))
entry_date.pack(pady=5)

tk.Label(button_frame, text="Carbon Footprint (kgCO2):", bg="white", font=("Comic Sans MS", 12)).pack(pady=10)
entry_footprint = tk.Entry(button_frame, font=("Comic Sans MS", 12))
entry_footprint.pack(pady=5)

tk.Button(button_frame, text="Submit Data", command=insert_data, bg="#5CA45C", fg="white", 
          font=("Comic Sans MS", 12), width=20).pack(pady=10)

tk.Button(button_frame, text="Export as CSV", command=export_to_csv, bg="#5C85A4", fg="white", 
          font=("Comic Sans MS", 12), width=20).pack(pady=10)

tk.Button(button_frame, text="Delete All Data", command=delete_all_data, bg="#A45C5C", fg="white", 
          font=("Comic Sans MS", 12), width=20).pack(pady=10)

# Fetch data initially
fetch_data()

root.mainloop()