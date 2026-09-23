class Car():
    # Class attribute
    fuel = "gasoline"

    def __init__(self, init_color, init_brand):
        """
        constructor for Car class
        """
        self.color = init_color
        self.brand = init_brand
        self.capacity = 4


car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = Car("White", "Volkswagen")

# Overriding the instance attribute
car_instance_a.capacity = 6

print(f"car_instance_a.capacity: {car_instance_a.capacity}")
# Class attributes are shared by all instances of the class
print(f"car_instance_a.fuel: {car_instance_a.fuel}")

print(f"car_instance_b.capacity: {car_instance_b.capacity}")
print(f"car_instance_b.fuel: {car_instance_b.fuel}")

# Class attributes can be accessed via the class name
print(f"Car.fuel: {Car.fuel}")
# Instance attributes cannot be accessed via the class name
# print(f"Car.capacity: {Car.capacity}")  # This will cause an error