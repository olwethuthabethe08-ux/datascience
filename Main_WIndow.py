import tkinter as tk
from tkinter import messagebox

class StudentManagementSystem:
    def _init_(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("900x600")

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        student_menu = tk.Menu(menubar, tearoff=0)
        student_menu.add_command(label="Add Student")
        student_menu.add_command(label="Update Student")
        student_menu.add_command(label="Delete Student")
        student_menu.add_command(label="View Students")
        menubar.add_cascade(label="Student", menu=student_menu)

        course_menu = tk.Menu(menubar, tearoff=0)
        course_menu.add_command(label="Add Course")
        course_menu.add_command(label="Update Course")
        course_menu.add_command(label="Delete Course")
        course_menu.add_command(label="View Courses")
        menubar.add_cascade(label="Course", menu=course_menu)

        reports_menu = tk.Menu(menubar, tearoff=0)
        reports_menu.add_command(label="Student Transcript")
        reports_menu.add_command(label="Course Enrollment Report")
        menubar.add_cascade(label="Reports", menu=reports_menu)

        notifications_menu = tk.Menu(menubar, tearoff=0)
        notifications_menu.add_command(label="Send Email")
        notifications_menu.add_command(label="Send SMS")
        menubar.add_cascade(label="Notifications", menu=notifications_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)


        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)

        btn_add = tk.Button(toolbar, text="Add Student", command=self.temp_action)
        btn_add.pack(side=tk.LEFT, padx=2, pady=2)

        btn_view = tk.Button(toolbar, text="View Students", command=self.temp_action)
        btn_view.pack(side=tk.LEFT, padx=2, pady=2)

        btn_course = tk.Button(toolbar, text="Courses", command=self.temp_action)
        btn_course.pack(side=tk.LEFT, padx=2, pady=2)

        btn_reports = tk.Button(toolbar, text="Reports", command=self.temp_action)
        btn_reports.pack(side=tk.LEFT, padx=2, pady=2)

        btn_notify = tk.Button(toolbar, text="Send Notification", command=self.temp_action)
        btn_notify.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.pack(side=tk.TOP, fill=tk.X)


        self.statusbar = tk.Label(
            self.root,
            text="Database: Connected | Email API: Connected | SMS API: Connected",
            bd=1, relief=tk.SUNKEN, anchor="w"
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

    def show_about(self):
        messagebox.showinfo("About", "Student Management System\nDeveloped by You")

    def temp_action(self):
        messagebox.showinfo("Info", "This feature will be implemented later.")


if _name_ == "_main_":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.mainloop()