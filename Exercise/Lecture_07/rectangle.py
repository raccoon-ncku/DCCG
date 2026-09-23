class Rectangle():
    def __init__(self, width, height):
        """
        Constructor of the Rectangle.
        """
        self.width = width
        self.height = height
    
        self.__area = width * height
        self.__perimeter = (width + height) * 2

    @property
    def area(self):
        return self.__area
    
    @property
    def perimeter(self):
        return self.__perimeter
    
    @classmethod
    def from_two_points(cls, p1, p2):
        """
        Create a rectangle from diagnal points.
        """
        width = p2[0] - p1[0]
        height = p2[1] - p1[1]
        return cls(width, height)

rec_1 = Rectangle(5, 10)
print(rec_1.area)
print(rec_1.perimeter)

rec_2 = Rectangle.from_two_points([0,0], [5,10])

print(rec_2.area)
print(rec_2.perimeter)
