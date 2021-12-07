"""
Factory methods for widgets.

Author: Mike Matera
"""

from typing import Iterable

import ipywidgets


def selector(description: str, values: Iterable):
    """
    Create a selection widget
    """    
    return ipywidgets.Select(
        options=list(values),
        description=description,
    )

def textbox():
    """
    Create a text selection input
    """


def colorpicker():
    """
    Pick a color
    """


def datepicker():
    """
    Pick a date
    """


def intslider():
    """
    Integer slider
    """


def floatslider():
    """
    Floating point number
    """
