"""PytSite Plugin Manager
"""
# Public API
from sys import exit as _exit
from . import _error as error
from ._api import plugins_path, plugin_info, install, uninstall, is_installed, load, is_loaded, \
    plugins_info, remote_plugin_info, remote_plugins_info, is_dev_mode, get_dependant_plugins, \
    get_allowed_version_range, on_install, on_update, on_uninstall

from importlib.machinery import PathFinder as _PathFinder

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_plugman_started = False


class _PluginPathFinder(_PathFinder):
    @classmethod
    def find_spec(cls, fullname: str, path: list = None, target=None):
        fullname_parts = fullname.split('.')

        if fullname_parts[0] == 'plugins' and len(fullname_parts) == 2:
            spec = _PathFinder.find_spec(fullname, path, target)
            if not spec:
                raise error.PluginNotInstalled(fullname_parts[1])

            return spec


def _init():
    import sys
    from os import mkdir, path
    from pytsite import lang, console, update, logger
    from . import _console_command

    sys.meta_path.insert(2, _PluginPathFinder())

    # Resources
    lang.register_package(__name__)

    # Create 'plugins' package if it doesn't exist
    plugins_dir_path = plugins_path()
    if not path.exists(plugins_dir_path):
        mkdir(plugins_dir_path, 0o755)
        with open(path.join(plugins_dir_path, '__init__.py'), 'wt') as f:
            f.write('"""Pytsite Plugins\n"""\n')

    # Register console commands
    console.register_command(_console_command.Install())
    console.register_command(_console_command.Update())
    console.register_command(_console_command.Uninstall())

    # Start installed plugins
    for p_name in plugins_info():
        if p_name.startswith('_'):
            continue

        try:
            if not is_loaded(p_name):
                load(p_name)

        except error.PluginStartError as e:
            logger.error(e)
            console.print_warning(str(e))

    global _plugman_started
    _plugman_started = True

    # Event handlers
    update.on_update_after(lambda: console.run_command('plugman:update', {'reload': False}))


_init()
