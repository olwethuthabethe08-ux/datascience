Import tkinter as tk
from tkinter import Menu, Frame, Label, Button, messagebox

class SMSApp:
    def _init_(self, master):
        self.master = master
        master.title("Student Management System")
        master.geometry("1024x768")

        # 1. Menu Bar
        self.create_menu_bar()

        # 2. Toolbar Frame
        self.create_toolbar()

        # 3. Main Content Area (Placeholder)
        self.content_frame = Frame(master, bg="#f0f0f0")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        Label(self.content_frame, text="Welcome to the Student Management System", font=("Arial", 24)).pack(pady=50)

        # 4. Status Bar
        self.create_status_bar()

    # --- Menu Bar Implementation ---
    def create_menu_bar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # File Menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Student", command=lambda: self.placeholder_action("New Student"))
        file_menu.add_command(label="Save Report", command=lambda: self.placeholder_action("Save Report"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)

        # Student Menu
        student_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Student", menu=student_menu)
        student_menu.add_command(label="Add New Student", command=lambda: self.placeholder_action("Add New Student"))
        student_menu.add_command(label="Manage Students", command=lambda: self.placeholder_action("Manage Students"))
        student_menu.add_command(label="Search Student", command=lambda: self.placeholder_action("Search Student"))

        # Course Menu
        course_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Course", menu=course_menu)
        course_menu.add_command(label="Add New Course", command=lambda: self.placeholder_action("Add New Course"))
        course_menu.add_command(label="Manage Courses", command=lambda: self.placeholder_action("Manage Courses"))
        course_menu.add_command(label="Assign Course", command=lambda: self.placeholder_action("Assign Course"))

        # Reports Menu
        reports_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Generate Transcript", command=lambda: self.placeholder_action("Generate Transcript"))
        reports_menu.add_command(label="Enrollment Report", command=lambda: self.placeholder_action("Enrollment Report"))
        reports_menu.add_command(label="GPA Statistics", command=lambda: self.placeholder_action("GPA Statistics"))

        # Notifications Menu
        notifications_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Notifications", menu=notifications_menu)
        notifications_menu.add_command(label="Send Bulk Email", command=lambda: self.placeholder_action("Send Bulk Email"))
        notifications_menu.add_command(label="Send SMS Alert", command=lambda: self.placeholder_action("Send SMS Alert"))
        notifications_menu.add_command(label="Notification Log", command=lambda: self.placeholder_action("Notification Log"))

        # Help Menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=lambda: self.placeholder_action("About SMS"))
        help_menu.add_command(label="Documentation", command=lambda: self.placeholder_action("Documentation"))

    # --- Toolbar Implementation ---
    def create_toolbar(self):
        toolbar = Frame(self.master, bd=1, relief=tk.RAISED)

        # Quick Access Buttons
        self.add_button(toolbar, "Add Student", "Add New Student", "green")
        self.add_button(toolbar, "Add Course", "Add New Course", "blue")
        self.add_button(toolbar, "Transcript", "Generate Transcript", "purple")
        self.add_button(toolbar, "Send SMS", "Send SMS Alert", "orange")

        toolbar.pack(side=tk.TOP, fill=tk.X)

    def add_button(self, parent, text, action_name, color):
        button = Button(parent, text=text, fg="white", bg=color,
                        command=lambda: self.placeholder_action(action_name))
        button.pack(side=tk.LEFT, padx=5, pady=5)

    # --- Status Bar Implementation ---
    def create_status_bar(self):
        self.db_status = tk.StringVar()
        self.api_status = tk.StringVar()

        # Simulate initial connection status
        self.db_status.set("Database: Connected (PostgreSQL)")
        self.api_status.set("APIs: Ready (Twilio, SendGrid)")

        status_bar = Frame(self.master, bd=1, relief=tk.SUNKEN)

        # Database Status Label
        db_label = Label(status_bar, textvariable=self.db_status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        db_label.pack(side=tk.LEFT, padx=10, pady=2)

        # API Status Label
        api_label = Label(status_bar, textvariable=self.api_status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        api_label.pack(side=tk.LEFT, padx=10, pady=2)

        # Right-aligned status (e.g., current user)
        user_label = Label(status_bar, text="User: Admin", bd=1, relief=tk.SUNKEN, anchor=tk.E)
        user_label.pack(side=tk.RIGHT, padx=10, pady=2)

        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Utility Functions ---
    def placeholder_action(self, action_name):
        """A function to show that the menu/toolbar item was clicked."""
        messagebox.showinfo("Action Triggered", f"Action: {action_name} functionality will be implemented here.")

    def on_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit the application?"):
            self.master.quit()

if _name_ == "_main_":
    root = tk.Tk()
    app = SMSApp(root)
    root.mainloop()
