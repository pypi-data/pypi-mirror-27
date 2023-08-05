# -*- coding: utf-8 -*-
"""
    sphinxcontrib.confluencebuilder
    ===============================

    Sphinx extension to output Atlassian Confluence wiki files.

    .. moduleauthor:: Anthony Shaw <anthonyshaw@apache.org>

    :copyright: Copyright 2016 by Anthony Shaw.
    :license: BSD, see LICENSE.txt for details.
"""

from __future__ import (print_function, unicode_literals, absolute_import)

from sphinx.writers.text import STDINDENT
from .builders.confluence import ConfluenceBuilder


def setup(app):
    app.require_sphinx('1.0')
    app.add_builder(ConfluenceBuilder)
    app.add_config_value('confluence_file_suffix', ".conf", False)
    """This is the file name suffix for reST files"""
    app.add_config_value('confluence_link_suffix', None, False)
    """The is the suffix used in internal links. By default, takes the same value as confluence_file_suffix"""
    app.add_config_value('confluence_file_transform', None, False)
    """Function to translate a docname to a filename. By default, returns docname + confluence_file_suffix."""
    app.add_config_value('confluence_link_transform', None, False)
    """Function to translate a docname to a (partial) URI. By default, returns docname + confluence_file_suffix."""
    app.add_config_value('confluence_indent', STDINDENT, False)
    """Publish to a confluence website"""
    app.add_config_value('confluence_publish', None, False)
    """Name of the confluence space to publish to (if publishing)"""
    app.add_config_value('confluence_space_name', None, False)
    """Name of the page within the confluence space to use as the root (if publishing)"""
    app.add_config_value('confluence_parent_page', None, False)
    """Allow purging legacy child pages from a parent page (if publishing)."""
    app.add_config_value('confluence_purge', None, False)
    """URL of the Confluence server to publish to"""
    app.add_config_value('confluence_server_url', None, False)
    """ Username to login to Confluence API with """
    app.add_config_value('confluence_server_user', None, False)
    """ Password to login to Confluence API with """
    app.add_config_value('confluence_server_pass', None, False)
    """ File to get page header information from. """
    app.add_config_value('confluence_header_file', None, False)
    """ File to get page footer information from. """
    app.add_config_value('confluence_footer_file', None, False)
