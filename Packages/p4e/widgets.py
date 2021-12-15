"""
Factory methods for widgets.

Author: Mike Matera
"""

import sys 
import ipywidgets

from typing import Dict, Iterable

from IPython.core.display import display 

def layout(*rows: Iterable[ipywidgets.Widget]) -> ipywidgets.Widget:
    """
    Create a simple grid layout. 
    """
    display(ipywidgets.VBox(tuple(map(ipywidgets.HBox, rows))))

def bind(fname: str, widgets: Dict[str, ipywidgets.Widget]) -> ipywidgets.Output:
    """
    Bind controls to a function. 
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
