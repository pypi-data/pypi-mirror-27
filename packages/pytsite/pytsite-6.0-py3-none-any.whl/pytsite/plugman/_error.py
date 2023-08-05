"""PytSite Plugin Manager Errors.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PlugmanError(Exception):
    pass


class PluginsApiError(PlugmanError):
    def __init__(self, request_url: str, error_content: str):
        self._request_url = request_url
        self._error_content = error_content

    @property
    def request_url(self) -> str:
        return self._request_url

    @property
    def error_content(self) -> str:
        return self._error_content

    def __str__(self) -> str:
        return "Error while requesting plugin API URL '{}': {}".format(self._request_url, self._error_content)


class UnknownPlugin(PlugmanError):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is unknown".format(self._name)


class PluginNotInstalled(PlugmanError):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is not installed".format(self._name)


class PluginAlreadyInstalled(PlugmanError):
    def __init__(self, name: str, version: str):
        self._name = name
        self._version = version

    def __str__(self) -> str:
        return "Plugin '{}-{}' is already installed".format(self._name, self._version)


class PluginInstallationInProgress(PlugmanError):
    pass


class PluginUninstallationInProgress(PlugmanError):
    pass


class PluginInstallError(PlugmanError):
    pass


class PluginUninstallError(PlugmanError):
    pass


class PluginStartError(PlugmanError):
    pass


class PluginAlreadyStarted(PlugmanError):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is already started".format(self._name)


class PluginNotStarted(PlugmanError):
    def __init__(self, plugin_name: str):
        self._name = plugin_name

    def __str__(self) -> str:
        return "Plugin '{}' is not started".format(self._name)


class PluginDependencyError(PlugmanError):
    pass
