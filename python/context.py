import sys
import addtoplaylist

def _generate_label(listitem):
    videotitle = listitem.getVideoInfoTag().getTitle()
    tvshowtitle = listitem.getVideoInfoTag().getTVShowTitle()
    if tvshowtitle:
        return "%s - %s" % (tvshowtitle, videotitle)
    return videotitle

if __name__ == '__main__':
    path = sys.listitem.getVideoInfoTag().getFilenameAndPath()
    label = _generate_label(sys.listitem)

    if path and label:
        addtoplaylist.add_to_playlist(path, label)
