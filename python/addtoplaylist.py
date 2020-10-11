import os, sys, traceback
import xbmc, xbmcaddon, xbmcgui
from playlists import PlaylistService, Playlist
addon = xbmcaddon.Addon()
addonpath = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(addonpath, u'python', u'lib'))
from pykodi import log, localize as L

SELECT_A_PLAYLIST = 372010
ERROR = 257
SUCCESS = 372011
ADDED_FILE_TO_PLAYLIST = 372014
CREATE_NEW_PLAYLIST = 372013
NEW_PLAYLIST_NAME = 372012

playlist_service = PlaylistService()

def _prompt_user_to_create_new_playlist():
    playlist_name = xbmcgui.Dialog().input(L(NEW_PLAYLIST_NAME)).strip()
    if playlist_name:
        return playlist_service.create_empty_playlist(playlist_name)

def _prompt_user_to_select_playlist(playlists):
    add_new_playlist_item = Playlist(label = L(CREATE_NEW_PLAYLIST))
    selectable_items = [add_new_playlist_item] + playlists
    selected_playlist_index = xbmcgui.Dialog().select(L(SELECT_A_PLAYLIST), [playlist.label for playlist in selectable_items])
    if selected_playlist_index == 0:
        return _prompt_user_to_create_new_playlist()
    adjusted_index = selected_playlist_index - 1
    return playlists[adjusted_index] if adjusted_index >= 0 else None

def add_to_playlist(filename, filelabel):
    try:
        playlists = playlist_service.get_all_supported_playlists()
        selected_playlist = _prompt_user_to_select_playlist(playlists)
        if selected_playlist is not None:
            playlist_service.add_file_to_playlist(selected_playlist, filename, filelabel)
            xbmcgui.Dialog().notification(L(SUCCESS), L(ADDED_FILE_TO_PLAYLIST).format(filelabel, selected_playlist.label))
    except Exception as e:
        log(traceback.format_exc(), xbmc.LOGERROR)
        xbmcgui.Dialog().notification(L(ERROR), "%s" % e, icon=xbmcgui.NOTIFICATION_ERROR)