"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['guitar_trainer.py']
DATA_FILES = ['guitar_cat.jpeg']
OPTIONS = {'iconfile': '/Users/mariebbr/guitar_trainer/guitar.icns'}

setup(
	name="Guitar Trainer",
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)