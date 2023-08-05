"""PytSite Language Package
"""
# Public API
from . import _error as error
from ._api import t, t_plural, register_package, define, is_defined, get_packages, langs, get_package_translations, \
    get_current, set_current, is_package_registered, lang_title, time_ago, pretty_date, pretty_date_time, \
    is_translation_defined, get_fallback, set_fallback, ietf_tag, get_primary, register_global, on_translate, \
    clear_cache, on_split_msg_id

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import reg, tpl

    # Register itself as a language package
    register_package(__name__)

    # Languages set
    define(reg.get('languages', ['en']))


_init()
