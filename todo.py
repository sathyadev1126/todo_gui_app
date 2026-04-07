import tkinter as tk
import sqlite3

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    status TEXT
)
""")
conn.commit()

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("To-Do List App")
root.geometry("600x600")
root.config(bg="#2c3e50")
# ---------- FUNCTIONS ----------

def load_tasks():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        task_text = row[1]
        if row[2] == "done":
            task_text = "✔ " + task_text
        listbox.insert(tk.END, task_text)

def add_task():
    task = task_entry.get()
    if task != "":
        cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "pending"))
        conn.commit()
        task_entry.delete(0, tk.END)
        load_tasks()

def delete_task():
    try:
        selected = listbox.curselection()[0]
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        task_id = tasks[selected][0]

        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()
    except:
        pass

def mark_done():
    try:
        selected = listbox.curselection()[0]
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        task_id = tasks[selected][0]

        cursor.execute("UPDATE tasks SET status=? WHERE id=?", ("done", task_id))
        conn.commit()
        load_tasks()
    except:
        pass

# ---------- UI ELEMENTS ----------

task_entry = tk.Entry(root, width=40, font=("Arial", 16), bg="#ecf0f1", fg="black")
task_entry.pack(pady=10)

listbox = tk.Listbox(root, width=50, height=18, bg="#ecf0f1", fg="black", font=("Arial", 13))
listbox.pack(pady=10 )

add_btn = tk.Button(root, text="Add Task", bg="#27ae60", fg="white", command=add_task)
add_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", bg="#e74c3c", fg="white", command=delete_task)
delete_btn.pack(pady=5)

done_btn = tk.Button(root, text="Mark Done", bg="#2980b9", fg="white", command=mark_done)
done_btn.pack(pady=5 )

# ---------- LOAD DATA ----------
load_tasks()

# ---------- RUN APP ----------
root.mainloop()