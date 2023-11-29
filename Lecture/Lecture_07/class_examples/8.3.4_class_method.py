import datetime


class Customer():

    email_promotion = False

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return "Customer Data: {}, age {}".format(self.name, self.age)

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
print(c1.email_promotion)
print(c2.email_promotion)
Customer.start_email_promotion()
print(c1.email_promotion)
print(c2.email_promotion)

# Staticmethod as utilities
print(Customer.calc_age(2001))
