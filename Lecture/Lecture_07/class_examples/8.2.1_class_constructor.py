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
        """
        An instance method.
        """
        print("HONK")
        print(f"A {self.color} car made by {self.brand}.")


# Use the class default constructor, __init__()
car_instance_a = Car("Blue", "Volkswagen")
# Pass different arguments to the constructor
car_instance_b = Car("White", "Renault")

# use dot operator to access attributes and methods
print(f"car_instance_a.color: {car_instance_a.color}")
print(f"car_instance_b.brand: {car_instance_b.brand}")

# use dot operator to invoke methods
car_instance_a.honk()
car_instance_b.honk()
