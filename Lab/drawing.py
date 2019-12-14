"""
Turtle Implementation
"""

import math
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image


class Pen:
    """A class that implements simple turtle-style graphics."""

    Scale = 10
    TurtleIcon = Image.open(Path(__file__).parent / "turtle.png")
    TurtleScale = 10

    class stroke:
        """A line pen segment with attributes."""

        def __init__(self, origin, prev=None):
            self.points = [origin]
            if prev is None:
                self.color = "blue"
                self.width = 1
            else:
                self.color = prev.color
                self.width = prev.width

    def __init__(self):
        self.current = (0, 0)
        self.heading = math.pi / 2
        self.strokes = [Pen.stroke(self.current)]
        self.pendown = True

    def draw(self, distance):
        """Move the pen by distance."""
        self.current = (self.current[0] + math.cos(self.heading) * distance * Pen.Scale,
                        self.current[1] + math.sin(self.heading) * distance * Pen.Scale)
        if self.pendown:
            self.strokes[-1].points.append(self.current)

    def turn(self, degrees):
        """Turn the pen by degrees"""
        self.heading = (self.heading + math.radians(degrees)) % (math.pi * 2)

    def goto(self, x, y):
        """Goto a point in the coordinate space."""
        self.current = (x * Pen.Scale, y * Pen.Scale)
        if self.pendown:
            self.strokes[-1].points.append(self.current)

    def heading(self, heading):
        """Set the pen to face heading."""
        self.heading = math.radians(heading)

    def up(self):
        """Pick the pen up. Movements won't make lines."""
        self.pendown = False

    def down(self):
        """Put the pen down. Movements will make lines."""
        self.strokes.append(Pen.stroke(self.current, self.strokes[-1]))
        self.pendown = True

    def color(self, color):
        """Set the pen color."""
        self.strokes.append(Pen.stroke(self.current, self.strokes[-1]))
        self.strokes[-1].color = color

    def width(self, width):
        """Set the line thickness."""
        self.strokes.append(Pen.stroke(self.current, self.strokes[-1]))
        self.strokes[-1].width = width

    def show(self, turtle=True, size=(8, 8)):
        """Show the current drawing."""
        plt.rcParams['figure.figsize'] = size

        plt.clf()
        plt.cla()
        plt.axis(False)

        cax = plt.gca()
        for stroke in self.strokes:
            cax.add_line(plt.Polygon(
                stroke.points, color=stroke.color,
                closed=None, fill=None, linewidth=stroke.width)
            )

        plt.axis('scaled')

        if turtle:
            xmin, xmax, ymin, ymax = plt.axis()
            xsize = xmax - xmin
            ysize = ymax - ymin
            turtlesize = max(xsize, ysize) / Pen.TurtleScale / 2
            turtle = Pen.TurtleIcon.rotate(math.degrees(self.heading - math.pi / 2))
            extent = (self.current[0] - turtlesize,
                      self.current[0] + turtlesize,
                      self.current[1] - turtlesize,
                      self.current[1] + turtlesize)
            plt.imshow(turtle, extent=extent)
            plt.axis('scaled')

        plt.show()
        self.__init__()


pen = Pen()
