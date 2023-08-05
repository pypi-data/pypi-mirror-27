py2venv
========

Provides a simple "shortcut" from virtualenv to venv on python 2.

Pretty much everything I do is in python3, where I use venv for every single project I work on.

Occasionally I need my CI to also test / build / deploy to python2 as well. 
As is stands, I generally end up with annoyingly complex startups scripts in ci that has to check which version 
is being being run and then either use `python -m venv .venv` on 3 or `python -m pip install virtualenv; python -m virtualenv .venv` for 2.

It would be much better if I could just use `python -m venv .venv` everywhere, but venv has not been backported. This package is a pretty decent workaround.

py2venv can be pre-installed on any python. On python3 it does nothing. On python 2 it ensures virtualenv has been installed and provides a 'venv' module entrypoint::

  python -m pip install py2venv
  python -m venv .venv
