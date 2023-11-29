class Car():
    def __init__(self, init_color, init_brand):
        """
        constructor for Car class
        """
        self.color = init_color
        self.brand = init_brand

        # Private instance attributes
        self.__capacity = 4

    @property
    def capacity(self):
        """
        A getter method for the private attribute __capacity
        """
        return self.__capacity
    
    @capacity.setter
    def capacity(self, new_val):
        """
        A setter method for the private attribute __capacity
        """
        if new_val < 0:
            new_val = 0

        self.__capacity = new_val


car = Car("Blue", "Volkswagen")

# Best practice
car.capacity = 10
print("1. car.capacity: ", car.capacity)

# Best practice
car.capacity = -1
print("4. car.capacity: ", car.capacity)

# Will run, but not a good practice
car.__capacity = -1
print("3. car.capacity: ", car.capacity)
print("4. car.__capacity: ", car.__capacity)