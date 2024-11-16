# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "F3 Nation Data"
copyright = "2024, Evan Petzoldt"
author = "Evan Petzoldt"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    # "sphinx_multiversion",
]

autoclass_content = "class"

templates_path = ["_templates"]
# html_sidebars = {
#     "**": [
#         "sidebar/brand.html",
#         "sidebar/search.html",
#         "sidebar/scroll-start.html",
#         "sidebar/navigation.html",
#         "sidebar/versions.html",
#         "sidebar/scroll-end.html",
#     ],
# }
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
