import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
from PIL import Image, ImageTk

class WeatherApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x400")

        self.api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your API key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

        self.location_label = ttk.Label(root, text="Enter City:")
        self.location_entry = ttk.Entry(root)

        self.search_button = ttk.Button(root, text="Search", command=self.get_weather_data)

        # Weather information labels
        self.weather_icon_label = ttk.Label(root, image=None)
        self.temperature_label = ttk.Label(root, text="")
        self.condition_label = ttk.Label(root, text="")
        self.wind_label = ttk.Label(root, text="")

        # Forecast Treeview
        self.forecast_tree = ttk.Treeview(root, columns=('Time', 'Temperature', 'Condition'), show='headings', height=5)
        self.forecast_tree.heading('Time', text='Time')
        self.forecast_tree.heading('Temperature', text='Temperature')
        self.forecast_tree.heading('Condition', text='Condition')

        # Grid layout
        self.location_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.location_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        self.search_button.grid(row=0, column=2, pady=10, padx=10, sticky="w")

        self.weather_icon_label.grid(row=1, column=0, columnspan=3, pady=10)
        self.temperature_label.grid(row=2, column=0, columnspan=3, pady=5)
        self.condition_label.grid(row=3, column=0, columnspan=3, pady=5)
        self.wind_label.grid(row=4, column=0, columnspan=3, pady=5)

        self.forecast_tree.grid(row=5, column=0, columnspan=3, pady=10)

    def get_weather_data(self):
        city = self.location_entry.get()
        if not city:
            return

        params = {
            'q': city,
            'appid': self.api_key,
            'units': 'metric',  # Use 'imperial' for Fahrenheit
        }

        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            self.display_weather(data)
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")

    def display_weather(self, data):
        if data.get('cod') != 200:
            # Error handling, e.g., city not found
            return

        # Extract relevant weather information
        temperature = data['main']['temp']
        condition = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        icon_code = data['weather'][0]['icon']

        # Display current weather information
        self.temperature_label.config(text=f'Temperature: {temperature} °C')
        self.condition_label.config(text=f'Condition: {condition.capitalize()}')
        self.wind_label.config(text=f'Wind Speed: {wind_speed} m/s')

        # Display weather icon
        icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
        icon_image = Image.open(requests.get(icon_url, stream=True).raw)
        icon_image = icon_image.resize((50, 50), Image.ANTIALIAS)
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.weather_icon_label.config(image=icon_photo)
        self.weather_icon_label.image = icon_photo

        # Display forecast data
        self.display_forecast(data)

    def display_forecast(self, data):
        self.forecast_tree.delete(*self.forecast_tree.get_children())

        if 'list' in data:
            for entry in data['list']:
                timestamp = entry['dt']
                time_str = datetime.utcfromtimestamp(timestamp).strftime('%H:%M')
                temperature = entry['main']['temp']
                condition = entry['weather'][0]['description']
                self.forecast_tree.insert("", "end", values=(time_str, f"{temperature} °C", condition.capitalize()))


root = tk.Tk()
app = WeatherApp(root)
root.mainloop()