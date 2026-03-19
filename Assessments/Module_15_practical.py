import tkinter as tk
from tkinter import messagebox
import os

class User:
    def __init__(self, name):
        self.name = name


class Post:
    def __init__(self, user, title, content):
        self.user = user
        self.title = title
        self.content = content

    def save_to_file(self):
        try:
            filename = f"{self.user.name}_{self.title}.txt"
            with open(filename, "w") as file:
                file.write(f"Author: {self.user.name}\n")
                file.write(f"Title: {self.title}\n\n")
                file.write(self.content)
            return filename
        except Exception as e:
            messagebox.showerror("Error", f"Error saving file: {e}")

class MiniBlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniBlog App")
        self.root.geometry("500x500")

        tk.Label(root, text="Username").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Post Title").pack()
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        tk.Label(root, text="Post Content").pack()
        self.content_text = tk.Text(root, height=8)
        self.content_text.pack()

        tk.Button(root, text="Save Post", command=self.save_post).pack(pady=5)
        tk.Button(root, text="Refresh Posts", command=self.load_posts).pack(pady=5)

        tk.Label(root, text="Saved Posts").pack()
        self.post_listbox = tk.Listbox(root)
        self.post_listbox.pack(fill=tk.BOTH, expand=True)

        tk.Button(root, text="View Post", command=self.view_post).pack(pady=5)

        self.display_text = tk.Text(root, height=10)
        self.display_text.pack()

        self.load_posts()

    def save_post(self):
        username = self.username_entry.get().strip()
        title = self.title_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()

        if not username or not title or not content:
            messagebox.showwarning("Warning", "All fields are required!")
            return

        try:
            user = User(username)
            post = Post(user, title, content)

            filename = post.save_to_file()

            messagebox.showinfo("Success", f"Post saved as {filename}")

            self.clear_fields()
            self.load_posts()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_posts(self):
        self.post_listbox.delete(0, tk.END)

        try:
            files = [f for f in os.listdir() if f.endswith(".txt")]
            for file in files:
                self.post_listbox.insert(tk.END, file)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading posts: {e}")

    def view_post(self):
        try:
            selected = self.post_listbox.get(self.post_listbox.curselection())

            with open(selected, "r") as file:
                content = file.read()

            self.display_text.delete("1.0", tk.END)
            self.display_text.insert(tk.END, content)

        except IndexError:
            messagebox.showwarning("Warning", "Please select a post!")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):
        self.username_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniBlogApp(root)
    root.mainloop()