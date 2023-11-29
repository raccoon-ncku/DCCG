class Car():
    # Class attribute
    fuel = "gasoline"

    def __init__(self, init_color, init_brand):
        """
        constructor for Car class
        """
        self.color = init_color
        self.brand = init_brand

        # Private instance attributes
        self._capacity = 4

    def set_capacity(self, new_val):
        """
        A setter method for the private attribute _capacity
        """
        
        # validate the new value before setting it
        if new_val < 0:
            new_val = 0

        self._capacity = new_val

    def get_capacity(self):
        """
        A getter method for the private attribute _capacity
        """
        return self._capacity


car_instance_a = Car("Blue", "Volkswagen")

# Best practice
car_instance_a.set_capacity(10)
print("1. car_instance_a.capacity: ", car_instance_a.get_capacity())

# Best practice
car_instance_a.set_capacity(-1)
print("2. car_instance_a.capacity: ", car_instance_a.get_capacity())

# Will run, but not a good practice
car_instance_a._capacity = -1
print("3. car_instance_a.capacity: ", car_instance_a._capacity)
print("4. car_instance_a.capacity: ", car_instance_a.get_capacity())
