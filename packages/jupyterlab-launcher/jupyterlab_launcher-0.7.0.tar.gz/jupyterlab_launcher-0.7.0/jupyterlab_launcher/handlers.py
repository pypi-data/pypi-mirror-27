# coding: utf-8
"""Jupyter Lab Launcher handlers"""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import json
import os

from tornado import web, template
from notebook.base.handlers import IPythonHandler, FileFindHandler
from jinja2 import FileSystemLoader, TemplateError
from notebook.utils import url_path_join as ujoin
from traitlets import HasTraits, Bool, Unicode

from .settings_handler import SettingsHandler


# -----------------------------------------------------------------------------
# Module globals
# -----------------------------------------------------------------------------

# The default urls for the application.
default_public_url = '/lab/static/'
default_settings_url = '/lab/api/settings/'
default_themes_url = '/lab/api/themes/'


DEFAULT_TEMPLATE = template.Template("""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Error</title>
</head>
<body>
<h2>Cannot find template: "{{name}}"</h2>
<p>In "{{path}}"</p>
</body>
</html>
""")


class LabHandler(IPythonHandler):
    """Render the JupyterLab View."""

    def initialize(self, lab_config):
        self.lab_config = lab_config
        self.file_loader = FileSystemLoader(lab_config.templates_dir)

    @web.authenticated
    @web.removeslash
    def get(self):
        config = self.lab_config
        settings_dir = config.app_settings_dir

        # Handle page config data.
        page_config = self.settings.setdefault('page_config_data', {})
        terminals = self.settings.get('terminals_available', False)
        server_root = self.settings.get('server_root_dir', '')
        page_config.setdefault('terminalsAvailable', terminals)
        page_config.setdefault('ignorePlugins', [])
        page_config.setdefault('serverRoot', server_root)

        mathjax_config = self.settings.get('mathjax_config',
                                           'TeX-AMS_HTML-full,Safe')
        page_config.setdefault('mathjaxConfig', mathjax_config)
        page_config.setdefault('mathjaxUrl', self.mathjax_url)

        for name in config.trait_names():
            page_config[_camelCase(name)] = getattr(config, name)

        # Load the current page config file if available.
        page_config_file = os.path.join(settings_dir, 'page_config.json')
        if os.path.exists(page_config_file):
            with open(page_config_file) as fid:
                try:
                    page_config.update(json.load(fid))
                except Exception as e:
                    print(e)

        # Handle error when the assets are not available locally.
        local_index = os.path.join(config.static_dir, 'index.html')
        if config.static_dir and not os.path.exists(local_index):
            self.write(self.render_template(
                'error.html', static_dir=config.static_dir
            ))
            return

        # Write the template with the config.
        self.write(self.render_template('index.html', page_config=page_config))

    def get_template(self, name):
        return self.file_loader.load(self.settings['jinja2_env'], name)

    def render_template(self, name, **ns):
        try:
            return IPythonHandler.render_template(self, name, **ns)
        except TemplateError:
            return DEFAULT_TEMPLATE.generate(
                name=name, path=self.lab_config.templates_dir
            )


class LabConfig(HasTraits):
    """The lab application configuration object.
    """
    app_name = Unicode('',
        help='The name of the application')

    app_version = Unicode('',
        help='The version of the application')

    app_namespace = Unicode('',
        help='The namespace of the application')

    page_url = Unicode('/lab',
        help='The url path for the application')

    app_settings_dir = Unicode('',
        help='The application settings directory')

    templates_dir = Unicode('',
        help='The templates directory for the application')

    static_dir = Unicode('',
        help=('The optional location of the local static files.  '
              'If given, a handler will be added to server the files.'))

    public_url = Unicode(default_public_url,
        help=('The url public path for the application static files.  '
              'This can be a CDN if desired'))

    settings_url = Unicode(default_settings_url,
        help='The url path of the settings handler')

    user_settings_dir = Unicode('',
        help='The optional location of the user settings directory')

    schemas_dir = Unicode('',
        help='The optional location of the settings schemas directory.  '
              'If given, a handler will be added for settings')

    themes_url = Unicode(default_themes_url,
        help='The theme url')

    themes_dir = Unicode('',
        help=('The optional location of the themes directory.  '
              'If given, a handler will be added for themes'))

    cache_files = Bool(True,
        help=('Whether to cache files on the server. This should be '
              '`True` unless in development mode'))


def add_handlers(web_app, config):
    """Add the appropriate handlers to the web app.
    """
    # Normalize directories.
    for name in config.trait_names():
        if not name.endswith('_dir'):
            continue
        value = getattr(config, name)
        setattr(config, name, value.replace(os.sep, '/'))

    # Set up the main page handler.
    base_url = web_app.settings['base_url']
    handlers = [
        (ujoin(base_url, config.page_url, r'/?'), LabHandler, {
            'lab_config': config
        })
    ]

    # Cache all or none of the files depending on the `cache_files` setting.
    no_cache_paths = ['/'] if config.cache_files else []

    # Handle local static assets.
    if config.static_dir:
        config.public_url = ujoin(base_url, default_public_url)
        handlers.append((config.public_url + "(.*)", FileFindHandler, {
            'path': config.static_dir,
            'no_cache_paths': no_cache_paths
        }))

    # Handle local settings.
    if config.schemas_dir:
        config.settings_url = ujoin(base_url, default_settings_url)
        settings_path = config.settings_url + '(?P<section_name>.+)'
        handlers.append((settings_path, SettingsHandler, {
            'app_settings_dir': config.app_settings_dir,
            'schemas_dir': config.schemas_dir,
            'settings_dir': config.user_settings_dir
        }))

    # Handle local themes.
    if config.themes_dir:
        config.themes_url = ujoin(base_url, default_themes_url)
        handlers.append((ujoin(config.themes_url, "(.*)"), FileFindHandler, {
            'path': config.themes_dir,
            'no_cache_paths': no_cache_paths
        }))

    web_app.add_handlers(".*$", handlers)


def _camelCase(base):
    """Convert a string to camelCase.
    https://stackoverflow.com/a/20744956
    """
    output = ''.join(x for x in base.title() if x.isalpha())
    return output[0].lower() + output[1:]
