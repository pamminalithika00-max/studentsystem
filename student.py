import tkinter as tk
from tkinter import messagebox
import sqlite3

# ================= DATABASE =================
def setup_database():
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Students table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT UNIQUE,
        branch TEXT,
        year INTEGER,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

# ================= REGISTER =================
def register_user():
    u = reg_user.get()
    p = reg_pass.get()

    if u == "" or p == "":
        messagebox.showerror("Error", "All fields required")
        return

    try:
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (u,p))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration Successful")
        reg_win.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

# ================= LOGIN =================
def login_user():
    u = log_user.get()
    p = log_pass.get()

    conn = sqlite3.connect("student.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
    user = cur.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login", "Login Successful")
        login_win.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Error", "Invalid Login")

# ================= REGISTER WINDOW =================
def open_register():
    global reg_win, reg_user, reg_pass
    reg_win = tk.Toplevel()
    reg_win.title("Register")
    reg_win.geometry("300x200")

    tk.Label(reg_win, text="Register", font=("Arial",14)).pack(pady=10)
    tk.Label(reg_win, text="Username").pack()
    reg_user = tk.Entry(reg_win)
    reg_user.pack()

    tk.Label(reg_win, text="Password").pack()
    reg_pass = tk.Entry(reg_win, show="*")
    reg_pass.pack()

    tk.Button(reg_win, text="Register", command=register_user).pack(pady=10)

# ================= ADD STUDENT =================
def add_student():
    try:
        conn = sqlite3.connect("student.db")
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO students (name,roll,branch,year,phone)
        VALUES (?,?,?,?,?)
        """, (
            e_name.get(),
            e_roll.get(),
            e_branch.get(),
            int(e_year.get()),
            e_phone.get()
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Student Added")
        clear_entries()
    except:
        messagebox.showerror("Error", "Roll already exists / Invalid data")

def clear_entries():
    e_name.delete(0,'end')
    e_roll.delete(0,'end')
    e_branch.delete(0,'end')
    e_year.delete(0,'end')
    e_phone.delete(0,'end')

# ================= VIEW STUDENTS =================
def view_students():
    view = tk.Toplevel()
    view.title("Students List")
    view.geometry("500x300")

    conn = sqlite3.connect("student.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()
    conn.close()

    text = tk.Text(view)
    text.pack(fill="both", expand=True)

    text.insert("end", "ID | Name | Roll | Branch | Year | Phone\n")
    text.insert("end", "-"*60 + "\n")

    for r in rows:
        text.insert("end", f"{r}\n")

# ================= DASHBOARD =================
def open_dashboard():
    global e_name, e_roll, e_branch, e_year, e_phone

    dash = tk.Tk()
    dash.title("Student Management System")
    dash.geometry("400x400")

    tk.Label(dash, text="Student Management", font=("Arial",16)).pack(pady=10)

    e_name = tk.Entry(dash)
    e_roll = tk.Entry(dash)
    e_branch = tk.Entry(dash)
    e_year = tk.Entry(dash)
    e_phone = tk.Entry(dash)

    for label, entry in [
        ("Name", e_name),
        ("Roll", e_roll),
        ("Branch", e_branch),
        ("Year", e_year),
        ("Phone", e_phone)
    ]:
        tk.Label(dash, text=label).pack()
        entry.pack()

    tk.Button(dash, text="Add Student", command=add_student).pack(pady=5)
    tk.Button(dash, text="View Students", command=view_students).pack(pady=5)

    dash.mainloop()

# ================= LOGIN WINDOW =================
setup_database()

login_win = tk.Tk()
login_win.title("Login Page")
login_win.geometry("300x220")

tk.Label(login_win, text="Login", font=("Arial",16)).pack(pady=10)

tk.Label(login_win, text="Username").pack()
log_user = tk.Entry(login_win)
log_user.pack()

tk.Label(login_win, text="Password").pack()
log_pass = tk.Entry(login_win, show="*")
log_pass.pack()

tk.Button(login_win, text="Login", command=login_user).pack(pady=10)
tk.Button(login_win, text="Register", command=open_register).pack()

login_win.mainloop()