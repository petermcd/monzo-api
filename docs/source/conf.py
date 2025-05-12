import datetime
import os
import sys
from configparser import ConfigParser

sys.path.insert(0, os.path.abspath('../'))
config = ConfigParser()
config.read('../../setup.cfg')

copyright_year = datetime.datetime.now().year
author = config['metadata']['author']
project = config['metadata']['name']
copyright = f'{copyright_year}, {author}'

release = config['metadata']['version']

extensions: list[str] = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
]

templates_path: list[str] = ['_templates']

exclude_patterns: list[str] = []

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']
