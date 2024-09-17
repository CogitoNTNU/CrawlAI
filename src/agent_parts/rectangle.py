

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return self.x <= point.x <= self.x + self.width and self.y <= point.y <= self.y + self.height

    def intersects(self, range):
        return not (range.x > self.x + self.width or range.x + range.width < self.x or range.y > self.y + self.height or range.y + range.height < self.y)

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, Width: {self.width}, Height: {self.height}"