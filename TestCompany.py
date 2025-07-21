from Company import Company
from Employee import Employee


# Create a company
company = Company("Acme Inc.")

# Add users to the company
company.addEmployee(Employee("John", "2000-01-01"))
company.addEmployee(Employee("Jane", "2003-04-01"))
company.addEmployee(Employee("Jim", "1990-03-01"))
company.addEmployee(Employee("Alex", "2006-11-13"))
company.addEmployee(Employee("Laura", "2009-07-05"))

# Example usage
company.printEmployees()

