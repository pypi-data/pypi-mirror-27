# notebook-wide-screen

This is a Python package to allow a user to display a [Jupyter notebook](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html) in a very wide screen by injection of CSS in an output cell. As a consequence for security reasons it only works in [**trusted** notebooks](http://jupyter-notebook.readthedocs.io/en/stable/security.html#security-in-notebook-documents).  

## 1 - Install

From terminal:

```bash
pip install notebook_wide_screen
```

## 2 - User Guide

In a notebook cell:

```Python
from notebook_wide_screen import WideScreen
# example
WideScreen(width='95%', verbose=False).add_js()
```

This will inject CSS (in the output cell) with immediate effect.  

The arguments are:
+ `width` (default='95%') represents the width of the notebook and header containers in css parlance.  
+ `verbose` (default=False) gives you more info about the mechanism.  

To rid the notebook of the wide-screen feature just clear the output cell.

See the [demo notebook](http://nbviewer.jupyter.org/github/oscar6echo/notebook-wide-screen/blob/master/demo_wide_screen.ipynb)


## 3 - Security

Because a notebook is designed to allow the user to write arbitrary code, it has full access to many resources.  

The typical risks are the following:
+ A notebook has access to your file system and can therefore potentially read/modify/delete any of your files or send them to an attacker, or write a new file (virus).  
+ A notebook may contain javascript in output cells which can read you cookies and local storage and potentially send them to an attacker.  

See the [Security in notebook documents](https://jupyter-notebook.readthedocs.io/en/stable/security.html#security-in-notebook-documents) section of the official [Jupyter Notebook documentation](https://jupyter-notebook.readthedocs.io/en/stable/index.html) for more info.  

Therefore you **should review** and **must trust** the notebook before you can use **notebook-wide-screen**.


<!-- pandoc --from=markdown --to=rst --output=README.rst README.md -->
