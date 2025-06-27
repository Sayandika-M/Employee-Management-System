import json
import re
import random
import datetime
import string
import sys
import time

EMPLOYEE_DB = "employees.json"

def load_employees():
    try:
        with open(EMPLOYEE_DB, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_employees(employees):
    with open(EMPLOYEE_DB, "w") as file:
        json.dump(employees, file, indent=4)

class Employee:

    def __init__(self):
        self.employees = load_employees()

    def register(self):
        name = input("Enter Full Name: ")
        mobile = self.validate_mobile()
        email = self.validate_email()
        department, role = self.select_department()
        emp_id = self.generate_emp_id(name, department)
        password = self.generate_password()

        self.employees = load_employees()
        self.employees[emp_id] = {
            "name": name,
            "mobile": mobile,
            "email": email,
            "department": department,
            "role": role,
            "password": password,
            "attendance": random.randint(70, 100),
            "salary": random.randint(30000, 60000)
        }

        save_employees(self.employees)
        self.loading("Registering")

        print(f"Registration Successful!\nEmployee ID: {emp_id}\nPassword: {password}")

    def login(self):
        self.employees = load_employees()
        emp_id = input("Enter Employee ID: ")
        password = input("Enter Password: ")

        if emp_id in self.employees and self.employees[emp_id]["password"] == password:
            print("Login Successful!")
            self.dashboard(emp_id)
        else:
            print("Invalid credentials!")

    def dashboard(self, emp_id):
        while True:
            print("\nDashboard Menu")
            print("1. View Profile")
            print("2. Edit Profile")
            print("3. View Attendance")
            print("4. View Salary")
            print("5. Change Password")
            print("6. Logout")

            choice = input("Select an option: ")

            if choice == "1":
                self.view_profile(emp_id)
            elif choice == "2":
                self.edit_profile(emp_id)
            elif choice == "3":
                self.view_attendance(emp_id)
            elif choice == "4":
                self.view_salary(emp_id)
            elif choice == "5":
                self.change_password(emp_id)
            elif choice == "6":
                print("Logged out successfully!")
                break
            else:
                print("Invalid choice.")

    def view_profile(self, emp_id):
        emp = self.employees[emp_id]
        print(f"Name: {emp['name']}\nMobile: {emp['mobile']}\nEmail: {emp['email']}\nDepartment: {emp['department']}\nRole: {emp['role']}")

    def edit_profile(self, emp_id):
        emp = self.employees[emp_id]
        emp["name"] = input(f"Name [{emp['name']}]: ") or emp["name"]
        emp["mobile"] = input(f"Mobile [{emp['mobile']}]: ") or emp["mobile"]
        emp["email"] = input(f"Email [{emp['email']}]: ") or emp["email"]
        save_employees(self.employees)
        print("Profile updated!")

    def view_attendance(self, emp_id):
        print(f"Attendance: {self.employees[emp_id]['attendance']}%")

    def view_salary(self, emp_id):
        print(f"Monthly Salary: ₹{self.employees[emp_id]['salary']}")

    def change_password(self, emp_id):
        current = input("Enter Current Password: ")
        if current == self.employees[emp_id]['password']:
            new = input("New Password: ")
            confirm = input("Confirm Password: ")
            if new == confirm:
                self.employees[emp_id]['password'] = new
                save_employees(self.employees)
                print("Password changed!")
            else:
                print("Passwords don't match.")
        else:
            print("Incorrect current password.")

    def validate_mobile(self):
        while True:
            mobile = input("Mobile Number (10 digits): ")
            if re.fullmatch(r"\d{10}", mobile):
                return mobile
            print("Invalid mobile number!")

    def validate_email(self):
        while True:
            email = input("Email: ")
            if re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z]+\.[A-Za-z]{2,}", email):
                return email
            print("Invalid email!")

    def select_department(self):
        departments = {
            1: ("HR", "HR Executive"),
            2: ("IT", "Software Developer"),
            3: ("Finance", "Accountant"),
            4: ("Marketing", "SEO Analyst"),
            5: ("Support", "Customer Executive")
        }
        print("\nDepartments:")
        for k, v in departments.items():
            print(f"{k}. {v[0]} - {v[1]}")

        while True:
            try:
                choice = int(input("Choose department number: "))
                if choice in departments:
                    return departments[choice]
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Enter a number!")

    def generate_emp_id(self, name, dept_code):
        year = datetime.datetime.now().year % 100
        unique = random.randint(1000, 9999)
        return f"{name[:3].upper()}{dept_code[:2].upper()}{year}{unique}"

    def generate_password(self, length=8):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def loading(self, message="Loading"):
        symbols = ['|', '/', '-', '\\']
        for _ in range(10):
            for s in symbols:
                sys.stdout.write(f"\r{message} {s}")
                sys.stdout.flush()
                time.sleep(0.1)
        sys.stdout.write("\rDone!\n")
        sys.stdout.flush()

def main():
    emp = Employee()
    while True:
        print("\nEmployee Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        option = input("Select option: ")

        if option == "1":
            emp.register()
        elif option == "2":
            emp.login()
        elif option == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()

