"""
A simple implementation of turtle graphics for teaching algorithms. 

Author: Mike Matera
"""

import math 
import pathlib
import numpy 
import PIL 

import face_recognition

from collections import namedtuple
from ipycanvas import Canvas, MultiCanvas, hold_canvas
from ipywidgets import Image

from IPython.display import display


class Turtle:

    DimPoint = namedtuple('DimPoint', ['x', 'y'])

    def _to_native(self, point):
        """Convert Turtle coordinates to native ones."""
        return Turtle.DimPoint(x=self._size.x//2 + point[0], y=self._size.y//2 - point[1])

    def _to_turtle(self, point):
        """Convert Turtle coordinates to native ones."""
        return (point[0] - self._size.x//2, self._size.y//2 - point[1])

    def __init__(self, size=DimPoint(x=600,y=300)):
        """Create a Turtle drawing canvas."""
        self._image = None
        self._size = size
        turtle = numpy.array(PIL.Image.open(pathlib.Path(__file__).parent / "turtle.png"))
        self._turtle = Canvas(width=turtle.shape[0], height=turtle.shape[1])
        self._turtle.put_image_data(turtle)
        self._canvas = MultiCanvas(n_canvases=3, width=self._size.x, height=self._size.y) 
        self.clear()
        
    def clear(self):
        """Clear the canvas and start over."""
        self._canvas[1].clear()
        self._current = self._to_native(Turtle.DimPoint(0,0))
        self._cur_heading = (3 * math.pi) / 2 # in Canvas Y is negative.
        self._pendown = True 
        self._show = True       
        self._draw_turtle()
        
    def _draw_turtle(self):
        """Update the position of the turtle."""
        self._canvas[2].clear()
        if self._show:
            self._canvas[2].save()
            self._canvas[2].translate(self._current.x, self._current.y)
            self._canvas[2].rotate(self._cur_heading + math.pi / 2)
            self._canvas[2].draw_image(self._turtle, 
                x=-15, y=-15, 
                width=30, height=30)
            self._canvas[2].restore()

    def draw(self, distance):
        """Move the pen by distance."""
        start = self._current
        self._current = Turtle.DimPoint(x = self._current.x + math.cos(self._cur_heading) * distance,
                        y = self._current.y + math.sin(self._cur_heading) * distance)                        
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

    def goto(self, *place):
        """Goto a point in the coordinate space."""
        if len(place) == 0:
            raise ValueError("Goto where?")
        elif isinstance(place[0], Turtle.DimPoint):
            p = place[0]
        elif isinstance(place[0], tuple):
            p = Turtle.DimPoint._make(*place)
        else:
            p = Turtle.DimPoint._make(place)

        start = self._current
        self._current = self._to_native(p)
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
        self._canvas[1].fill_style = color

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
        """Set the background image"""
        self._image = numpy.array(PIL.Image.open(filename))
        self._size = Turtle.DimPoint(x=self._image.shape[1], y=self._image.shape[0])
        self._canvas.width = self._size[0]
        self._canvas.height = self._size[1]
        self._canvas[0].put_image_data(self._image)
        self.clear()
    
    def find_faces(self):
        faces = face_recognition.face_locations(self._image, model='hog')
        features = face_recognition.face_landmarks(self._image, face_locations=faces)
        rval = []        
        for i in range(len(faces)):
            face = {}
            face.update({
                'top_right':    self._to_turtle(Turtle.DimPoint(x=faces[i][1], y=faces[i][0])),
                'top_left':     self._to_turtle(Turtle.DimPoint(x=faces[i][3], y=faces[i][0])),
                'bottom_left':  self._to_turtle(Turtle.DimPoint(x=faces[i][3], y=faces[i][2])),
                'bottom_right': self._to_turtle(Turtle.DimPoint(x=faces[i][1], y=faces[i][2])),                
            })
            for feature in features[i]:
                face[feature] = list(map(self._to_turtle, features[i][feature]))
            rval.append(face)
        return rval

    def polygon(self, points):
        """Draw a filled polygon."""
        self._canvas[1].begin_path()
        self._canvas[1].move_to(*self._to_native(points[0]))
        for point in points[1:]:
            self._canvas[1].line_to(*self._to_native(point))
        self._canvas[1].fill()

    def write(self, text, font="24px sans-serif", text_align="center", line_color=None, fill_color=None):
        """Write text"""
        old_stroke = self._canvas[1].stroke_style
        old_fill = self._canvas[1].fill_style
        if line_color is not None:
            self._canvas[1].stroke_style = line_color
        if fill_color is not None:
            self._canvas[1].fill_style = fill_color
        self._canvas[1].translate(self._current.x, self._current.y)
        self._canvas[1].rotate(self._cur_heading + math.pi/2)
        self._canvas[1].font = font
        self._canvas[1].text_align = text_align
        self._canvas[1].fill_text(text, 0, 0)
        self._canvas[1].stroke_text(text, 0, 0)
        self._canvas[1].reset_transform()
        self._canvas[1].stroke_style = old_stroke
        self._canvas[1].fill_style = old_fill

    def _ipython_display_(self):
        display(self._canvas)
