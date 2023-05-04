# Configuration file for the Sphinx documentation builder.
# -- Project information
import datetime
import os
import sys

from pip._vendor.pkg_resources import parse_version

import pyvkbot

sys.path.insert(0, os.path.abspath("../.."))

project = "pyvkbot"
author = "Zeph1rr"
copyright = f"{datetime.datetime.now().year}, {author}"

parsed_version = parse_version(pyvkbot.__version__)

version = parsed_version.base_version
release = pyvkbot.__version__


# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
