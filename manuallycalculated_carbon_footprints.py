import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

def calculate_carbon_footprints():
    """Calculate carbon footprints and display them next to the questions."""
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Sanil@1750",  # Replace with your MySQL password
            database="carbon_footprints_db"
        )
        cursor = connection.cursor()

        # Define emission factors for specific keywords
        emission_factors = {
            "computers": 0.051,  # kg CO2 per hour per computer
            "laptops": 0.017,    # kg CO2 per hour per laptop
            "monitors_lcd": 0.017,  # kg CO2 per hour per unit (LCD)
            "monitors_led": 0.026,  # kg CO2 per hour per unit (LED)
            "monitors_crt": 0.043,  # kg CO2 per hour per unit (CRT)
            "projectors": 0.255,  # kg CO2 per hour per unit (lower bound)
            "projectors_upper": 0.425,  # kg CO2 per hour per unit (upper bound)
            "network_switches": 0.01275,  # kg CO2 per hour per unit
            "network_servers": 0.425,  # kg CO2 per hour per server (lower bound)
            "network_servers_upper": 2.125,  # kg CO2 per hour per server (upper bound)
            "air_conditioners": 1.275,  # kg CO2 per hour per AC
            "ceiling_fans": 0.0595,  # kg CO2 per hour per fan
            "tube_lights": 0.034,  # kg CO2 per hour per unit
            "led_bulbs": 0.0085,  # kg CO2 per hour per unit
            "ups": 0.085,  # kg CO2 per hour (lower bound)
            "ups_upper": 0.85,  # kg CO2 per hour (upper bound)
            "generators": 2.5,  # kg CO2 per liter
            "electricity_grid": 0.85,  # kg CO2 per kWh
            "electricity_solar": 0,  # kg CO2 per kWh
            "water_coolers": 0.085,  # kg CO2 per hour per unit
            "cctv_cameras": 0.0085  # kg CO2 per hour per unit
        }

        total_carbon_footprint = 0

        # Loop through each question and calculate carbon footprint
        for i, entry in enumerate(entries, start=1):
            user_input = entry.get()
            question_text = questions[i - 1]
            try:
                # Convert user input to float
                user_input = float(user_input)
                carbon_footprint = 0

                if "computers" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["computers"]
                elif "laptops" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["laptops"]
                elif "monitors" in question_text.lower():
                    if "lcd" in question_text.lower():
                        carbon_footprint = user_input * emission_factors["monitors_lcd"]
                    elif "led" in question_text.lower():
                        carbon_footprint = user_input * emission_factors["monitors_led"]
                    elif "crt" in question_text.lower():
                        carbon_footprint = user_input * emission_factors["monitors_crt"]
                elif "projectors" in question_text.lower():
                    carbon_footprint = user_input * (emission_factors["projectors"] + emission_factors["projectors_upper"]) / 2
                elif "network switches" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["network_switches"]
                elif "network servers" in question_text.lower():
                    carbon_footprint = user_input * (emission_factors["network_servers"] + emission_factors["network_servers_upper"]) / 2
                elif "air conditioners" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["air_conditioners"]
                elif "ceiling fans" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["ceiling_fans"]
                elif "tube lights" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["tube_lights"]
                elif "led bulbs" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["led_bulbs"]
                elif "ups" in question_text.lower():
                    carbon_footprint = user_input * (emission_factors["ups"] + emission_factors["ups_upper"]) / 2
                elif "generators" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["generators"]
                elif "electricity" in question_text.lower():
                    if "grid" in question_text.lower():
                        carbon_footprint = user_input * emission_factors["electricity_grid"]
                    elif "solar" in question_text.lower():
                        carbon_footprint = user_input * emission_factors["electricity_solar"]
                elif "water coolers" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["water_coolers"]
                elif "cctv cameras" in question_text.lower():
                    carbon_footprint = user_input * emission_factors["cctv_cameras"]

                total_carbon_footprint += carbon_footprint

                # Display the carbon footprint next to the question
                if i <= len(carbon_footprint_labels):
                    carbon_footprint_labels[i - 1].config(text=f"{carbon_footprint:.2f} kg CO2")
            except ValueError:
                # Handle invalid or non-numeric inputs
                if i <= len(carbon_footprint_labels):
                    carbon_footprint_labels[i - 1].config(text="Invalid input")

        # Display the total carbon footprint at the bottom
        total_label.config(text=f"Total Carbon Footprint: {total_carbon_footprint:.2f} kg CO2")

        # Save the data to the database
        for i, entry in enumerate(entries, start=1):
            user_input = entry.get()
            question_text = questions[i - 1]
            carbon_footprint = carbon_footprint_labels[i - 1].cget("text")
            if carbon_footprint != "Invalid input":
                cursor.execute(
                    "INSERT INTO manual_outputs (question_number, question_text, user_input, carbon_footprint) VALUES (%s, %s, %s, %s)",
                    (i, question_text, user_input, carbon_footprint.split()[0])  # Save only the numeric value of carbon footprint
                )

        # Save the total carbon footprint to the database
        cursor.execute(
            "INSERT INTO manual_outputs (question_number, question_text, user_input, carbon_footprint) VALUES (%s, %s, %s, %s)",
            (0, "Total Carbon Footprint", "N/A", total_carbon_footprint)
        )

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Success", "Carbon footprints calculated and saved successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

