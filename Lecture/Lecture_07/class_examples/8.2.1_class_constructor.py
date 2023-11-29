class Car():
    """
    A class to represent a car.
    """
    def __init__(self, init_color, init_brand):
        """
        Constructor for the Car class.
        Sets the color and brand of the car.
        `self` is a reference to the object itself.
        """
        # instance attributes
        self.color = init_color
        self.brand = init_brand

    def honk(self):
        print("HONK")
        print(f"A {self.color} car made by {self.brand}.")


# Use the class default constructor
car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = Car("White", "Renault")

# use dot operator to access attributes and methods
print(car_instance_a.brand)
print(car_instance_b.color)
car_instance_a.honk()
car_instance_b.honk()

print(car_instance_a)
