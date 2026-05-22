import tkinter as tk
from tkinter import messagebox

def submit():
    name = entry.get()
    if name == "":
        messagebox.showwarning("Please enter your name")
    else:
        messagebox.showinfo("Welcome", f"Hello {name}!")

root = tk.Tk()
root.title("My Python Tkinter Page")
root.geometry("400x300")
root.configure(bg="Orange")

l1 = tk.Label(root,font=("Calibari", 16, "bold"), bg="orange")
l1.grid(row=0,column=0,sticky='w')

l2 = tk.Label(root, text="Enter your name:", 
             font=("Arial", 12), bg="orange")
l2.grid(row=0,column=0,sticky='w')

entry = tk.Entry(root, width=20, font=("Arial", 12))
entry.grid(row=1,column=0,sticky='w')

btn=tk.Radiobutton(value=0,text='Male',bg='Orange',fg='Black',
                   font='Calibari')
btn2=tk.Radiobutton(value=1,text='Female',bg='Orange',fg='Black',
                   font='Calibari')
btn.grid(row=2,column=0,sticky='w')
btn2.grid(row=2,column=1,sticky='w')

root.mainloop()