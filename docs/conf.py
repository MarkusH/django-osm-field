#!/usr/bin/env python
import sys
import os
from os.path import abspath, dirname, join

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

sys.path.insert(0, abspath(join(dirname(__file__), '..', '..', 'example')))
sys.path.insert(0, abspath(join(dirname(__file__), '..', '..')))

from osm_field import __version__

# -- General configuration -----------------------------------------------------

project = u'django-osm-field'
copyright = u'2014, Markus Holtermann, et al'
version = __version__
release = __version__

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
exclude_patterns = ['_build']

master_doc = 'index'
source_suffix = '.rst'

pygments_style = 'sphinx'
templates_path = ['_templates']

intersphinx_mapping = {
    'django': ('https://docs.djangoproject.com/en/dev/',
               'https://docs.djangoproject.com/en/dev/_objects/'),
    'python2': ('http://docs.python.org/2/', None),
    'python3': ('http://docs.python.org/3/', None),
}

# -- Options for HTML output ---------------------------------------------------
html_theme = 'nature'
html_static_path = ['_static']
htmlhelp_basename = 'django-osm-fielddoc'
modindex_common_prefix = ['osm_field.']

RTD_NEW_THEME = True
