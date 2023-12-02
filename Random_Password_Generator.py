import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import string
import pyperclip

class PasswordGeneratorApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("400x300")

        self.length_label = ttk.Label(root, text="Password Length:")
        self.length_entry = ttk.Entry(root)
        self.length_entry.insert(0, "12")  # Default password length

        self.lowercase_var = tk.IntVar()
        self.lowercase_checkbox = ttk.Checkbutton(root, text="Include Lowercase", variable=self.lowercase_var)

        self.uppercase_var = tk.IntVar()
        self.uppercase_checkbox = ttk.Checkbutton(root, text="Include Uppercase", variable=self.uppercase_var)

        self.digits_var = tk.IntVar()
        self.digits_checkbox = ttk.Checkbutton(root, text="Include Digits", variable=self.digits_var)

        self.symbols_var = tk.IntVar()
        self.symbols_checkbox = ttk.Checkbutton(root, text="Include Symbols", variable=self.symbols_var)

        self.generate_button = ttk.Button(root, text="Generate Password", command=self.generate_password)
        self.copy_button = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)

        # Password display
        self.password_var = tk.StringVar()
        self.password_label = ttk.Label(root, textvariable=self.password_var, font=("Courier", 12))

        # Grid layout
        self.length_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.length_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")
        self.lowercase_checkbox.grid(row=1, column=0, pady=5, padx=10, sticky="w")
        self.uppercase_checkbox.grid(row=2, column=0, pady=5, padx=10, sticky="w")
        self.digits_checkbox.grid(row=3, column=0, pady=5, padx=10, sticky="w")
        self.symbols_checkbox.grid(row=4, column=0, pady=5, padx=10, sticky="w")
        self.generate_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.copy_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.password_label.grid(row=7, column=0, columnspan=2, pady=10, padx=10)

    def generate_password(self):
        length = int(self.length_entry.get())
        lowercase = bool(self.lowercase_var.get())
        uppercase = bool(self.uppercase_var.get())
        digits = bool(self.digits_var.get())
        symbols = bool(self.symbols_var.get())

        if not (lowercase or uppercase or digits or symbols):
            messagebox.showinfo("Error", "Please select at least one character type.")
            return

        all_characters = ""
        if lowercase:
            all_characters += string.ascii_lowercase
        if uppercase:
            all_characters += string.ascii_uppercase
        if digits:
            all_characters += string.digits
        if symbols:
            all_characters += string.punctuation

        password = ''.join(random.choice(all_characters) for _ in range(length))
        self.password_var.set(password)

    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            messagebox.showinfo("Error", "No password generated to copy.")


root = tk.Tk()
app = PasswordGeneratorApp(root)
root.mainloop()