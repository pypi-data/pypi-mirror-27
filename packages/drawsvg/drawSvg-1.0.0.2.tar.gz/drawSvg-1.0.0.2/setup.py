import subprocess
from setuptools import setup

try:
    longDesc = subprocess.check_output(
                    ('pandoc', '--to', 'rst', 'README.md'))
    longDesc = longDesc.decode()
except Exception as e:
    print('Waring: Install Pandoc to use README.md as the long_description property')
    longDesc = None

setup(
    name = 'drawSvg',
    packages = ['drawSvg'],
    version = '1.0.0.2',
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

