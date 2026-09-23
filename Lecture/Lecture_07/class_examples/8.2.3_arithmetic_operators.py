class Car():
    def __init__(self, init_color, init_brand):
        """
        Constructor for Car class
        """
        self.color = init_color
        self.brand = init_brand
        self.capacity = 4  # Default capacity

    def __add__(self, other):
        """
        Adding the capacity of two cars
        """
        return self.capacity + other.capacity


car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = Car("White", "Volkswagen")

add_result = car_instance_a + car_instance_b
print(f"add_result: {add_result}")
