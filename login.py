import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import mysql.connector

def open_index():
    root.destroy()
    os.system('python index.py')

def return_to_start():
    root.destroy()
    import start

def login():
    """Handle the login process."""
    role = role_var.get().strip()  # Getting the selected role from the dropdown
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    user_id = age_entry.get().strip()

    if not role or not username or not password or not user_id:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    try:
        user_id = int(user_id)
    except ValueError:
        messagebox.showerror("Error", "ID must be a number.")
        return

    # Save user details to the MySQL database
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sanil@1750",
            database="carbon_footprints_db"
        )
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (role, username, password, user_id) VALUES (%s, %s, %s, %s)",
            (role, username, password, user_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success", "Login details saved successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return

    open_index()

# GUI Code
root = tk.Tk()
root.title("Login")
root.geometry("1535x813+2+42")
root.state('zoomed')

bg_image = Image.open("background2.jpg")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

return_button = tk.Button(root, text="Return", command=return_to_start, font=("Comic Sans MS", 16), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.05, anchor="ne")

login_frame = tk.Frame(root)
login_frame.pack(pady=20)

tk.Label(login_frame, text="Role:", font=("Comic Sans MS", 20)).pack(pady=10)

# Create a dropdown menu for roles
role_var = tk.StringVar()
role_options = ["Admin"]
role_menu = tk.OptionMenu(login_frame, role_var, *role_options)
role_menu.config(width=28, font=("Comic Sans MS", 20))
role_menu.pack(pady=20)

tk.Label(login_frame, text="Username:", font=("Comic Sans MS", 20)).pack(pady=10)
username_entry = tk.Entry(login_frame, width=30, font=("Comic Sans MS", 18))
username_entry.pack(pady=10)

tk.Label(login_frame, text="Password:", font=("Comic Sans MS", 20)).pack(pady=10)
password_entry = tk.Entry(login_frame, width=30, show="*", font=("Comic Sans MS", 18))
password_entry.pack(pady=10)

tk.Label(login_frame, text="ID:", font=("Comic Sans MS", 20)).pack(pady=10)
age_entry = tk.Entry(login_frame, width=30, font=("Comic Sans MS", 18))
age_entry.pack(pady=10)

login_button = tk.Button(login_frame, text="Start Calculating Carbon Footprints", command=login, font=("Comic Sans MS", 20), bg="green", fg="white")
login_button.pack(pady=20)

root.mainloop()
