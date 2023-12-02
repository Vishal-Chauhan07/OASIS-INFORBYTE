import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
import socket
import threading
import os

class ChatApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.username = None
        self.host = 'localhost'
        self.port = 55555

        # GUI Components
        self.chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.message_entry = ttk.Entry(root, width=50)
        self.send_button = ttk.Button(root, text="Send", command=self.send_message)
        self.attachment_button = ttk.Button(root, text="Attach File", command=self.attach_file)

        # Grid layout
        self.chat_history.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)
        self.attachment_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Socket setup
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # Start receiving messages in a separate thread
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.socket.send(f"{self.username}: {message}".encode())
            self.message_entry.delete(0, tk.END)

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            with open(file_path, 'rb') as file:
                file_data = file.read()
                self.socket.send(f"file|{self.username}|{file_name}".encode())
                self.socket.send(file_data)

    def receive_messages(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if data.startswith("file|"):
                    _, sender, file_name = data.split("|")
                    file_data = self.socket.recv(1024)
                    self.save_file(sender, file_name, file_data)
                else:
                    self.chat_history.insert(tk.END, data + '\n')
                    self.chat_history.yview(tk.END)
            except ConnectionError:
                break

    def save_file(self, sender, file_name, file_data):
        file_path = f"received_files/{sender}_{file_name}"
        with open(file_path, 'wb') as file:
            file.write(file_data)
        self.chat_history.insert(tk.END, f"{sender} sent a file: {file_name}\n")
        self.chat_history.yview(tk.END)


root = tk.Tk()
app = ChatApp(root)
root.mainloop()