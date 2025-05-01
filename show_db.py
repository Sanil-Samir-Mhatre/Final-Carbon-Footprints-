import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mysql.connector
from datetime import datetime
import os
import csv

def open_csvfile():
    """Open csvfile.py for analysis and prediction."""
    os.system('python csvfile.py')

def fetch_data():
    """Fetch all tables and their data from the database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sanil@1750",
            database="carbon_footprints_db"
        )
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            table_label = tk.Label(scrollable_frame, text=f"Table: {table_name}", font=("Comic Sans MS", 18, "bold"), bg="#e8f5e9", fg="black", anchor="w")
            table_label.pack(pady=10, padx=20, anchor="w")
            tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", style="Custom.Treeview")
            for col in columns:
                tree.heading(col, text=col, anchor="center")
                tree.column(col, width=200, anchor="center")
            for row in rows:
                tree.insert("", "end", values=row)
            tree.pack(pady=10, padx=20, anchor="w")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        error_label = tk.Label(scrollable_frame, text=f"Error: {err}", font=("Comic Sans MS", 14), fg="red", bg="#e8f5e9")
        error_label.pack(pady=10)

def delete_data():
    """Delete all data from the database with a confirmation popup."""
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete all data from the database?")
    if confirm:
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sanil@1750",
                database="carbon_footprints_db"
            )
            cursor = connection.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Temporarily disable foreign key checks
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            for table in tables:
                cursor.execute(f"DELETE FROM {table[0]};")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Re-enable foreign key checks
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "All data has been deleted from the database.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

def download_report():
    """Save data from specific tables to a CSV file with a timestamped filename."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sanil@1750",
            database="carbon_footprints_db"
        )
        cursor = connection.cursor()

        # Specify the tables to export (only 'manual_inputs' and 'manual_outputs')
        tables_to_export = ["manual_inputs", "manual_outputs"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"CarbonFootprintsReport_{timestamp}.csv"

        # Open a file dialog to choose the save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=filename
        )
        if not file_path:
            return  # User canceled the save dialog

        with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            for table in tables_to_export:
                cursor.execute(f"SELECT * FROM {table};")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

                # Write table name as a header
                csv_writer.writerow([f"Table: {table}"])
                # Write column headers
                csv_writer.writerow(columns)
                # Write rows
                csv_writer.writerows(rows)
                # Add a blank line between tables
                csv_writer.writerow([])

        cursor.close()
        connection.close()
        messagebox.showinfo("Success", f"Report saved successfully as {file_path}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def scroll_up():
    """Scroll up the canvas."""
    canvas.yview_scroll(-1, "units")

def scroll_down():
    """Scroll down the canvas."""
    canvas.yview_scroll(1, "units")

def return_to_index():
    """Return to the index page."""
    root.destroy()
    os.system('python index.py')

root = tk.Tk()
root.title("Carbon Footprints Database Viewer")
root.geometry("1535x813+2+42")
root.state('zoomed')
root.configure(bg="#e8f5e9")
canvas = tk.Canvas(root, bg="#e8f5e9", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#e8f5e9")
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
style = ttk.Style()
style.configure("Custom.Treeview", font=("Comic Sans MS", 14), rowheight=40, background="#ffffff", fieldbackground="#ffffff")
style.configure("Custom.Treeview.Heading", font=("Comic Sans MS", 16, "bold"), background="#a5d6a7", foreground="black")
return_button = tk.Button(root, text="Return", command=return_to_index, font=("Comic Sans MS", 16), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.02, anchor="ne")
current_date_label = tk.Label(root, text=f"Date: {datetime.now().strftime('%d %B, %Y %H:%M:%S')}", font=("Comic Sans MS", 14), bg="#e8f5e9", fg="black")
current_date_label.place(relx=0.95, rely=0.08, anchor="ne")
nav_frame = tk.Frame(root, bg="#e8f5e9")
nav_frame.pack(side="bottom", fill="x")
save_footprints_button = tk.Button(nav_frame, text="Save Total Footprints for Analysis and Prediction", command=open_csvfile, font=("Comic Sans MS", 16), bg="purple", fg="white")
save_footprints_button.pack(side="top", pady=10)
scroll_up_button = tk.Button(nav_frame, text="↑ Scroll Up", command=scroll_up, font=("Comic Sans MS", 16), bg="green", fg="white")
scroll_up_button.pack(side="top", pady=10)
scroll_down_button = tk.Button(nav_frame, text="↓ Scroll Down", command=scroll_down, font=("Comic Sans MS", 16), bg="green", fg="white")
scroll_down_button.pack(side="top", pady=10)
download_button = tk.Button(nav_frame, text="Download Report", command=download_report, font=("Comic Sans MS", 16), bg="blue", fg="white")
download_button.pack(side="top", pady=10)
delete_button = tk.Button(nav_frame, text="Delete Database", command=delete_data, font=("Comic Sans MS", 16), bg="red", fg="white")
delete_button.pack(side="top", pady=10)
fetch_data()
root.mainloop()