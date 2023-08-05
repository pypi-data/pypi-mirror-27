import sys
from os import path
from setuptools import setup

# Get the long description from the README file
with open(path.join(path.dirname(__file__), 'Readme.rst'), 'r') as f:
    long_description = f.read()

PY2 = (sys.version_info < (3, 0))


setup(
    name='py2venv',
    use_scm_version=True,
    description='Shortcut from virtualenv to venv for python2',
    long_description=long_description,
    url='https://gitlab.com/alelec/py2venv',
    author='Andrew Leech',
    author_email='andrew@alelec.net',
    license='MIT',
    packages=['venv'] if PY2 else [],
    install_requires=['setuptools_scm', 'virtualenv; python_version<"3.0"'],
    setup_requires=['setuptools_scm'],
)
