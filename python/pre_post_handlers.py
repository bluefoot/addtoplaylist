import xbmc, xbmcgui
from playlists import PlaylistService
from lib.pykodi import log, get_main_addon, localize as L
from translations import TranslationKey

DUPLICATE_ENTRIES_SETTING_KEY = 'duplicateentries'
    
class DuplicateOption:
    ASK = '0'
    ADD = '1'
    DO_NOTHING = '2'

class DuplicateFileHandler:
    def handle(self, playlist, filename_to_add, filelabel):
        same_input = (playlist, filename_to_add, filelabel)
        empty_return_value = (None, None, None)
        if playlist is not None and PlaylistService().playlist_contains_file(playlist, filename_to_add):
            duplicate_setting = get_main_addon().getSetting(DUPLICATE_ENTRIES_SETTING_KEY)
            if duplicate_setting == DuplicateOption.ASK:
                user_said_yes = self._ask_user_to_add_item(playlist, filename_to_add, filelabel)
                return same_input if user_said_yes else empty_return_value
            elif duplicate_setting == DuplicateOption.ADD:
                return same_input
            elif duplicate_setting == DuplicateOption.DO_NOTHING:
                xbmcgui.Dialog().notification(None, L(TranslationKey.VIDEO_ALREADY_IN_PLAYLIST_HEADER), xbmcgui.NOTIFICATION_WARNING)
                return empty_return_value
            else:
                raise Exception("Invalid setting '%s' for entry '%s'" % (duplicate_setting, DUPLICATE_ENTRIES_SETTING_KEY))
        else:
            return same_input

    def _ask_user_to_add_item(self, playlist, filename_to_add, filelabel):
        return xbmcgui.Dialog().yesno(L(TranslationKey.VIDEO_ALREADY_IN_PLAYLIST_HEADER), 
            L(TranslationKey.VIDEO_ALREADY_IN_PLAYLIST_PROMPT).format(filelabel, playlist.label))

class PrePostHandler:
    pre_handler_chain = [DuplicateFileHandler()]
    post_handler_chain = []

    def pre_handle(self, playlist, filename_to_add, filelabel):
        return self._run_handlers(playlist, filename_to_add, filelabel, self.pre_handler_chain)
    
    def post_handle(self, playlist, filename_to_add, filelabel):
        return self._run_handlers(playlist, filename_to_add, filelabel, self.post_handler_chain)

    def _run_handlers(self, _playlist, _filename_to_add, _filelabel, handler_chain):
        playlist, filename_to_add, filelabel = _playlist, _filename_to_add, _filelabel
        for handler in handler_chain:
            log('Running pre handler %s' % (handler), xbmc.LOGDEBUG)
            playlist, filename_to_add, filelabel = handler.handle(playlist, filename_to_add, filelabel)
        return playlist, filename_to_add, filelabel