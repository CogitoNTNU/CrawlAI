import numpy
import pygame


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}"

class Rectangle:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.poPoints = numpy.array([   
                                        numpy.array([x,y]),
                                        numpy.array([x+self.height,y]),
                                        numpy.array([x+self.height,y+self.width]),
                                        numpy.array([x, y+self.width])
                                    ])

    #Linear algebra method to check if a point is inside a rectangle
    def contains(self, point):
        for i in range(4):
            x1 = self.poPoints[i][0]
            y1 = self.poPoints[i][1]
            x2 = self.poPoints[(i + 1) % 4][0]
            y2 = self.poPoints[(i + 1) % 4][1]
            xp = point.x
            yp = point.y
            # Cross product
            crossProduct = (yp - y1) * (x2 - x1) - (xp - x1) * (y2 - y1)
            if crossProduct < 0:
                return False
        return True

    def intersects(self, range):
        return not (range.x > self.x + self.width or range.x + range.width < self.x or range.y > self.y + self.height or range.y + range.height < self.y)

    def __str__(self):
        return f"X: {self.x}, Y: {self.y}, Width: {self.width}, Height: {self.height}"
    
    def render(self, window):
        pygame.draw.polygon(window, (255, 255, 255), ((self.poPoints[0][0], self.poPoints[0][1]), (self.poPoints[1][0], self.poPoints[0][1]), (self.poPoints[2][0], self.poPoints[2][1]), (self.poPoints[3][0], self.poPoints[3][1])))

    def updatePosition(self, x, y):
        self.poPointsx += x
        self.poPointsy += y

def rectangle_factory(x, y, width, height) -> Rectangle:
    """
    Factory function for creating a rectangle object.
    """
    return Rectangle(x, y, width, height)