# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
project = 'AlphaX Movie Recognition and Recommendation System using GenAI'
copyright = '2024, Qadeer Ahmad'
author = 'Qadeer Ahmad'
release = '1.1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc","sphinx.ext.viewcode",
              "sphinx.ext.todo","sphinx.ext.napoleon"]
autodoc_member_order = 'bysource'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','../setup.py']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['../static']