def save_carbon_footprints():
    """Save user inputs to the database."""
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="Sanil@1750",  # Replace with your MySQL password
            database="carbon_footprints_db"
        )
        cursor = connection.cursor()

        # Insert each question and user input into the database
        for i, entry in enumerate(entries, start=1):
            user_input = entry.get()
            question_text = questions[i - 1]
            cursor.execute(
                "INSERT INTO manual_inputs (question_number, question_text, user_input) VALUES (%s, %s, %s)",
                (i, question_text, user_input)
            )

        connection.commit()
        cursor.close()
        connection.close()

        messagebox.showinfo("Success", "Carbon footprint data saved successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

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

# Create the main GUI window
root = tk.Tk()
root.title("Manually Calculate Carbon Footprints")
root.state('zoomed')  # Maximize the window

# Load background image
bg_image = Image.open("manual.jpg")
bg_image = bg_image.resize((1535, 813), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Create a canvas and a scrollbar
canvas = tk.Canvas(root, bg="white", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="white")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((20, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Add questions with serial numbers
questions = [
    "How many computers were used today in labs and offices? (units)",
    "How many hours were computers used today on average? (hours)",
    "How many laptops were used today? (units)",
    "How many hours were laptops used today on average? (hours)",
    "How many projectors were used today? (units)",
    "How many hours were projectors used today? (hours)",
    "How many air conditioners (ACs) were used today? (units)",
    "How many hours were air conditioners used today? (hours)",
    "How many ceiling fans were used today? (units)",
    "What was the operational duration of ceiling fans today? (hours)",
    "How many tube lights/LED bulbs were used today? (units)",
    "What were the power ratings of tube lights/LED bulbs used today? (watts)",
    "Were any UPS (Uninterruptible Power Supplies) or generators used today? If yes, what was their power rating? (watts)",
    "What was the usage time of UPS or generators today? (hours)",
    "What was the electricity source today (grid, solar, or generator)? (source)",
    "How much electricity was consumed today? (kWh)",
    "Were any water coolers or dispensers used today? If yes, how many? (units)",
    "How many hours were water coolers or dispensers used today? (hours)",
    "How many CCTV cameras were operational today? (units)",
    "What was the power rating of the CCTV cameras used today? (watts)",
    "Were any old computers, monitors, or laptops replaced today? (Yes/No)",
    "What happened to any old or non-functional electronic devices today? Were they recycled or disposed of? (disposal)",
    "Was the e-waste collection and disposal policy followed today? (Yes/No)",
    "Were batteries from UPS systems, laptops, or other devices safely disposed of or recycled today? (Yes/No)",
    "Was there any initiative today to refurbish or donate old computers instead of discarding them? (Yes/No)"
]

entries = []
carbon_footprint_labels = []

for i, question in enumerate(questions, start=1):
    label = ttk.Label(scrollable_frame, text=f"{i}. {question}", font=("Times New Roman", 16), anchor="w", justify="left", background="white")
    label.grid(row=i + 1, column=0, sticky="w", padx=10, pady=5)  # Start below the return button

    entry = ttk.Entry(scrollable_frame, width=20, font=("Times New Roman", 14))  # Reduced width
    entry.grid(row=i + 1, column=1, padx=10, pady=5)
    entries.append(entry)

    carbon_label = ttk.Label(scrollable_frame, text="", font=("Times New Roman", 14), background="white", foreground="darkgreen")  # Dark green text
    carbon_label.grid(row=i + 1, column=2, padx=10, pady=5)
    carbon_footprint_labels.append(carbon_label)

# Add Save button
save_button = tk.Button(scrollable_frame, text="Save Inputs", command=save_carbon_footprints, font=("Times New Roman", 16), bg="blue", fg="white")
save_button.grid(row=len(questions) + 2, column=0, pady=20, padx=20)

# Add Calculate button
calculate_button = tk.Button(scrollable_frame, text="Calculate Carbon Footprints\n Save Outputs", command=calculate_carbon_footprints, font=("Times New Roman", 16), bg="green", fg="white")
calculate_button.grid(row=len(questions) + 2, column=1, pady=30, padx=10)

# Add Total Carbon Footprint Label
total_label = ttk.Label(scrollable_frame, text="", font=("Times New Roman", 16), background="white", foreground="red")
total_label.grid(row=len(questions) + 3, column=0, columnspan=3, pady=20)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Add Scroll Up and Down Buttons
scroll_up_button = tk.Button(root, text="↑", command=scroll_up, font=("Times New Roman", 20), bg="green", fg="white")
scroll_up_button.place(relx=0.95, rely=0.4, anchor="center")

scroll_down_button = tk.Button(root, text="↓", command=scroll_down, font=("Times New Roman", 20), bg="green", fg="white")
scroll_down_button.place(relx=0.95, rely=0.6, anchor="center")

# Add Return Button at Top-Right Corner
return_button = tk.Button(root, text="Return", command=return_to_index, font=("Times New Roman", 16), bg="red", fg="white")
return_button.place(relx=0.95, rely=0.02, anchor="ne")

root.mainloop()
