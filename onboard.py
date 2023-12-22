import tkinter as tk
import sqlite3
from fpdf import FPDF

def initialize_database():
    conn = sqlite3.connect('employee_data.db')  # This creates the database file
    cur = conn.cursor()
    # Create a table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            start_date TEXT,
            title TEXT,
            department TEXT,
            cell_phone_provided BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Onboarding")
        self.root.geometry("500x800")
        self.employee_id = None  # Set employee ID for search/edit
        
        # High-contrast dark theme colors
        background_color = '#424242'  # Professional Slate
        text_color = '#FFFFFF'  # White
        button_color = '#757575'  # Gray
        entry_bg = '#616161'  # Dark Gray
        entry_fg = '#FFFFFF'  # White

        self.root.configure(bg=background_color)

        # Define a custom font style for the application
        custom_font = ("Arial", 10)  # Example: Using Arial

        # Style configuration
        style_config = {'bg': background_color, 'fg': text_color, 'font': custom_font}

        # Name Field
        self.label = tk.Label(self.root, text="Name", **style_config)
        self.label.pack(anchor='w', padx=10, pady=5)
        self.name_entry = tk.Entry(self.root, font=custom_font, bg=entry_bg, fg=entry_fg)
        self.name_entry.pack(anchor='w', padx=10, pady=5)

        # Start Date Field
        self.label = tk.Label(self.root, text="Start date", **style_config)
        self.label.pack(anchor='w', padx=10, pady=5)
        self.start_date_entry = tk.Entry(self.root, font=custom_font, bg=entry_bg, fg=entry_fg)
        self.start_date_entry.pack(anchor='w', padx=10, pady=5)

        # Title Field
        self.label = tk.Label(self.root, text="Title", **style_config)
        self.label.pack(anchor='w', padx=10, pady=5)
        self.title_entry = tk.Entry(self.root, font=custom_font, bg=entry_bg, fg=entry_fg)
        self.title_entry.pack(anchor='w', padx=10, pady=5)

        # Department Dropdown
        self.label = tk.Label(self.root, text="Department", **style_config)
        self.label.pack(anchor='w', padx=10, pady=5)
        self.department_var = tk.StringVar(root)
        self.departments = ["Executive", "Management", "Clinical", "Administrative"]
        self.department_var.set(self.departments[0])
        self.department_menu = tk.OptionMenu(root, self.department_var, *self.departments)
        self.department_menu.config(bg=button_color, fg=text_color, font=custom_font)
        self.department_menu.pack(anchor='w', padx=10, pady=5)

        # Checkbox for Company Cell Phone
        self.check_var = tk.IntVar()
        self.checkbox = tk.Checkbutton(self.root, text="Company cell phone provided?", variable=self.check_var, **style_config)
        self.checkbox.pack(anchor='w', padx=10, pady=5)

        # Define the onboarding tasks dictionary
        self.onboarding_tasks = {
            "Executive": ["User account created", "Zoom account created (licensed)", "Laptop provided", "Computer/Email Training Complete"],
            "Management": ["User account created", "Zoom account created (licensed)", "Laptop provided", "Computer/Email Training Complete"],
            "Clinical": ["User account created", "Zoom account created (licensed)", "Laptop provided", "Computer/Email Training Complete"],
            "Administrative": ["User account created", "Zoom account created (basic)", "Laptop provided (if remote)", "Computer/Email Training Complete"]
        }

        # Confirm Button
        self.confirm_button = tk.Button(root, text="Create Record", command=self.confirm, bg=button_color, fg=text_color, font=custom_font)
        self.confirm_button.pack(anchor='w', padx=12, pady=10)
        
        # Search entry box
        self.search_entry = tk.Entry(root, font=custom_font, bg=entry_bg, fg=entry_fg)
        self.search_entry.pack(anchor='w', padx=12, pady=5)

        # Search button
        self.search_button = tk.Button(root, text="Search Records", command=self.read_records, bg=button_color, fg=text_color, font=custom_font)
        self.search_button.pack(anchor='w', padx=12, pady=5)

        # Display for search results
        self.employee_listbox = tk.Listbox(self.root, font=custom_font, bg=entry_bg, fg=entry_fg)
        self.employee_listbox.pack(anchor='w', padx=25, pady=25)
        
        # Edit button  
        self.edit_button = tk.Button(root, text="Edit Record", command=self.edit_records, bg=button_color, fg=text_color, font=custom_font)
        self.edit_button.pack(anchor='w', padx=12, pady=5)

        # Delete button
        self.delete_button = tk.Button(root, text="Delete Record", command=self.delete_record, bg=button_color, fg=text_color, font=custom_font)
        self.delete_button.pack(anchor='w', padx=12, pady=5)

    def edit_records(self):
        selected_index = self.employee_listbox.curselection()
        if not selected_index:
            print("No item selected")
            return
        
        employee_id = self.employee_listbox.get(selected_index[0])[0]

        try:
            with sqlite3.connect('employee_data.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
                employee_data = cur.fetchone()

                #Populate the fields
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, employee_data[1])
                print(employee_data[1])
                print(employee_id)

                self.start_date_entry.delete(0, tk.END)
                self.start_date_entry.insert(0, employee_data[2])
                print(employee_data[2])

                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, employee_data[3])
                print(employee_data[3])

                self.department_var.set(employee_data[4])
                print(employee_data[4])

                self.check_var.set(employee_data[5])

                self.employee_id = employee_id
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def read_records(self):
        search_query = self.search_entry.get()
        self.employee_listbox.delete(0, tk.END)

        try:
            with sqlite3.connect('employee_data.db') as conn:
                cur = conn.cursor()
                query = "SELECT * FROM employees WHERE name LIKE ?"
                cur.execute(query, ('%' + search_query + '%',))
                rows = cur.fetchall()
                for row in rows:
                    self.employee_listbox.insert(tk.END, row)
                    print(self.employee_id)
            if rows:
                self.employee_listbox.pack(anchor='w', padx=10, pady=10)  # Show the Listbox
            else:
                self.employee_listbox.pack_forget()  # Hide the Listbox if no results
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def delete_record(self):
        selection = self.employee_listbox.curselection()
        if not selection:
            print("No item selected")
            return

        selected_index = selection[0]
        selected_item = self.employee_listbox.get(selected_index)
        employee_index = selected_item[0]

        try:
            with sqlite3.connect('employee_data.db') as conn:
                cur = conn.cursor()
                query = "DELETE FROM employees WHERE id = ?"
                cur.execute(query, (employee_index,))
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        self.refresh_employee_list()
        print(f"{employee_index} removed")

    def refresh_employee_list(self):
        self.employee_listbox.delete(0, tk.END)

        try:
            with sqlite3.connect('employee_data.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM employees ORDER BY id")
                rows = cur.fetchall()
                for row in rows:
                    self.employee_listbox.insert(tk.END, row)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def clear_fields(self):
        # Method to clear all input fields
        self.name_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.department_var.set(self.departments[0])
        self.check_var.set(0)  

    def confirm(self):
        name = self.name_entry.get()
        start_date = self.start_date_entry.get()
        title = self.title_entry.get()
        department = self.department_var.get()
        cell_phone = "Yes" if self.check_var.get() == 1 else "No"
        tasks = self.onboarding_tasks[department]
        
        # Insert data in SQLite db
        try:
            conn = sqlite3.connect('employee_data.db')
            cur = conn.cursor()

            if self.employee_id is not None:
                cur.execute('''
                UPDATE employees
                SET name = ?, start_date = ?, title = ?, department = ?, cell_phone_provided = ?
                WHERE id = ?
                ''', (name, start_date, title, department, cell_phone == "Yes", self.employee_id))
                self.employee_id = None
            else:
                cur.execute('''
                        INSERT INTO employees (name, start_date, title, department, cell_phone_provided)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, start_date, title, department, cell_phone == "Yes"))


            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")
        finally:
            conn.close()

        self.clear_fields()
        self.refresh_employee_list()

        create_interactive_pdf(name, start_date, title, department, cell_phone, tasks)

# PDF class creation with Helvetica font
class PDF(FPDF):
    def checkbox(self, name, x, y, size=10):
        self.set_xy(x, y)
        self.cell(size, size, "", border=1)
        self.set_font('Helvetica', 'B', 12)
        self.cell(size + 2, size, name)

def create_interactive_pdf(name, start_date, title, department, cell_phone, tasks):
    pdf = PDF()
    pdf.add_page()

    # Set title
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, f'Onboarding Checklist for {name}', 0, 1)

    # Add employee details
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 10, f'Start Date: {start_date}', 0, 1)
    pdf.cell(0, 10, f'Title: {title}', 0, 1)
    pdf.cell(0, 10, f'Department: {department}', 0, 1)
    pdf.cell(0, 10, f'Company Cell Phone Provided: {cell_phone}', 0, 1)

    # Add tasks with checkboxes
    pdf.set_font('Helvetica', '', 12)
    y = 60  # Starting Y position for checkboxes
    for task in tasks:
        pdf.checkbox(task, 10, y)
        y += 15

    # Save PDF
    filename = f"Onboarding_Checklist_{name.replace(' ', '_')}.pdf"
    pdf.output(filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
