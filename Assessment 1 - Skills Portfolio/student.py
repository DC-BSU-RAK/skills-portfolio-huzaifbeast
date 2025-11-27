import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Student data from file
def load_students():
    students = []
    try:
        file = open("resources/studentMarks.txt", "r")
        lines = file.readlines()
        
        num_students = int(lines[0].strip())
        
        for i in range(1, num_students + 1):
            line = lines[i].strip()
            parts = line.split(",")
            
            student = {
                "number": parts[0],
                "name": parts[1],
                "coursework1": int(parts[2]),
                "coursework2": int(parts[3]),
                "coursework3": int(parts[4]),
                "exam": int(parts[5])
            }
            students.append(student)
        
        file.close()
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt file not found!")
    return students

# Save students to file
def save_students():
    try:
        file = open("resources/studentMarks.txt", "w")
        file.write(f"{len(students)}\n")
        
        for student in students:
            line = f"{student['number']},{student['name']},{student['coursework1']},{student['coursework2']},{student['coursework3']},{student['exam']}\n"
            file.write(line)
        
        file.close()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save: {str(e)}")
        return False

# Calculating total coursework mark
def get_coursework_total(student):
    return student["coursework1"] + student["coursework2"] + student["coursework3"]

# To find overall percentage
def get_percentage(student):
    total = get_coursework_total(student) + student["exam"]
    return (total / 160) * 100

# To give percentage overall
def get_grade(percentage):
    if percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"

# Student info for display
def format_student(student):
    coursework = get_coursework_total(student)
    percentage = get_percentage(student)
    grade = get_grade(percentage)
    
    info = f"Name: {student['name']}\n"
    info += f"Student Number: {student['number']}\n"
    info += f"Total Coursework: {coursework}/60\n"
    info += f"Exam Mark: {student['exam']}/100\n"
    info += f"Overall Percentage: {percentage:.2f}%\n"
    info += f"Grade: {grade}\n"
    
    return info

# Show all students
def view_all_students():
    output = "▄︻デ══━一💥 ALL STUDENT RECORDS ▄︻デ══━一💥\n\n"
    
    total_percentage = 0
    for student in students:
        output += format_student(student)
        output += "-" * 40 + "\n"
        total_percentage += get_percentage(student)
    
    if len(students) > 0:
        average = total_percentage / len(students)
        output += f"\nTotal Students: {len(students)}\n"
        output += f"Average Percentage: {average:.2f}%"
    else:
        output += "\nNo students in the system."
    
    result_text.delete(1.0, tk.END)
    result_text.insert(1.0, output)

# For individual student
def view_individual_student():
    search = search_entry.get().strip()
    
    if not search:
        messagebox.showwarning("Input Required", "Please enter a student name or number!")
        return
    
    found = None
    for student in students:
        if search.lower() in student["name"].lower() or search == student["number"]:
            found = student
            break
    
    if found:
        output = "🌟 STUDENT RECORD 🌟\n\n"
        output += format_student(found)
        result_text.delete(1.0, tk.END)
        result_text.insert(1.0, output)
    else:
        messagebox.showerror("Not Found", "Student not found!")

# Show highest scoring student
def show_highest_student():
    if len(students) == 0:
        messagebox.showwarning("No Data", "No students in the system!")
        return
    
    highest = students[0]
    highest_percentage = get_percentage(highest)
    
    for student in students:
        percentage = get_percentage(student)
        if percentage > highest_percentage:
            highest = student
            highest_percentage = percentage
    
    output = "🌟 HIGHEST SCORING STUDENT 🌟\n\n"
    output += format_student(highest)
    
    result_text.delete(1.0, tk.END)
    result_text.insert(1.0, output)

# Show lowest scoring student
def show_lowest_student():
    if len(students) == 0:
        messagebox.showwarning("No Data", "No students in the system!")
        return
    
    lowest = students[0]
    lowest_percentage = get_percentage(lowest)
    
    for student in students:
        percentage = get_percentage(student)
        if percentage < lowest_percentage:
            lowest = student
            lowest_percentage = percentage
    
    output = "📉 LOWEST SCORING STUDENT 📉\n\n"
    output += format_student(lowest)
    
    result_text.delete(1.0, tk.END)
    result_text.insert(1.0, output)

