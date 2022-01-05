"""
Factory methods for widgets.

Author: Mike Matera
"""

import sys 
import ipywidgets

from typing import Dict, Iterable

from IPython.core.display import display 


def bind(fname: str, widgets: Dict[str, ipywidgets.Widget]) -> ipywidgets.Output:
    """
    Bind controls to a function. The function is given by name and is searched for in the __main__ 
    package. Returns a Widget that displays the output of the wrapped function. The return 
    value of the wrapped function is given to `display()` and shown in the output widget.

    The purpose of this function is to make it possible to wrap a student function before 
    the function is defined in the notebook. If the function doesn't exist an error message
    is shown. The function output can be nestled with input widgets at the top of a notebook.
    """
    def wrapper(**kwargs):
        main = sys.modules['__main__']
        if hasattr(main, fname):
            got = getattr(main, fname)(**kwargs)
            if isinstance(got, tuple):
                display(*got)
            else:
                display(got)
        else:
            display(f"Function __main__.{fname} is not defined.")

    out = ipywidgets.interactive_output(wrapper, widgets)
    label = ipywidgets.HTML(f"""<pre style="">{fname}</pre>""")
    panel = ipywidgets.VBox([label, out])
    panel.layout = {
        'margin': '1em',
    }    
    out.layout = {
        'border': '1px solid lightgrey',
        'padding': '1em 1em 1em 1em',
    }
    return panel
