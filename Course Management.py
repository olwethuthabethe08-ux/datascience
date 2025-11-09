import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

def init_db():
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    # courses table (your existing table)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            course_code TEXT UNIQUE NOT NULL,
            instructor TEXT,
            credits INTEGER
        )
    ''')
    # student_courses table to link students and courses (assignments)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER
            -- we don't enforce FK here to keep it simple and avoid errors if other modules aren't loaded
        )
    ''')
    conn.commit()
    conn.close()

# -------------------- DATABASE FUNCTIONS --------------------
def add_course(name, code, instructor, credits):
    try:
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_name, course_code, instructor, credits) VALUES (?, ?, ?, ?)",
                       (name, code, instructor, credits))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course added successfully!")
        view_courses()
        load_courses_into_combobox()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add course: {e}")


def update_course(course_id, name, instructor, credits):
    try:
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE courses SET course_name=?, instructor=?, credits=? WHERE course_id=?",
                       (name, instructor, credits, course_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Course updated successfully!")
        view_courses()
        load_courses_into_combobox()
    except Exception as e:
        messagebox.showerror("Error", f"Update failed: {e}")


def delete_course(course_id):
    try:
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE course_id=?", (course_id,))
        # Also remove any assignments for this course
        cursor.execute("DELETE FROM student_courses WHERE course_id=?", (course_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Course deleted.")
        view_courses()
        load_courses_into_combobox()
        view_assignments()
    except Exception as e:
        messagebox.showerror("Error", f"Deletion failed: {e}")


def view_courses():
    for i in course_table.get_children():
        course_table.delete(i)

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    for row in rows:
        course_table.insert('', 'end', values=row)
    conn.close()

# -------------------- ASSIGNMENTS / STUDENTS --------------------

def load_students_into_combobox():
    """Load students from 'students' table into the student combobox.
       If students table doesn't exist or is empty, combobox will be empty."""
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_id, name FROM students")
        rows = cursor.fetchall()
        student_values = [f"{r[0]} - {r[1]}" for r in rows]
        combo_student['values'] = student_values
    except Exception:
        # No students table or another error: leave combobox empty
        combo_student['values'] = []
    conn.close()

def load_courses_into_combobox():
    """Load courses into the course combobox."""
    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM courses")
    rows = cursor.fetchall()
    course_values = [f"{r[0]} - {r[1]}" for r in rows]
    combo_course['values'] = course_values
    conn.close()

def assign_student_to_course():
    """Assign selected student to selected course."""
    student_sel = combo_student.get().strip()
    course_sel = combo_course.get().strip()
    if not student_sel or not course_sel:
        messagebox.showwarning("Input Error", "Please select both a student and a course.")
        return

    try:
        student_id = int(student_sel.split(" - ")[0])
        course_id = int(course_sel.split(" - ")[0])
    except Exception:
        messagebox.showerror("Format Error", "Selection format invalid. Please re-load the lists.")
        return

    try:
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        # Prevent duplicate assignment
        cursor.execute("SELECT COUNT(*) FROM student_courses WHERE student_id=? AND course_id=?", (student_id, course_id))
        if cursor.fetchone()[0] > 0:
            messagebox.showinfo("Info", "Student is already assigned to this course.")
            conn.close()
            return

        cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",
                       (student_id, course_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Assigned", f"Student {student_id} assigned to Course {course_id}.")
        view_assignments()
    except Exception as e:
        messagebox.showerror("Error", f"Assignment failed: {e}")

def view_assignments():
    """Show all assignments in the assignments table."""
    for i in assignments_table.get_children():
        assignments_table.delete(i)

    conn = sqlite3.connect("student_management.db")
    cursor = conn.cursor()
    # Try to join with students and courses if they exist, otherwise show ids
    try:
        cursor.execute('''
            SELECT sc.id,
                   sc.student_id,
                   COALESCE(s.name, 'Unknown') AS student_name,
                   sc.course_id,
                   COALESCE(c.course_name, 'Unknown') AS course_name
            FROM student_courses sc
            LEFT JOIN students s ON sc.student_id = s.student_id
            LEFT JOIN courses c ON sc.course_id = c.course_id
        ''')
        rows = cursor.fetchall()
        for r in rows:
            # Show: assignment id, student (id - name), course (id - name)
            student_text = f"{r[1]} - {r[2]}"
            course_text = f"{r[3]} - {r[4]}"
            assignments_table.insert('', 'end', values=(r[0], student_text, course_text))
    except Exception as e:
        # If student_courses table doesn't exist or other error
        print("Error loading assignments:", e)
    conn.close()

def remove_assignment():
    selected = assignments_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an assignment to remove.")
        return
    assignment_id = assignments_table.item(selected[0])['values'][0]
    try:
        conn = sqlite3.connect("student_management.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student_courses WHERE id=?", (assignment_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Removed", "Assignment removed.")
        view_assignments()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove assignment: {e}")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_code.delete(0, tk.END)
    entry_instructor.delete(0, tk.END)
    entry_credits.delete(0, tk.END)

def on_add():
    name = entry_name.get()
    code = entry_code.get()
    instructor = entry_instructor.get()
    credits = entry_credits.get()
    if not name or not code or not credits:
        messagebox.showwarning("Input Error", "Please fill in all required fields.")
        return
    add_course(name, code, instructor, int(credits))
    clear_fields()

def on_update():
    selected = course_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a course to update.")
        return
    course_id = course_table.item(selected[0])['values'][0]
    name = entry_name.get()
    instructor = entry_instructor.get()
    credits = entry_credits.get()
    update_course(course_id, name, instructor, int(credits))

def on_delete():
    selected = course_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a course to delete.")
        return
    course_id = course_table.item(selected[0])['values'][0]
    delete_course(course_id)

root = tk.Tk()
root.title("Course Management Module")
root.geometry("820x600")
root.config(bg="#f5f5f5")

# Input Frame
frame_input = tk.Frame(root, bg="#f5f5f5", padx=10, pady=10)
frame_input.pack(fill='x')

tk.Label(frame_input, text="Course Name:", bg="#f5f5f5").grid(row=0, column=0)
entry_name = tk.Entry(frame_input, width=25)
entry_name.grid(row=0, column=1)

tk.Label(frame_input, text="Course Code:", bg="#f5f5f5").grid(row=1, column=0)
entry_code = tk.Entry(frame_input, width=25)
entry_code.grid(row=1, column=1)

tk.Label(frame_input, text="Instructor:", bg="#f5f5f5").grid(row=0, column=2)
entry_instructor = tk.Entry(frame_input, width=25)
entry_instructor.grid(row=0, column=3)

tk.Label(frame_input, text="Credits:", bg="#f5f5f5").grid(row=1, column=2)
entry_credits = tk.Entry(frame_input, width=25)
entry_credits.grid(row=1, column=3)

tk.Button(frame_input, text="Add Course", command=on_add, bg="#FF007F", fg="white").grid(row=2, column=0, pady=10)
tk.Button(frame_input, text="Update Course", command=on_update, bg="#FFB6C1", fg="white").grid(row=2, column=1, pady=10)
tk.Button(frame_input, text="Delete Course", command=on_delete, bg="#FF69B4", fg="white").grid(row=2, column=2, pady=10)
tk.Button(frame_input, text="Clear Fields", command=clear_fields, bg="#FF00FF", fg="white").grid(row=2, column=3, pady=10)

columns = ("ID", "Name", "Code", "Instructor", "Credits")
course_table = ttk.Treeview(root, columns=columns, show='headings', height=8)
for col in columns:
    course_table.heading(col, text=col)
    course_table.column(col, width=140)

course_table.pack(fill='x', padx=10, pady=5)

assign_frame = tk.LabelFrame(root, text="Assign Student to Course", padx=10, pady=10)
assign_frame.pack(fill='x', padx=10, pady=10)

tk.Label(assign_frame, text="Student (id - name):").grid(row=0, column=0, sticky='w')
combo_student = ttk.Combobox(assign_frame, width=30)
combo_student.grid(row=0, column=1, padx=5, pady=5)

tk.Label(assign_frame, text="Course (id - name):").grid(row=1, column=0, sticky='w')
combo_course = ttk.Combobox(assign_frame, width=30)
combo_course.grid(row=1, column=1, padx=5, pady=5)

tk.Button(assign_frame, text="Assign Student", command=assign_student_to_course, bg="#4CAF50", fg="white").grid(row=0, column=2, padx=10)
tk.Button(assign_frame, text="Refresh Lists", command=lambda: (load_students_into_combobox(), load_courses_into_combobox()), bg="#2196F3", fg="white").grid(row=1, column=2, padx=10)

tk.Label(root, text="Assignments (Student -> Course):", bg="#f5f5f5").pack(anchor='w', padx=12)
assign_cols = ("Assignment ID", "Student", "Course")
assignments_table = ttk.Treeview(root, columns=assign_cols, show='headings', height=6)
for col in assign_cols:
    assignments_table.heading(col, text=col)
    assignments_table.column(col, width=250)
assignments_table.pack(fill='both', expand=False, padx=10, pady=5)

tk.Button(root, text="Remove Selected Assignment", command=remove_assignment, bg="#f44336", fg="white").pack(pady=6)

init_db()
view_courses()
load_courses_into_combobox()
load_students_into_combobox()
view_assignments()

root.mainloop()
