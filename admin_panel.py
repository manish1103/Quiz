import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Mani123@"

LEADERBOARD_FILE = os.path.join("data", "leaderboard.json")

class AdminLogin:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Login")
        self.master.geometry("300x200")
        self.master.resizable(False, False)

        tk.Label(master, text="Admin Login", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(master, text="Username").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Password").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Button(master, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.master.destroy()
            self.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

    def open_dashboard(self):
        dashboard = tk.Tk()
        dashboard.title("Admin Panel - Quiz Leaderboard")
        dashboard.geometry("600x400")

        tree = ttk.Treeview(dashboard, columns=("Username", "Score", "Category"), show="headings")
        tree.heading("Username", text="Username")
        tree.heading("Score", text="Score")
        tree.heading("Category", text="Category")
        tree.pack(fill=tk.BOTH, expand=True)

        
        if os.path.exists(LEADERBOARD_FILE):
            try:
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for entry in data:
                        tree.insert("", "end", values=(entry["username"], entry["score"], entry["category"]))
            except:
                messagebox.showwarning("Error", "Leaderboard file is corrupted or unreadable.")
        else:
            messagebox.showinfo("Info", "No leaderboard data found yet.")

        dashboard.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminLogin(root)
    root.mainloop()
