class Car():
    def __init__(self, init_color, init_brand):
        """
        Constructor for Car class
        """
        self.color = init_color
        self.brand = init_brand

    def __str__(self):
        """
        Overriding the __str__ method
        """
        return f"A {self.color} car made by {self.brand}."


# Use the class default constructor
car_instance_a = Car("Blue", "Volkswagen")

# print() invokes __str__()
print(f"print(car_instance_a): {car_instance_a}")

# str() also invokes __str__()
str_a = str(car_instance_a)
print(f"str(car_instance_a): {str_a}")
