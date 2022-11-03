class Car():
    def __init__(self, init_color, init_brand):
        # Attributes
        self.color = init_color
        self.brand = init_brand
        self.capacity = 4

    def __add__(self, other):
        return self.capacity + other.capacity

    def honk(self):
        print("HONK")


car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = Car("White", "Volkswagen")
a = car_instance_a + car_instance_b
print(a)
