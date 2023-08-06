import os
import sys

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(os.path.join('..', 'src')))

# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

authors = ['Stefan Scherfke']
project = 'aiomas'
copyright = f'2014, {", ".join(authors)}'

version = '2.0'
release = '2.0.0'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'alabaster'

html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'aiomasdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    # 'preamble': '',
}

latex_documents = [
    (master_doc, 'aiomas.tex', 'aiomas Documentation',
     ''.join(authors), 'manual'),
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    (master_doc, 'aiomas', 'aiomas Documentation',
     authors, 1)
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (master_doc, 'aiomas', 'aiomas Documentation',
     ''.join(authors), 'aiomas', 'One line description of project.',
     'Miscellaneous'),
]


# Intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'arrow': ('https://arrow.readthedocs.io/en/latest/', None),
}

# Autodoc
autodoc_member_order = 'bysource'
