import json

EMPLOYEE_FILE = "data/employees.json"

def load_employees():
    with open(EMPLOYEE_FILE, "r") as f:
        return json.load(f)

def get_employee(emp_id: str):
    employees = load_employees()
    return employees.get(emp_id)
