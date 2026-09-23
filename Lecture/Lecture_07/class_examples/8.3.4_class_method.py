import datetime


class Customer():

    email_promotion = False

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"Customer Details: {self.name}, age {self.age}"

    @classmethod
    def from_birthyear(cls, name, b_year):
        age = datetime.datetime.now().year - b_year
        return cls(name, age)

    @classmethod
    def start_email_promotion(cls):
        cls.email_promotion = True

    @staticmethod
    def calc_age(b_year):
        age = datetime.datetime.now().year - b_year
        return age


# Classmethod as a constructor
c1 = Customer("Chris", 25)
c2 = Customer.from_birthyear("Ryan", 1993)

print(c1)
print(c2)

# Classmethod to modify class attribute
print("Before starting email promotion")
print(f"c1.email_promotion: {c1.email_promotion}")
print(f"c2.email_promotion: {c2.email_promotion}")
Customer.start_email_promotion()
print("After starting email promotion")
print(f"c1.email_promotion: {c1.email_promotion}")
print(f"c2.email_promotion: {c2.email_promotion}")  # both c1 and c2 are affected

# Staticmethod as utilities
print(Customer.calc_age(2001))  # not related to any instance
