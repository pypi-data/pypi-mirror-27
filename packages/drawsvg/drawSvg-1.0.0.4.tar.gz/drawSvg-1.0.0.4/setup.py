import subprocess
from setuptools import setup

with open('DESCRIPTION.rst', 'r') as f:
    longDesc = f.read()

setup(
    name = 'drawSvg',
    packages = ['drawSvg'],
    version = '1.0.0.4',
    description = 'This is a Python 3 library for programmatically generating SVG images (vector drawings) and rendering them or displaying them in an iPython notebook.',
    long_description = longDesc,
    author = 'Casey Duckering',
    #author_email = '',
    url = 'https://github.com/cduck/drawSvg',
    download_url = 'https://github.com/cduck/drawSvg/archive/1.0.0.tar.gz',
    keywords = ['SVG', 'draw', 'graphics', 'iPython', 'Jupyter'],
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Framework :: IPython',
        'Framework :: Jupyter',
    ],
    requires = [
        'cairoSVG',
    ],
)

