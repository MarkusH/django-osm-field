#!/usr/bin/env python
import sys
import os
from os.path import abspath, dirname, join
from pkg_resources import get_distribution

os.environ['DJANGO_SETTINGS_MODULE'] = 'example.settings'

sys.path.insert(0, abspath(join(dirname(__file__), '..', '..', 'example')))
sys.path.insert(0, abspath(join(dirname(__file__), '..', '..')))

# -- General configuration -----------------------------------------------------

project = u'django-osm-field'
copyright = u'2014, Markus Holtermann, et al'
version = release = get_distribution("django-osm-field").version

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']
exclude_patterns = ['build']

master_doc = 'index'
source_suffix = '.rst'

pygments_style = 'sphinx'
templates_path = ['_templates']

intersphinx_mapping = {
    'django': ('https://docs.djangoproject.com/en/dev/',
               'https://docs.djangoproject.com/en/dev/_objects/'),
}

# -- Options for HTML output ---------------------------------------------------
html_static_path = ['_static']
htmlhelp_basename = 'django-osm-fielddoc'
modindex_common_prefix = ['osm_field.']
