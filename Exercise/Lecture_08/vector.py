class Vector2D():
    name = "Vector2D"

    def __init__(self, x=0, y=0):
        """
        Constructor
        """
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector2D({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector2D(
            self.x + other.x,
            self.y + other.y
        )
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y

vec_a = Vector2D(2)
vec_b = Vector2D(3, 4.0)
print(vec_a.dot(vec_b))
print(vec_a.name)

import compas.geometry as cg
cg_vec_a = cg.Vector(2,0,0)
cg_vec_b = cg.Vector(3,4,0)

print(cg_vec_a.dot(cg_vec_b))