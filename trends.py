import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from sklearn.linear_model import LinearRegression
import os

class TrendsAnalysis:
    def __init__(self, root):
        self.root = root
        self.root.title("Carbon Footprint Trends Analysis")
        self.root.geometry("1920x1080")
        self.root.configure(bg="black")

        self.data = None
        self.file_path = None

        # Canvas for background image
        self.canvas = tk.Canvas(root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)

        try:
            if os.path.exists("graph.jpg"):
                bg_image = Image.open("graph.jpg").resize((1920, 1080), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
            else:
                self.canvas.create_text(960, 540, text="graph.jpg Missing", fill="gray", font=('Comic Sans MS', 30))
        except Exception as e:
            print(f"Background error: {e}")
            self.canvas.create_text(960, 540, text="Error loading background", fill="gray", font=('Comic Sans MS', 30))

        # Main Frame (centered)
        self.frame = tk.Frame(root, bg='#2E8B57', padx=30, pady=30)  # forest green
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = tk.Label(self.frame, text="Carbon Footprint Trends Analysis", bg='#2E8B57',
                                    font=('Comic Sans MS', 28, 'bold'), fg='white')
        self.title_label.pack(pady=10)

        # Upload CSV Button
        self.upload_button = tk.Button(self.frame, text="Upload CSV File", command=self.upload_file,
                                       font=('Comic Sans MS', 14, 'bold'), height=2, width=20,
                                       bg="#66BB6A", fg="white", activebackground="#4CAF50")
        self.upload_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.frame, text="", bg='#2E8B57',
                                     font=('Comic Sans MS', 12), fg="white")
        self.status_label.pack(pady=5)

        # Show Graph Button
        self.graph_button = tk.Button(self.frame, text="Show Graph", command=self.show_graph,
                                      font=('Comic Sans MS', 14, 'bold'), height=2, width=20,
                                      bg="#42A5F5", fg="white", activebackground="#1E88E5")
        self.graph_button.pack(pady=10)
        self.graph_button.config(state="disabled")

        # Conclusion
        self.conclusion_label = tk.Label(self.frame, text="", bg='#2E8B57', font=('Comic Sans MS', 16, 'bold'))
        self.conclusion_label.pack(pady=10)

        # Return Button (top right)
        self.return_button = tk.Button(
            self.root,
            text="Return",
            command=self.return_to_index,
            bg="red",
            fg="white",
            font=('Comic Sans MS', 14, 'bold'),
            borderwidth=3,
            relief="raised",
            activebackground="#ff4d4d"
        )
        self.return_button.place(x=self.root.winfo_screenwidth() - 120, y=20, width=100, height=50)
        
                # General Solutions Button (below Return)
        self.solution_button = tk.Button(
            self.root,
            text="General Solutions",
            command=self.open_solutions,
            bg="orange",
            fg="white",
            font=('Comic Sans MS', 14, 'bold'),
            borderwidth=3,
            relief="raised",
            activebackground="#FFA500"
        )
        self.solution_button.place(x=self.root.winfo_screenwidth() - 200, y=80, width=180, height=50)


    def upload_file(self):
        self.upload_button.config(state="disabled")
        self.graph_button.config(state="disabled")
        self.status_label.config(text="Loading CSV file...", fg="yellow")
        self.file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not self.file_path:
            messagebox.showinfo("Cancelled", "No file selected.")
            self.upload_button.config(state="normal")
            self.status_label.config(text="")
            return

        try:
            self.data = pd.read_csv(self.file_path)
            self.data['entry_date'] = pd.to_datetime(self.data['entry_date'], format='%d-%m-%Y', dayfirst=True)
            self.data.sort_values(by='entry_date', inplace=True)

            self.status_label.config(text="CSV loaded successfully!", fg="lightgreen")
            self.graph_button.config(state="normal")
            self.analyze_trends()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process CSV: {str(e)}")
        finally:
            self.upload_button.config(state="normal")

    def analyze_trends(self):
        if 'Total_Carbon_Footprint_kgCO2' not in self.data.columns:
            messagebox.showerror("Error", "Missing column: 'Total_Carbon_Footprint_kgCO2'")
            return

        # Add monthly grouping summary
        monthly_summary = self.data.groupby(self.data['entry_date'].dt.to_period('M'))['Total_Carbon_Footprint_kgCO2'].sum().reset_index()
        months_loaded = monthly_summary['entry_date'].dt.strftime('%B %Y').tolist()
        months_text = "Months Loaded: " + ", ".join(months_loaded)
        self.status_label.config(text=months_text, fg="lightblue")

        X = self.data['entry_date'].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
        y = self.data['Total_Carbon_Footprint_kgCO2'].values

        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]

        if slope > 0:
            trend_text = "Trend: Increasing Carbon Footprint - Attention Needed"
            color = "red"
        else:
            trend_text = "Trend: Decreasing Carbon Footprint - Good Progress"
            color = "black"

        self.conclusion_label.config(text=trend_text, fg=color)

    def show_graph(self):
        if self.data is None:
            messagebox.showerror("Error", "Please upload a CSV file first.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(self.data['entry_date'], self.data['Total_Carbon_Footprint_kgCO2'],
                 marker='o', linestyle='-', color='blue', label='Carbon Footprint')

        X = self.data['entry_date'].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
        y = self.data['Total_Carbon_Footprint_kgCO2'].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        plt.plot(self.data['entry_date'], y_pred, color='orange', linestyle='--', label='Trend Line (Linear Regression)')

        plt.xlabel("Date")
        plt.ylabel("Carbon Footprint (kgCO2)")
        plt.title("Carbon Footprint Trend Analysis")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def return_to_index(self):
        self.root.destroy()
        os.system("python index.py")
     
    def open_solutions(self):
        self.root.destroy()
        os.system("python solutions.py")
        
               


if __name__ == "__main__":
    root = tk.Tk()
    app = TrendsAnalysis(root)
    root.mainloop()