# Sort student records
def sort_students():
    sort_window = tk.Toplevel(window)
    sort_window.title("Sort Students")
    sort_window.geometry("300x150")
    sort_window.config(bg="#f0f0f0")
    
    tk.Label(sort_window, text="Sort Order:", font=("Arial", 12), bg="#f0f0f0").pack(pady=20)
    
    def sort_ascending():
        students.sort(key=lambda s: get_percentage(s))
        save_students()
        view_all_students()
        sort_window.destroy()
        messagebox.showinfo("Success", "Students sorted in ascending order!")
    
    def sort_descending():
        students.sort(key=lambda s: get_percentage(s), reverse=True)
        save_students()
        view_all_students()
        sort_window.destroy()
        messagebox.showinfo("Success", "Students sorted in descending order!")
    
    tk.Button(sort_window, text="Ascending", command=sort_ascending, 
              width=15, bg="#4CAF50", fg="white").pack(pady=5)
    tk.Button(sort_window, text="Descending", command=sort_descending, 
              width=15, bg="#2196F3", fg="white").pack(pady=5)

# Add student record
def add_student():
    add_window = tk.Toplevel(window)
    add_window.title("Add Student")
    add_window.geometry("400x350")
    add_window.config(bg="#f0f0f0")
    
    tk.Label(add_window, text="Add New Student", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # Input fields
    fields_frame = tk.Frame(add_window, bg="#f0f0f0")
    fields_frame.pack(pady=10)
    
    tk.Label(fields_frame, text="Student Number:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
    number_entry = tk.Entry(fields_frame, width=20)
    number_entry.grid(row=0, column=1, pady=5)
    
    tk.Label(fields_frame, text="Student Name:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(fields_frame, width=20)
    name_entry.grid(row=1, column=1, pady=5)
    
    tk.Label(fields_frame, text="Coursework 1 (0-20):", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
    cw1_entry = tk.Entry(fields_frame, width=20)
    cw1_entry.grid(row=2, column=1, pady=5)
    
    tk.Label(fields_frame, text="Coursework 2 (0-20):", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
    cw2_entry = tk.Entry(fields_frame, width=20)
    cw2_entry.grid(row=3, column=1, pady=5)
    
    tk.Label(fields_frame, text="Coursework 3 (0-20):", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
    cw3_entry = tk.Entry(fields_frame, width=20)
    cw3_entry.grid(row=4, column=1, pady=5)
    
    tk.Label(fields_frame, text="Exam Mark (0-100):", bg="#f0f0f0").grid(row=5, column=0, sticky="w", pady=5)
    exam_entry = tk.Entry(fields_frame, width=20)
    exam_entry.grid(row=5, column=1, pady=5)
    
    def save_new_student():
        try:
            number = number_entry.get().strip()
            name = name_entry.get().strip()
            cw1 = int(cw1_entry.get())
            cw2 = int(cw2_entry.get())
            cw3 = int(cw3_entry.get())
            exam = int(exam_entry.get())
            
            # Validation
            if not number or not name:
                messagebox.showerror("Error", "Student number and name are required!")
                return
            
            if not (1000 <= int(number) <= 9999):
                messagebox.showerror("Error", "Student number must be between 1000 and 9999!")
                return
            
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                return
            
            #  To check for duplicate student number
            for student in students:
                if student["number"] == number:
                    messagebox.showerror("Error", "Student number already exists!")
                    return
            
            new_student = {
                "number": number,
                "name": name,
                "coursework1": cw1,
                "coursework2": cw2,
                "coursework3": cw3,
                "exam": exam
            }
            
            students.append(new_student)
            if save_students():
                messagebox.showinfo("Success", "Student added successfully!")
                add_window.destroy()
                view_all_students()
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for marks!")
    
    tk.Button(add_window, text="Save Student", command=save_new_student, 
              bg="#4CAF50", fg="white", width=15).pack(pady=10)

# Delete student record
def delete_student():
    search = simpledialog.askstring("Delete Student", "Enter student name or number to delete:")
    
    if not search:
        return
    
    found_index = -1
    found_student = None
    
    for i, student in enumerate(students):
        if search.lower() in student["name"].lower() or search == student["number"]:
            found_index = i
            found_student = student
            break
    
    if found_student:
        confirm = messagebox.askyesno("Confirm Delete", 
                                      f"Are you sure you want to delete:\n\n{found_student['name']} ({found_student['number']})?")
        
        if confirm:
            students.pop(found_index)
            if save_students():
                messagebox.showinfo("Success", "Student deleted successfully!")
                view_all_students()
    else:
        messagebox.showerror("Not Found", "Student not found!")

# Update student record
def update_student():
    search = simpledialog.askstring("Update Student", "Enter student name or number to update:")
    
    if not search:
        return
    
    found_student = None
    
    for student in students:
        if search.lower() in student["name"].lower() or search == student["number"]:
            found_student = student
            break
    
    if not found_student:
        messagebox.showerror("Not Found", "Student not found!")
        return
    
    # Update window
    update_window = tk.Toplevel(window)
    update_window.title("Update Student")
    update_window.geometry("400x350")
    update_window.config(bg="#f0f0f0")
    
    tk.Label(update_window, text=f"Update: {found_student['name']}", 
             font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
    
    # Input fields with current values
    fields_frame = tk.Frame(update_window, bg="#f0f0f0")
    fields_frame.pack(pady=10)
    
    tk.Label(fields_frame, text="Student Number:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
    number_entry = tk.Entry(fields_frame, width=20)
    number_entry.insert(0, found_student["number"])
    number_entry.grid(row=0, column=1, pady=5)
    
    tk.Label(fields_frame, text="Student Name:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(fields_frame, width=20)
    name_entry.insert(0, found_student["name"])
    name_entry.grid(row=1, column=1, pady=5)
    
    tk.Label(fields_frame, text="Coursework 1 (0-20):", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
    cw1_entry = tk.Entry(fields_frame, width=20)
    cw1_entry.insert(0, str(found_student["coursework1"]))
    cw1_entry.grid(row=2, column=1, pady=5)
    
    tk.Label(fields_frame, text="Coursework 2 (0-20):", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
    cw2_entry = tk.Entry(fields_frame, width=20)
    cw2_entry.insert(0, str(found_student["coursework2"]))
    cw2_entry.grid(row=3, column=1, pady=5)
    
    tk.Label(fields_frame, text="Coursework 3 (0-20):", bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=5)
    cw3_entry = tk.Entry(fields_frame, width=20)
    cw3_entry.insert(0, str(found_student["coursework3"]))
    cw3_entry.grid(row=4, column=1, pady=5)
    
    tk.Label(fields_frame, text="Exam Mark (0-100):", bg="#f0f0f0").grid(row=5, column=0, sticky="w", pady=5)
    exam_entry = tk.Entry(fields_frame, width=20)
    exam_entry.insert(0, str(found_student["exam"]))
    exam_entry.grid(row=5, column=1, pady=5)
    
    def save_updates():
        try:
            number = number_entry.get().strip()
            name = name_entry.get().strip()
            cw1 = int(cw1_entry.get())
            cw2 = int(cw2_entry.get())
            cw3 = int(cw3_entry.get())
            exam = int(exam_entry.get())
            
            # Validation
            if not number or not name:
                messagebox.showerror("Error", "Student number and name are required!")
                return
            
            if not (1000 <= int(number) <= 9999):
                messagebox.showerror("Error", "Student number must be between 1000 and 9999!")
                return
            
            if not (0 <= cw1 <= 20 and 0 <= cw2 <= 20 and 0 <= cw3 <= 20):
                messagebox.showerror("Error", "Coursework marks must be between 0 and 20!")
                return
            
            if not (0 <= exam <= 100):
                messagebox.showerror("Error", "Exam mark must be between 0 and 100!")
                return
            
            # Check for duplicate student number (if changed)
            if number != found_student["number"]:
                for student in students:
                    if student["number"] == number:
                        messagebox.showerror("Error", "Student number already exists!")
                        return
            
            # Update student
            found_student["number"] = number
            found_student["name"] = name
            found_student["coursework1"] = cw1
            found_student["coursework2"] = cw2
            found_student["coursework3"] = cw3
            found_student["exam"] = exam
            
            if save_students():
                messagebox.showinfo("Success", "Student updated successfully!")
                update_window.destroy()
                view_all_students()
        
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for marks!")
    
    tk.Button(update_window, text="Save Changes", command=save_updates, 
              bg="#4CAF50", fg="white", width=15).pack(pady=10)

# Load all students
students = load_students()

# Create main window 
window = tk.Tk()
window.title("Student Results Manager - Extended")
window.geometry("800x700")
window.config(bg="#f0f0f0")

# Title
title = tk.Label(window, text="Student Results Manager", font=("Arial", 20, "bold"), bg="#f0f0f0")
title.pack(pady=15)

# Menu buttons frame
menu_frame = tk.Frame(window, bg="#f0f0f0")
menu_frame.pack(pady=10)

# Row 1
btn1 = tk.Button(menu_frame, text="View All Students", command=view_all_students, 
                 width=18, height=2, bg="#4CAF50", fg="white", font=("Arial", 9))
btn1.grid(row=0, column=0, padx=5, pady=5)

btn3 = tk.Button(menu_frame, text="Highest Score", command=show_highest_student, 
                 width=18, height=2, bg="#2196F3", fg="white", font=("Arial", 9))
btn3.grid(row=0, column=1, padx=5, pady=5)

btn4 = tk.Button(menu_frame, text="Lowest Score", command=show_lowest_student, 
                 width=18, height=2, bg="#FF9800", fg="white", font=("Arial", 9))
btn4.grid(row=0, column=2, padx=5, pady=5)

# Row 2 
btn5 = tk.Button(menu_frame, text="Sort Students", command=sort_students, 
                 width=18, height=2, bg="#9C27B0", fg="white", font=("Arial", 9))
btn5.grid(row=1, column=0, padx=5, pady=5)

btn6 = tk.Button(menu_frame, text="Add Student", command=add_student, 
                 width=18, height=2, bg="#00BCD4", fg="white", font=("Arial", 9))
btn6.grid(row=1, column=1, padx=5, pady=5)

btn7 = tk.Button(menu_frame, text="Delete Student", command=delete_student, 
                 width=18, height=2, bg="#FF5722", fg="white", font=("Arial", 9))
btn7.grid(row=1, column=2, padx=5, pady=5)

# Row 3
btn8 = tk.Button(menu_frame, text="Update Student", command=update_student, 
                 width=18, height=2, bg="#795548", fg="white", font=("Arial", 9))
btn8.grid(row=2, column=0, padx=5, pady=5)

quit_btn = tk.Button(menu_frame, text="Quit", command=window.quit, 
                     width=18, height=2, bg="#f44336", fg="white", font=("Arial", 9))
quit_btn.grid(row=2, column=1, padx=5, pady=5)

# Search frame for individual student
search_frame = tk.Frame(window, bg="#f0f0f0")
search_frame.pack(pady=10)

search_label = tk.Label(search_frame, text="Search Student (Name or Number):", 
                       font=("Arial", 10), bg="#f0f0f0")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(search_frame, font=("Arial", 10), width=25)
search_entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(search_frame, text="Search", command=view_individual_student, 
                      bg="#9C27B0", fg="white", font=("Arial", 10))
search_btn.pack(side=tk.LEFT, padx=5)

# Result text area
result_frame = tk.Frame(window, bg="#f0f0f0")
result_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(result_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, font=("Courier", 10), wrap=tk.WORD, 
                     yscrollcommand=scrollbar.set)
result_text.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=result_text.yview)

#  To start the app
window.mainloop()