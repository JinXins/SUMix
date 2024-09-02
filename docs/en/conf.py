# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

import pytorch_sphinx_theme

sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'OpenMixup'
copyright = '2021-2022, CAIRI'
author = 'CAIRI OpenMixup Authors'

# # The full version, including alpha/beta/rc tags
# version_file = '../../openmixup/version.py'


# def get_version():
#     with open(version_file, 'r') as f:
#         exec(compile(f.read(), version_file, 'exec'))
#     return locals()['__version__']


# release = get_version()

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.viewcode',
    'sphinx_markdown_tables', 'sphinx_copybutton', 'myst_parser'
]

autodoc_mock_imports = ['json_tricks', 'openmixup.version']

# Ignore >>> when copying code
copybutton_prompt_text = r'>>> |\.\.\. '
copybutton_prompt_is_regexp = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pytorch_sphinx_theme'
html_theme_path = [pytorch_sphinx_theme.get_html_theme_path()]
html_theme_options = {
    # The target url that the logo directs to. Unset to do nothing
    'logo_url': 'https://openmixup.readthedocs.io/en/latest/',
    # "menu" is a list of dictionaries where you can specify the content and the 
    # behavior of each item in the menu. Each item can either be a link or a
    # dropdown menu containing a list of links.
    'menu': [
        {
            'name': 'GitHub',
            'url': 'https://github.com/Westlake-AI/openmixup'
        },
        {
            'name':
            'Upstream',
            'children': [
                {
                    'name': 'MMCV',
                    'url': 'https://github.com/open-mmlab/mmcv',
                    'description': 'Foundational library for computer vision'
                },
                {
                    'name': 'MMDetection',
                    'url': 'https://github.com/open-mmlab/mmdetection',
                    'description': 'Object detection toolbox and benchmark'
                },
                {
                    'name': 'MMClassification',
                    'url': 'https://github.com/open-mmlab/mmclassification',
                    'description': 'OpenMMLab Image Classification Toolbox and Benchmark'
                },
                {
                    'name': 'MMSelfSup',
                    'url': 'https://github.com/open-mmlab/mmselfsup',
                    'description': 'OpenMMLab Self-Supervised Learning Toolbox and Benchmark'
                },
            ]
        },
    ],
    # For shared menu: If your project is a part of OpenMMLab's project and 
    # you would like to append Docs and OpenMMLab section to the right
    # of the menu, you can specify menu_lang to choose the language of
    # shared contents. Available options are 'en' and 'cn'. Any other
    # strings will fall back to 'en'.
    'menu_lang': 'en'
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

language = 'en'

html_static_path = ['_static']
html_css_files = ['css/readthedocs.css']

# Enable ::: for my_st
myst_enable_extensions = ['colon_fence']
myst_heading_anchors = 4

master_doc = 'index'
