class Student(object):

    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def printstudent(self):
        print(f'{self.name} is {self.age} years old, and is in grade {self.grade}')

student1 = Student("Henning", 16, 2)
student2 = Student("Nicolas", 17, 2)
student3 = Student("Olaf", 16, 2)
student1.printstudent()
student2.printstudent()
student3.printstudent()
