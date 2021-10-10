import re
import xbmc, xbmcvfs
from lib.pykodi import log

class FileManager(object):
    def _read_file(self, file_name):
        f = None
        try:
            f = xbmcvfs.File(file_name)
            return f.read().replace('\n\n', '\n')
        finally:
            if f:
                f.close()

    def _get_list(self, address):
        return self._read_file(address)

    @staticmethod
    def supports(filename):
        raise NotImplementedError("supports not implemented!")
    
class M3uFileManager(FileManager):
    @staticmethod
    def supports(filename):
        return 'm3u' in filename

    def load_playlist(self, url):
        raw_file_contents = self._get_list(url)
        matches = re.compile('^#EXTINF:-?[0-9]*(.*?),([^\"]*?)\n(.*?)$', re.M).findall(raw_file_contents)
        return [PlaylistItem(display_name.strip(), url.strip()) for params, display_name, url in matches]

    def save_playlist(self, playlist, playlist_items):
        filename = playlist.file
        f = None
        try:
            f = xbmcvfs.File(filename,'w')
            data = '#EXTCPlayListM3U::M3U\n'
            for item in playlist_items:
                data += '#EXTINF:0,%s\n' % item.display_name
                data += '%s\n' % item.url
            log('Saving into playlist file %s the following contents:\n%s' % (filename, data), xbmc.LOGDEBUG)
            f.write(bytearray(data, 'utf_8'))
        finally:
            if f:
                f.close()

class PlaylistItem(object):
    def __init__(self, display_name, url):
        self.display_name = display_name
        self.url = url

    def __str__(self):
        return 'PlaylistItem(display_name=%s, url=%s)' % (self.display_name, self.url)

    def __repr__(self):
        return '{display_name:%s, url:%s}' % (self.display_name, self.url)