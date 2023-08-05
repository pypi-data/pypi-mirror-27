# coding: utf-8
"""A tornado based QuantLab server."""

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from notebook.notebookapp import NotebookApp, aliases, flags
from jupyter_core.application import JupyterApp, base_aliases

from traitlets import Bool, Unicode

from ._version import __version__
from .extension import load_jupyter_server_extension
from .commands import (
    build, clean, get_app_dir, get_user_settings_dir, get_app_version,
    ensure_dev
)


build_aliases = dict(base_aliases)
build_aliases['app-dir'] = 'QuantLabBuildApp.app_dir'
build_aliases['name'] = 'QuantLabBuildApp.name'
build_aliases['version'] = 'QuantLabBuildApp.version'


version = __version__
app_version = get_app_version()
if version != app_version:
    version = '%s (dev), %s (app)' % (__version__, app_version)


class QuantLabBuildApp(JupyterApp):
    version = version
    description = """
    Build the QuantLab application
    The application is built in the QuantLab app directory in `/staging`.
    When the build is complete it is put in the QuantLab app `/static`
    directory, where it is used to serve the application.
    """
    aliases = build_aliases

    app_dir = Unicode('', config=True,
        help="The app directory to build in")

    name = Unicode('QuantLab', config=True,
        help="The name of the built application")

    version = Unicode('', config=True,
        help="The version of the built application")

    def start(self):
        build(self.app_dir, self.name, self.version)


clean_aliases = dict(base_aliases)
clean_aliases['app-dir'] = 'QuantLabCleanApp.app_dir'


class QuantLabCleanApp(JupyterApp):
    version = version
    description = """
    Clean the QuantLab application
    This will clean the app directory by removing the `staging` and `static`
    directories.
    """
    aliases = clean_aliases

    app_dir = Unicode('', config=True,
        help="The app directory to clean")

    def start(self):
        clean(self.app_dir)


class QuantLabPathApp(JupyterApp):
    version = version
    description = """
    Print the configured paths for the QuantLab application
    The application path can be configured using the QUANTLAB_DIR environment variable.
    The user settings path can be configured using the QUANTLAB_SETTINGS_DIR
        environment variable or it will fall back to
        `/quantlab/user-settings` in the default Jupyter configuration directory.
    """

    def start(self):
        print('Application directory:   %s' % get_app_dir())
        print('User Settings directory: %s' % get_user_settings_dir())


quantlab_aliases = dict(aliases)
quantlab_aliases['app-dir'] = 'QuantLabApp.app_dir'

quantlab_flags = dict(flags)
quantlab_flags['core-mode'] = (
    {'QuantLabApp': {'core_mode': True}},
    "Start the app in core mode."
)
quantlab_flags['dev-mode'] = (
    {'QuantLabApp': {'dev_mode': True}},
    "Start the app in dev mode for running from source."
)
quantlab_flags['watch'] = (
    {'QuantLabApp': {'watch': True}},
    "Start the app in watch mode."
)


class QuantLabApp(NotebookApp):
    version = version

    description = """
    QuantLab - An extensible computational environment for Jupyter.
    This launches a Tornado based HTML Server that serves up an
    HTML5/Javascript QuantLab client.
    QuantLab has three different modes of running:
    * Core mode (`--core-mode`): in this mode QuantLab will run using the JavaScript
      assets contained in the installed `quantlab` Python package. In core mode, no
      extensions are enabled. This is the default in a stable QuantLab release if you
      have no extensions installed.
    * Dev mode (`--dev-mode`): uses the unpublished local JavaScript packages
        in the `dev_mode` folder.  In this case QuantLab will show a red stripe at the top of the page.  It can only be used if QuantLab
        is installed as `pip install -e .`.
    * App mode: QuantLab allows multiple QuantLab "applications" to be
      created by the user with different combinations of extensions. The `--app-dir` can
      be used to set a directory for different applications. The default application
      path can be found using `jupyter quantlab path`.
    """

    examples = """
        jupyter quantlab                       # start QuantLab
        jupyter quantlab --dev-mode            # start QuantLab in development mode, with no extensions
        jupyter quantlab --core-mode           # start QuantLab in core mode, with no extensions
        jupyter quantlab --app-dir=~/myquantlabapp # start QuantLab with a particular set of extensions
        jupyter quantlab --certfile=mycert.pem # use SSL/TLS certificate
    """

    aliases = quantlab_aliases
    flags = quantlab_flags

    subcommands = dict(
        build=(QuantLabBuildApp, QuantLabBuildApp.description.splitlines()[0]),
        clean=(QuantLabCleanApp, QuantLabCleanApp.description.splitlines()[0]),
        path=(QuantLabPathApp, QuantLabPathApp.description.splitlines()[0]),
        paths=(QuantLabPathApp, QuantLabPathApp.description.splitlines()[0])
    )

    default_url = Unicode('/quantlab', config=True,
        help="The default URL to redirect to from `/`")

    app_dir = Unicode(get_app_dir(), config=True,
        help="The app directory to launch QuantLab from.")

    core_mode = Bool(False, config=True,
        help="""Whether to start the app in core mode. In this mode, QuantLab
        will run using the JavaScript assets that are within the installed
        QuantLab Python package. In core mode, third party extensions are disabled.
        The `--dev-mode` flag is an alias to this to be used when the Python package
        itself is installed in development mode (`pip install -e .`).
        """)

    dev_mode = Bool(False, config=True,
        help="""Whether to start the app in dev mode. Uses the unpublished local JavaScript packages
        in the `dev_mode` folder.  In this case QuantLab will show a red stripe at the top of the page.  It can only be used if QuantLab
        is installed as `pip install -e .`.
        """)

    watch = Bool(False, config=True,
        help="Whether to serve the app in watch mode")

    def init_server_extensions(self):
        """Load any extensions specified by config.
        Import the module, then call the load_jupyter_server_extension function,
        if one exists.
        If the QuantLab server extension is not enabled, it will
        be manually loaded with a warning.
        The extension API is experimental, and may change in future releases.
        """
        super(QuantLabApp, self).init_server_extensions()
        msg = 'QuantLab server extension not enabled, manually loading...'
        if not self.nbserver_extensions.get('quantlab', False):
            self.log.warn(msg)
            load_jupyter_server_extension(self)


#-----------------------------------------------------------------------------
# Main entry point
#-----------------------------------------------------------------------------

main = launch_new_instance = QuantLabApp.launch_instance

if __name__ == '__main__':
    main()
