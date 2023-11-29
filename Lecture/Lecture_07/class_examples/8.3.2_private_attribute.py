class Car():
    # Class attribute
    fuel = "gas"

    def __init__(self, init_color, init_brand):
        # Instance attributes
        self.color = init_color
        self.brand = init_brand

        # Private instance attributes
        self.__capacity = 4

    def set_capacity(self, new_val):
        if new_val < 0:
            new_val = 0

        self.__capacity = new_val

    def get_capacity(self):
        return self.__capacity

    def honk(self):
        print("HONK")


car_instance_a = Car("Blue", "Volkswagen")

# Best practice
car_instance_a.set_capacity(10)
print("1. car_instance_a.capacity: ", car_instance_a.get_capacity())
# print("2. car_instance_a.capacity: ", car_instance_a.__capacity)

# Best practice
car_instance_a.set_capacity(-1)
print("3. car_instance_a.capacity: ", car_instance_a.get_capacity())

# Will run, but not a good practice
car_instance_a.__capacity = -1
print("4. car_instance_a.capacity: ", car_instance_a.__capacity)
print("5. car_instance_a.capacity: ", car_instance_a.get_capacity())
