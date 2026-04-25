import math

def pymath():

    class mathbase:
        def area():
            return 0
        
        def perimeter():
            return 0

    class triangle(mathbase):
        def __init__(self, side_a, side_b, angle):
            # trianle sides and angle between them
            self.side_a = side_a
            self.side_b = side_b
            self.angle = angle

    
        def perimeter(self):
            side_c = math.sqrt(self.side_a ** 2 + self.side_b ** 2 - math.cos(self.angle))
            return side_c

        def area(self):
            return (self.a * self.b) /2 * math.sin(self.ac)

    class rectangle(mathbase):
        def __init__(self, side_a, side_b):
            self.side_a = side_a
            self.side_b = side_b

        def perimeter(self):
            return self.side_a * 2 + self.side_b * 2

        def area(self):
            return self.side_a * self.side_b
        
    class circle(mathbase):
        def __init__(self, radius):
            self.radius = radius

        def perimeter(self):
            return 2 * 3.14 * self.radius
        def area(self):
            return 3.14 * self.radius ** 2
pymath()
