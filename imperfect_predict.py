import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os

class AIMLDataAnalysis:
    def __init__(self, root):  # <-- FIXED: proper constructor
        self.root = root
        self.root.title("AIML Data Analysis")
        self.root.geometry("1920x1080")  
        self.root.state('zoomed')  

        # Load background image
        self.canvas = tk.Canvas(root, width=1920, height=1080)
        self.canvas.pack(fill="both", expand=True)

        background_image = Image.open("data.png")  
        background_image = background_image.resize((1920, 1080), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(background_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        # Create main frame
        self.frame = tk.Frame(root, bg='grey', padx=30, pady=30)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        self.title_label = tk.Label(self.frame, text="AIML Data Analysis", bg='grey',
                                    font=('Times New Roman', 40, 'bold'), fg='white')
        self.title_label.pack(pady=20)

        # Upload button
        self.upload_button = tk.Button(self.frame, text="Upload CSV File", command=self.upload_csv,
                                       font=('Helvetica', 14), height=2, width=20,
                                       bg="#4CAF50", fg="white")
        self.upload_button.pack(pady=10)

        # Label to show uploaded file name
        self.file_name_label = tk.Label(self.frame, text="No file selected", bg='grey',
                                        font=('Helvetica', 16, 'bold'))
        self.file_name_label.pack(pady=10)

        # Predict button
        self.predict_button = tk.Button(self.frame, text="Predict", command=self.run_prediction,
                                        font=('Helvetica', 14), height=2, width=15,
                                        bg="#2196F3", fg="white")
        self.predict_button.pack(pady=20)

        # Return button
        self.return_button = tk.Button(root, text="Return", command=self.return_to_previous,
                                       fg="white", bg="red", font=('Helvetica', 14),
                                       height=2, width=10)
        self.return_button.place(x=root.winfo_screenwidth() - 180, y=20)

        self.data = None  

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            messagebox.showwarning("File Upload", "No file selected.")
            return

        try:
            self.data = pd.read_csv(file_path)
            self.file_name_label.config(text=f"Uploaded File: {os.path.basename(file_path)}")
            messagebox.showinfo("Success", "CSV file uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the CSV file: {str(e)}")

    def run_prediction(self):
        if self.data is None:
            messagebox.showerror("Error", "No CSV file uploaded!")
            return
        
        try:
            results = self.predict_with_linear_regression(self.data)
            self.display_results(*results)
        except Exception as e:
            messagebox.showerror("Prediction Error", f"An error occurred: {str(e)}")

    def predict_with_linear_regression(self, data):
        if 'entry_date' not in data.columns or 'Total_Carbon_Footprint_kgCO2' not in data.columns:
            raise ValueError("CSV must have 'entry_date' and 'Total_Carbon_Footprint_kgCO2' columns. "
                             "Consider changing the column titles.")

        data['entry_date'] = pd.to_datetime(data['entry_date'], format='%d-%m-%Y', dayfirst=True)
        data['Days'] = (data['entry_date'] - data['entry_date'].min()).dt.days

        X = data[['Days']]
        y = data['Total_Carbon_Footprint_kgCO2']
        model = LinearRegression()
        model.fit(X, y)

        last_date = data['entry_date'].max()
        start_of_next_year = pd.Timestamp(year=last_date.year + 1, month=1, day=1)

        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=365, freq='D')
        future_days = np.array([(date - data['entry_date'].min()).days for date in future_dates]).reshape(-1, 1)
        future_forecast = model.predict(future_days)

        forecast_df = pd.DataFrame({'entry_date': future_dates, 'Predicted_Carbon_Footprint': future_forecast})
        forecast_df['Year'] = forecast_df['entry_date'].dt.year

        next_month_df = forecast_df[forecast_df['entry_date'].dt.month == (last_date.month % 12) + 1]

        monthly_avg_forecast = forecast_df.groupby(forecast_df['entry_date'].dt.to_period('M'))['Predicted_Carbon_Footprint'].mean().reset_index()

        yearly_total_forecast = forecast_df.groupby('Year')['Predicted_Carbon_Footprint'].sum().reset_index()

        return (monthly_avg_forecast, yearly_total_forecast, next_month_df)

    def display_results(self, monthly_avg_forecast, yearly_total_forecast, next_month_df):
        result_window = tk.Toplevel(self.root)
        result_window.title("Prediction Results")
        result_window.geometry("900x600")

        notebook = ttk.Notebook(result_window)
        notebook.pack(fill="both", expand=True)

        self.add_tab(notebook, "Monthly Predictions", monthly_avg_forecast)
        self.add_tab(notebook, "Yearly Predictions", yearly_total_forecast)
        self.add_tab(notebook, "Next Month Daily Predictions", next_month_df)

        download_button = tk.Button(result_window, text="Download Report",
                                    command=lambda: self.download_report(monthly_avg_forecast, yearly_total_forecast, next_month_df),
                                    font=("Helvetica", 14), bg="#FF9800", fg="white")
        download_button.pack(pady=10)

    def add_tab(self, notebook, title, data):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        text_widget = tk.Text(frame, wrap="word")
        text_widget.insert("1.0", data.to_string(index=False, header=True))
        text_widget.pack(fill="both", expand=True)

    def download_report(self, monthly_avg_forecast, yearly_total_forecast, next_month_df):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", ".csv"), ("Text files", ".txt")])
        if not file_path:
            return

        try:
            if file_path.endswith(".csv"):
                monthly_avg_forecast.to_csv(file_path, index=False)
                yearly_total_forecast.to_csv(file_path, index=False, mode='a', header=True)
                next_month_df.to_csv(file_path, index=False, mode='a', header=True)
            else:
                with open(file_path, "w") as f:
                    f.write("Monthly Predictions:\n")
                    f.write(monthly_avg_forecast.to_string(index=False))
                    f.write("\n\nYearly Predictions:\n")
                    f.write(yearly_total_forecast.to_string(index=False))
                    f.write("\n\nNext Month Daily Predictions:\n")
                    f.write(next_month_df.to_string(index=False))

            messagebox.showinfo("Success", f"Report saved successfully at:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def return_to_previous(self):
        self.root.destroy()
        os.system("python index.py")

if __name__ == "__main__":
    root = tk.Tk()
    app = AIMLDataAnalysis(root)
    root.mainloop()
