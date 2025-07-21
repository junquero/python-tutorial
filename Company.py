# A company has a list of users

class Company:
    def __init__(self, name):
        self.name = name
        self.users = []  # List of Employee objects

    def addEmployee(self, user):
        self.users.append(user)

    def printEmployees(self):
        for user in self.users:
            user.print_user()

