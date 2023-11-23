class Car():
    # Class attribute
    fuel = "gas"

    def __init__(self, init_color, init_brand):
        # Instance attributes
        self.color = init_color
        self.brand = init_brand
        self.capacity = 4

    def honk(self):
        print("HONK")


car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = Car("White", "Volkswagen")

car_instance_a.capacity = 6
car_instance_a.fuel = "electricity"

print(car_instance_a.fuel)
print(car_instance_b.fuel)
print(Car.fuel)

print("car_instance_a.capacity: ", car_instance_a.capacity)
print("car_instance_b.capacity: ", car_instance_b.capacity)
print(Car.capacity)
