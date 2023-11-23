class Car():
    def __init__(self, init_color, init_brand):
        # Instance attributes
        self.color = init_color
        self.brand = init_brand
        self.capacity = 4

    def honk(self):
        print("HONK")


class Jet():
    def __init__(self, init_model, init_airline):
        # Instance attributes
        self.model = init_model
        self.airline = init_airline
        self.capacity = 4

    def honk(self):
        print("AIRPLANE HONK")


car_a = Car("sapphire blue", "Chevrolet")
jet_b = Jet("Gulfstream", "EasyJet")

vehicles = [car_a, jet_b]
for vehicle in vehicles:
    vehicle.honk()
