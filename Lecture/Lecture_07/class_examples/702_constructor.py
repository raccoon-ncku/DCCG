class Car():
    def __init__(self, init_color, init_brand):
        # Attributes
        self.color = init_color
        self.brand = init_brand

    def honk(self):
        print("HONK")
        print("A {} {} car.".format(self.color, self.brand))


# Use the class default constructor
car_instance_a = Car("Blue", "Volkswagen")
car_instance_b = Car("White", "Renault")

# use dot operator to access attributes and methods
print(car_instance_a.brand)
print(car_instance_b.color)
car_instance_a.honk()
car_instance_b.honk()

print(car_instance_a)
