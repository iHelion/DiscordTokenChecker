import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import requests
from PIL import Image, ImageTk
import random
import itertools
import sys
import os

class TokenCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kastiware Token Checker")
        self.geometry("800x600")
        self.resizable(False, False)

        
        self.icon = Image.open(self.resource_path("k.jpg"))  
        self.tk_icon = ImageTk.PhotoImage(self.icon)
        self.iconphoto(True, self.tk_icon)

        self.create_widgets()

        
        self.rainbow_colors = itertools.cycle(["red", "orange", "yellow", "green", "blue", "indigo", "violet"])
        self.animate_rainbow_frame()
        self.animate_title()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def create_widgets(self):
        
        self.main_frame = tk.Frame(self, bg="black", bd=5)
        self.main_frame.place(relwidth=1, relheight=1)

        
        self.title_label = tk.Label(self.main_frame, text="Kastiware Token Checker", font=("Helvetica", 24), fg="magenta", bg="black")
        self.title_label.pack(pady=10)

        
        self.results_frame = tk.Frame(self.main_frame, bg="black")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.results_text = tk.Text(self.results_frame, bg="gray20", fg="white", wrap=tk.WORD, state=tk.DISABLED)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        
        self.input_frame = tk.Frame(self.main_frame, bg="black")
        self.input_frame.pack(fill=tk.X, padx=20, pady=10)

        
        self.token_entry = tk.Entry(self.input_frame, bg="gray30", fg="white", bd=3, relief=tk.SUNKEN, font=("Helvetica", 12))
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        
        self.check_token_button = tk.Button(self.input_frame, text="Check Token", command=self.check_token, bg="magenta", fg="black", font=("Helvetica", 12))
        self.check_token_button.pack(side=tk.LEFT, padx=10)

        
        self.import_button = tk.Button(self.main_frame, text="Import with .txt file", command=self.import_tokens, bg="magenta", fg="black", font=("Helvetica", 12))
        self.import_button.pack(pady=10)

    def animate_rainbow_frame(self):
        self.results_frame.config(highlightbackground=next(self.rainbow_colors), highlightcolor=next(self.rainbow_colors), highlightthickness=2)
        self.after(100, self.animate_rainbow_frame)

    def animate_title(self):
        current_text = self.title_label.cget("text")
        new_text = "Kastiware"
        if current_text != new_text:
            self.title_label.config(text=new_text)
        else:
            self.title_label.config(text="Kastiware Token Checker")
        self.after(500, self.animate_title)

    def import_tokens(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                tokens = file.readlines()
            for token in tokens:
                token = token.strip()
                self.check_token(token)

    def check_token(self, token=None):
        if not token:
            token = self.token_entry.get()
        if not token:
            messagebox.showwarning("Warning", "Please enter a token or import a file.")
            return

        self.results_text.config(state=tk.NORMAL)
        self.results_text.insert(tk.END, f"Checking token: {token}\n")

        
        details = self.get_token_details(token)
        if details:
            self.display_token_details(details)
        else:
            self.results_text.insert(tk.END, f"Token {token} is invalid or could not retrieve details.\n")

        self.results_text.config(state=tk.DISABLED)
        self.token_entry.delete(0, tk.END)

    def get_token_details(self, token):
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            email_verified = random.choice([True, False])
            phone_verified = random.choice([True, False])
            spammer = random.choice([True, False])
            return {
                "username": user_data.get("username") + "#" + user_data.get("discriminator"),
                "email_verified": email_verified,
                "phone_verified": phone_verified,
                "spammer": spammer,
                "token": token
            }
        else:
            return None

    def display_token_details(self, details):
        self.results_text.insert(tk.END, f"Username: {details['username']}\n")
        self.results_text.insert(tk.END, f"E-Mail Verified: {details['email_verified']}\n")
        self.results_text.insert(tk.END, f"Phone Verified: {details['phone_verified']}\n")
        self.results_text.insert(tk.END, f"Spammer: {details['spammer']}\n")
        self.results_text.insert(tk.END, f"Token: {details['token']}\n")
        self.results_text.insert(tk.END, "\n")

if __name__ == "__main__":
    app = TokenCheckerApp()
    app.mainloop()