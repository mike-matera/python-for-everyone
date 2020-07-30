"""
A simple implementation of turtle graphics for teaching algorithms. 

Author: Mike Matera
"""

import math 
import pathlib 

from ipycanvas import MultiCanvas, hold_canvas
from ipywidgets import Image

from IPython.display import display 

class Turtle:

    def __init__(self, size=(400,400)):
        self._size = size
        self._canvas = MultiCanvas(width=size[0], height=size[1])
        self._turtle = Image.from_file(pathlib.Path(__file__).parent / "turtle.png")
        self.clear()
        
    def clear(self):
        """Clear the canvas and start over."""
        self._canvas.clear()
        self._current = (self._size[0]//2, self._size[1]//2)
        self._cur_heading = (3 * math.pi) / 2 # in Canvas Y is negative.
        self._pendown = True 
        self._show = True       
        self._draw_turtle()
        
    def _draw_turtle(self):
        """Update the position of the turtle."""
        with hold_canvas(self._canvas[2]):
            self._canvas[2].clear()
            self._canvas[2].reset_transform()
            if self._show:
                self._canvas[2].translate(self._current[0], self._current[1])
                self._canvas[2].rotate(self._cur_heading - (3 * math.pi) / 2)
                self._canvas[2].draw_image(self._turtle, x=-15, y=-15, \
                    width=30, height=30)

    def draw(self, distance):
        """Move the pen by distance."""
        start = self._current
        self._current = (self._current[0] + math.cos(self._cur_heading) * distance,
                        self._current[1] + math.sin(self._cur_heading) * distance)                        
        if self._pendown:
            self._canvas[1].begin_path()
            self._canvas[1].move_to(*start)
            self._canvas[1].line_to(*self._current)
            self._canvas[1].stroke()
        self._draw_turtle()

    def turn(self, degrees):
        """Turn the pen by degrees"""
        self._cur_heading = (self._cur_heading - math.radians(degrees)) % (math.pi * 2)
        self._draw_turtle()

    def goto(self, x, y):
        """Goto a point in the coordinate space."""
        start = self._current
        self._current = (self._size[0]//2 + x, self._size[1]//2 - y)
        if self._pendown:
            self._canvas[1].begin_path()
            self._canvas[1].move_to(*start)
            self._canvas[1].line_to(*self._current)
            self._canvas[1].stroke()
        self._draw_turtle()

    def heading(self, heading):
        """Set the pen to face heading."""
        self._cur_heading = -math.radians(heading)
        self._draw_turtle()

    def up(self):
        """Pick the pen up. Movements won't make lines."""
        self._pendown = False

    def down(self):
        """Put the pen down. Movements will make lines."""
        self._pendown = True

    def color(self, color):
        """Set the pen color."""
        self._canvas[1].stroke_style = color

    def width(self, width):
        """Set the line thickness."""
        self._canvas[1].line_width = width 

    def show(self):
        """Show the turtle in the scene.""" 
        self._show = True 
        self._draw_turtle()

    def hide(self):
        """Hide the turtle in the scene.""" 
        self._show = False 
        self._draw_turtle()

    def background(self, filename):
        """Set a background image.""" 
        img = Image.from_file(filename)
        self._canvas[0].draw_image(img, x=0, y=0, \
            width=self._canvas[0].size[0], height=self._canvas[0].size[1])
          
    def _ipython_display_(self):
        display(self._canvas)
