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


class ElecctricCar(Car):
    fuel = "electricity"

    def __init__(self, init_color, init_brand):
        super().__init__(init_color, init_brand)
        self.charger = "Type 2"


car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = ElecctricCar("White", "Tesla")

print(car_instance_a.fuel)
print(car_instance_b.fuel)  # Overridden attribute
print(car_instance_b.charger)  # New attribute

car_instance_a.honk()
car_instance_b.honk()  # Inherited method
