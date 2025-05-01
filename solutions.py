import tkinter as tk
from tkinter import ttk
import subprocess  # To run index.py when returning

class CarbonFootprintSolutions:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Footprint Reduction Solutions")
        self.root.geometry("1920x1080")
        self.root.state("zoomed")  # Full-screen mode
        self.root.configure(bg="#d4edda")  # Light green background

        # Title Label
        title_label = tk.Label(
            root, text="Carbon Footprint Reduction Solutions",
            font=("Arial", 24, "bold"), bg="#155724", fg="white", pady=20
        )
        title_label.pack(fill=tk.X)

        # ✅ Return Button (Fixed Position & Size)
        self.return_button = tk.Button(
            root, text="Return", font=("Arial", 16, "bold"), bg="red", fg="white",
            padx=15, pady=5, command=self.return_to_index
        )
        self.return_button.place(relx=0.95, rely=0.02, anchor="ne")  # Top-right corner

        self.create_solution_categories()

    def create_solution_categories(self):
        categories = {
            "Energy Efficiency": [
                "Use energy-efficient computers, monitors, and LED lights.",
                "Set computers and monitors to sleep mode after inactivity.",
                "Optimize air conditioning with temperature settings and timers.",
                "Encourage natural lighting during the day.",
                "Replace old, inefficient hardware with energy-saving models."
            ],
            "Renewable Energy & Power Management": [
                "Switch to solar or hybrid power solutions.",
                "Use smart power strips to reduce phantom energy waste.",
                "Optimize UPS usage and ensure efficient power backup.",
                "Implement server virtualization to reduce running servers."
            ],
            "Sustainable IT Practices": [
                "Reduce redundant network switches and optimize router placement.",
                "Use cloud storage efficiently instead of power-consuming physical servers.",
                "Encourage energy-saving modes on all electronic devices."
            ],
            "Waste Reduction & Recycling": [
                "Donate or refurbish old computers and electronics.",
                "Implement a strict e-waste recycling policy.",
                "Ensure proper disposal of old batteries and UPS systems."
            ],
            "Workplace & Behavior Changes": [
                "Promote remote work or BYOD (Bring Your Own Device).",
                "Schedule power-off times for labs and offices.",
                "Train employees/students to adopt sustainable digital habits."
            ]
        }

        main_frame = tk.Frame(self.root, bg="#d4edda")
        main_frame.pack(fill="both", expand=True)

        # Canvas + Scrollbar
        self.canvas = tk.Canvas(main_frame, bg="#d4edda", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ttk.Frame(self.canvas)
        scrollable_frame.configure(style="Custom.TFrame")

        style = ttk.Style()
        style.configure("Custom.TFrame", background="#d4edda")

        scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((800, 0), window=scrollable_frame, anchor="n")

        for category, solutions in categories.items():
            category_label = tk.Label(
                scrollable_frame, text=category, font=("Arial", 18, "bold"),
                bg="#155724", fg="white", pady=10, padx=20
            )
            category_label.pack(fill=tk.X, padx=50, pady=10)

            for solution in solutions:
                solution_label = tk.Label(
                    scrollable_frame, text=f"✔ {solution}", font=("Arial", 14),
                    bg="#d4edda", wraplength=1400, justify="center"
                )
                solution_label.pack(fill="x", pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll Buttons
        button_frame = tk.Frame(self.root, bg="#d4edda")
        button_frame.pack(fill="x", pady=10)

        up_button = tk.Button(
            button_frame, text="▲ Scroll Up", font=("Arial", 12), bg="#155724", fg="white",
            command=self.scroll_up
        )
        up_button.pack(side="left", padx=20, pady=5)

        down_button = tk.Button(
            button_frame, text="▼ Scroll Down", font=("Arial", 12), bg="#155724", fg="white",
            command=self.scroll_down
        )
        down_button.pack(side="right", padx=20, pady=5)

    def scroll_up(self):
        self.canvas.yview_scroll(-1, "units")

    def scroll_down(self):
        self.canvas.yview_scroll(1, "units")

    def return_to_index(self):
        self.root.destroy()  # Close current window
        subprocess.run(["python", "index.py"])  # Open index.py

if __name__ == "__main__":
    root = tk.Tk()
    app = CarbonFootprintSolutions(root)
    root.mainloop()
