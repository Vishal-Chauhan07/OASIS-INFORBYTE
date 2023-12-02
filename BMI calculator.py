import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Database setup
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS bmi_records
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              weight REAL,
              height REAL,
              bmi REAL,
              date TEXT)''')
conn.commit()

class BMIApp:
    def _init_(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("400x300")

        self.name_label = ttk.Label(root, text="Name:")
        self.name_entry = ttk.Entry(root)

        self.weight_label = ttk.Label(root, text="Weight (kg):")
        self.weight_entry = ttk.Entry(root)

        self.height_label = ttk.Label(root, text="Height (m):")
        self.height_entry = ttk.Entry(root)

        self.calculate_button = ttk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
        self.save_button = ttk.Button(root, text="Save Record", command=self.save_record)

        self.result_label = ttk.Label(root, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Treeview to display records
        self.tree = ttk.Treeview(root, columns=('ID', 'Name', 'Weight', 'Height', 'BMI', 'Date'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Weight', text='Weight (kg)')
        self.tree.heading('Height', text='Height (m)')
        self.tree.heading('BMI', text='BMI')
        self.tree.heading('Date', text='Date')
        self.tree.grid(row=7, column=0, columnspan=2, pady=10)

        # Plotting
        self.plot_button = ttk.Button(root, text="Plot BMI Trend", command=self.plot_bmi_trend)

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = round(weight / (height ** 2), 2)
            result_text = f"BMI: {bmi:.2f} ({self.get_bmi_category(bmi)})"
            self.result_label.config(text=result_text)
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter valid numbers.")

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal Weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obese"

    def save_record(self):
        name = self.name_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()
        bmi = self.result_label.cget("text").split()[1]
        date = tk.StringVar(value='Now').get()
        c.execute("INSERT INTO bmi_records (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                  (name, weight, height, bmi, date))
        conn.commit()

        self.show_records()

    def show_records(self):
        self.tree.delete(*self.tree.get_children())
        c.execute("SELECT * FROM bmi_records")
        for row in c.fetchall():
            self.tree.insert("", "end", values=row)

    def plot_bmi_trend(self):
        c.execute("SELECT date, bmi FROM bmi_records")
        data = c.fetchall()

        if data:
            dates, bmis = zip(*data)
            fig, ax = plt.subplots()
            ax.plot(dates, bmis, marker='o', linestyle='-', color='b')
            ax.set_xlabel('Date')
            ax.set_ylabel('BMI')
            ax.set_title('BMI Trend Over Time')

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=8, column=0, columnspan=2, pady=10)
            canvas.draw()
        else:
            self.result_label.config(text="No data available for plotting.")


root = tk.Tk()
app = BMIApp(root)
app.show_records()
root.mainloop()

# Close the database connection when the application is closed
conn.close()