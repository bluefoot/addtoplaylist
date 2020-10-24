import os, sys, traceback
import xbmc, xbmcaddon, xbmcgui
from playlists import PlaylistService, Playlist
from pre_post_handlers import PrePostHandler
from translations import TranslationKey
addon = xbmcaddon.Addon()
addonpath = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(addonpath, u'python', u'lib'))
from pykodi import log, localize as L

playlist_service = PlaylistService()

def _prompt_user_to_create_new_playlist():
    playlist_name = xbmcgui.Dialog().input(L(TranslationKey.NEW_PLAYLIST_NAME)).strip()
    if playlist_name:
        return playlist_service.create_empty_playlist(playlist_name)

def _prompt_user_to_select_playlist(playlists):
    add_new_playlist_item = Playlist(label = L(TranslationKey.CREATE_NEW_PLAYLIST))
    selectable_items = [add_new_playlist_item] + playlists
    selected_playlist_index = xbmcgui.Dialog().select(L(TranslationKey.SELECT_A_PLAYLIST), [playlist.label for playlist in selectable_items])
    selected_playlist = None
    if selected_playlist_index == 0:
        selected_playlist = _prompt_user_to_create_new_playlist()
    else:
        adjusted_index = selected_playlist_index - 1
        selected_playlist = playlists[adjusted_index] if adjusted_index >= 0 else None
    return selected_playlist

def add_to_playlist(filename, filelabel):
    try:
        playlists = playlist_service.get_all_supported_playlists()
        selected_playlist = _prompt_user_to_select_playlist(playlists)
        selected_playlist, filename, filelabel = PrePostHandler().pre_handle(selected_playlist, filename, filelabel)
        if selected_playlist is not None:
            playlist_service.add_file_to_playlist(selected_playlist, filename, filelabel)
            xbmcgui.Dialog().notification(L(TranslationKey.SUCCESS), L(TranslationKey.ADDED_FILE_TO_PLAYLIST).format(filelabel, selected_playlist.label))
    except Exception as e:
        log(traceback.format_exc(), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(L(TranslationKey.ERROR), "%s" % e, icon=xbmcgui.NOTIFICATION_ERROR)