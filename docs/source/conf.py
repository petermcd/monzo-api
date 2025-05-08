"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import datetime
import os
import sys
from configparser import ConfigParser
from typing import List

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath('../'))
config = ConfigParser()
config.read('../../setup.cfg')

# -- Project information -----------------------------------------------------

copyright_year = datetime.datetime.now().year
author = config['metadata']['author']
project = config['metadata']['name']
copyright = f'{copyright_year}, {author}'

# The full version, including alpha/beta/rc tags

release = config['metadata']['version']


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions: List[str] = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
]

# Add any paths that contain templates here, relative to this directory.
templates_path: List[str] = ['_templates']

# List of patterns, relative to the source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns: List[str] = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
