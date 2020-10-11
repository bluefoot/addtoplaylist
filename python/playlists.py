import os, sys
from files import M3uFileManager, PlaylistItem
import xbmcaddon, xbmc
addon = xbmcaddon.Addon()
addonpath = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(addonpath, u'python', u'lib'))
import pykodi
from pykodi import log

class PlaylistService(object):
    NEW_PLAYLIST_BASE_DIR = 'special://profile/playlists/video/'

    def __init__(self):
        self.file_managers = [M3uFileManager]
    
    def get_all_playlists(self):
        json_request = {
            'jsonrpc': '2.0', 
            'method': 'Files.GetDirectory', 
            'params': {'directory': 'special://videoplaylists'}, 
            'id': 1
        }
        json_result = pykodi.execute_jsonrpc(json_request)
        if self._check_json_result(json_result, 'files', json_request):
            playlists = [self._convert_json_to_playlist(json_playlist) for json_playlist in json_result['result']['files']]
            log("Loaded playlists:\n%s" % playlists, xbmc.LOGDEBUG)
            return playlists
        else:
            return []

    def get_all_supported_playlists(self):
        all_playlists = self.get_all_playlists()
        return self._filter_out_unsupported_playlists(all_playlists)

    def add_file_to_playlist(self, playlist, filename_to_add, label):
        file_manager = self._get_filemanager_for_playlist_type(playlist)
        if file_manager is None:
            raise Exception('Playlist file %s of playlist %s not supported' % (playlist.file, playlist.label))
        playlist_items = file_manager.load_playlist(playlist.file)
        playlist_items.append(PlaylistItem(label, filename_to_add))
        file_manager.save_playlist(playlist, playlist_items)

    def create_empty_playlist(self, playlist_name):
        file_name = playlist_name
        if not file_name.endswith('m3u'):
            file_name += '.m3u'
        new_playlist = Playlist(file = self.NEW_PLAYLIST_BASE_DIR + file_name, label = playlist_name)
        return new_playlist

    def _check_json_result(self, json_result, result_key, json_request):
        if 'error' in json_result:
            raise JSONException(json_request, json_result)

        return 'result' in json_result and (not result_key or result_key in json_result['result'])

    def _convert_json_to_playlist(self, pl):
        return Playlist(pl['filetype'], pl['type'], pl['file'], pl['label'])

    def _filter_out_unsupported_playlists(self, playlists):
        return filter(lambda p: self._get_filemanager_for_playlist_type(p) is not None, playlists)
    
    def _get_filemanager_for_playlist_type(self, playlist):
        for manager in self.file_managers:
            if manager.supports(playlist.file):
                return manager()

class Playlist(object):
    def __init__(self, filetype = None, type = None, file = None, label = None):
        self.filetype = filetype
        self.type = type
        self.file = file
        self.label = label

    def __str__(self):
        return 'Playlist(filetype=%s, type=%s, file=%s, label=%s)' % (self.filetype, self.type, self.file, self.label)

    def __repr__(self):
        return '{filetype:%s, type:%s, file:%s, label:%s}' % (self.filetype, self.type, self.file, self.label) 

class JSONException(Exception):
    def __init__(self, json_request, json_result):
        self.json_request = json_request
        self.json_result = json_result

        message = "There was an error with a JSON-RPC request.\nRequest: "
        message += json.dumps(json_request, cls=pykodi.LogJSONEncoder)
        message += "\nResult: "
        message += json.dumps(json_result, cls=pykodi.LogJSONEncoder)

        super(JSONException, self).__init__(message)
