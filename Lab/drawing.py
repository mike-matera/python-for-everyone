"""
A simple implementation of turtle graphics for teaching algorithms. 

Author: Mike Matera
"""

import math
from pathlib import Path
import matplotlib.pyplot as plt
from PIL import Image


class Pen:
    """A class that implements simple turtle-style graphics."""

    _Scale = 1
    _TurtleIcon = Image.open(Path(__file__).parent / "turtle.png")
    _TurtleScale = 10

    class _stroke:
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
        self.cur_heading = math.pi / 2
        self.strokes = [Pen._stroke(self.current)]
        self.pendown = True

    def draw(self, distance):
        """Move the pen by distance."""
        self.current = (self.current[0] + math.cos(self.cur_heading) * distance * Pen._Scale,
                        self.current[1] + math.sin(self.cur_heading) * distance * Pen._Scale)
        if self.pendown:
            self.strokes[-1].points.append(self.current)

    def turn(self, degrees):
        """Turn the pen by degrees"""
        self.cur_heading = (self.cur_heading + math.radians(degrees)) % (math.pi * 2)

    def goto(self, x, y):
        """Goto a point in the coordinate space."""
        self.current = (x * Pen._Scale, y * Pen._Scale)
        if self.pendown:
            self.strokes[-1].points.append(self.current)

    def heading(self, heading):
        """Set the pen to face heading."""
        self.cur_heading = math.radians(heading)

    def up(self):
        """Pick the pen up. Movements won't make lines."""
        self.pendown = False

    def down(self):
        """Put the pen down. Movements will make lines."""
        self.strokes.append(Pen._stroke(self.current, self.strokes[-1]))
        self.pendown = True

    def color(self, color):
        """Set the pen color."""
        self.strokes.append(Pen._stroke(self.current, self.strokes[-1]))
        self.strokes[-1].color = color

    def width(self, width):
        """Set the line thickness."""
        self.strokes.append(Pen._stroke(self.current, self.strokes[-1]))
        self.strokes[-1].width = width

    def show(self, turtle=True, arena=(-100, 100, -100, 100), size=(6, 6)):
        """Show the current drawing and reset all drawing state. 
        
        Arguments:

          turtle - (boolean) If True the turle will be visible in the output (default True)
          arena - The coordinate space of the arena: [x_min, x_max, y_min, y_max] 
          size - The size of the drawing in inches: [x_size, y_size]
        """
        plt.rcParams['figure.figsize'] = size

        plt.clf()
        plt.cla()
        plt.axis(False)

        try:
            cax = plt.gca()
            for stroke in self.strokes:
                cax.add_line(plt.Polygon(
                    stroke.points, color=stroke.color,
                    closed=None, fill=None, linewidth=stroke.width)
                )

            plt.axis(arena)

            if turtle:
                xmin, xmax, ymin, ymax = plt.axis()
                xsize = xmax - xmin
                ysize = ymax - ymin
                turtlesize = max(xsize, ysize) / Pen._TurtleScale / 2
                turtle = Pen._TurtleIcon.rotate(math.degrees(self.cur_heading - math.pi / 2))
                extent = (self.current[0] - turtlesize,
                        self.current[0] + turtlesize,
                        self.current[1] - turtlesize,
                        self.current[1] + turtlesize)
                plt.imshow(turtle, extent=extent)

            plt.show()

        finally:
            self.__init__()


pen = Pen()
