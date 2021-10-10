"""
This file contains code adapted from 
rmrector's playrandomvideos: https://github.com/rmrector/script.playrandomvideos/
"""
import collections
import json
from urllib.parse import urlparse
import xbmc
import xbmcaddon

_main_addon = None
def get_main_addon():
    global _main_addon
    if not _main_addon:
        _main_addon = xbmcaddon.Addon()
    return _main_addon

def localize(messageid):
    if isinstance(messageid, str):
        return messageid
    if messageid >= 371000 and messageid < 373000:
        return get_main_addon().getLocalizedString(messageid)
    return xbmc.getLocalizedString(messageid)

def execute_jsonrpc(jsonrpc_command):
    if isinstance(jsonrpc_command, dict):
        jsonrpc_command = json.dumps(jsonrpc_command)

    json_result = xbmc.executeJSONRPC(jsonrpc_command)
    return json.loads(json_result)

ignoredtypes = ('', 'addons', 'sources', 'plugin')
def get_pathinfo(path):
    result = {}
    if path.startswith('/') or '://' not in path:
        path_type = 'other'
        query = None
    else:
        path_type, db_path = path.split('://', 1)
        db_path = db_path.split('?', 1)
        query = parse_qs(db_path[1]) if len(db_path) > 1 else None
        db_path = db_path[0].rstrip('/').split('/')
        result['path'] = db_path

    if path_type in ignoredtypes:
        return
    if query and query.get('xsp'):
        try:
            query['xsp'] = json.loads(query['xsp'][0])
        except ValueError:
            del query['xsp']

    result['type'] = path_type
    if query:
        result['query'] = query

    return result

def log(message, level=xbmc.LOGDEBUG):
    if not isinstance(message, str):
        message = json.dumps(message, cls=LogJSONEncoder)

    file_message = '[%s] %s' % (get_main_addon().getAddonInfo('id'), message)
    xbmc.log(file_message, level)

class LogJSONEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        kwargs['skipkeys'] = True
        kwargs['ensure_ascii'] = False
        kwargs['indent'] = 2
        kwargs['separators'] = (',', ': ')
        super(LogJSONEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        if isinstance(obj, collections.Mapping):
            return dict((key, obj[key]) for key in obj.keys())
        if isinstance(obj, collections.Iterable):
            return list(obj)
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)

