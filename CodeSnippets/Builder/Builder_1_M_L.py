class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class EmployeeBuilder:
    def __init__(self):
        self.employee = None
    
    def set_name(self, name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        self.employee.name = name
        return self
    
    def set_age(self, age):
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        self.employee.age = age
        return self
    
    def build(self):
        if self.employee is None:
            raise ValueError("Employee cannot be built without name and age")
        return self.employee

# Usage example in a main section
def main():
    employee_builder = EmployeeBuilder()
    employee_builder.set_name("John Doe").set_age(30).build()

if __name__ == "__main__":
    main()