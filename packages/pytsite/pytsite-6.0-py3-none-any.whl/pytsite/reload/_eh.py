"""PytSite Reload Event Handlers.
"""
from pytsite import router as _router, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    pass
    # if _api.get_flag() and _auth.get_current_user().has_permission('pytsite.reload'):
    #     _assetman.preload('pytsite.reload@js/reload.js')
    #     _router.session().add_warning_message(_lang.t(_api.RELOAD_MSG_ID))
