class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, name):
        first, last = name.split(" ", 1)
        self.first_name = first
        self.last_name = last

    @full_name.deleter
    def full_name(self):
        print("Удаление имени...")
        self.first_name = None
        self.last_name = None


person = Person("Vanya", "Drago")

print(person.full_name)

person.full_name = "Ivan Killer"
print(person.full_name)

del person.full_name
print(person.full_name)
