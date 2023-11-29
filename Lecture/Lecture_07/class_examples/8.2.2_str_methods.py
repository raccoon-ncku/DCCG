class Car():

    def __init__(self, init_color, init_brand):
        # Attributes
        self.color = init_color
        self.brand = init_brand

    def __str__(self):
        return "A car object. Color:{}, Brand: {}".format(self.color, self.brand)

    def honk(self):
        print("HONK")


# Use the class default constructor
car_instance_a = Car("Blue", "Volkswagen")

# invoke __str__ when using print() or str()
print(car_instance_a)

str_a = str(car_instance_a)
print(str_a)
