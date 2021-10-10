import sys
import addtoplaylist

if __name__ == '__main__':
    path = sys.listitem.getPath()
    label = sys.listitem.getLabel()

    if path and label:
        addtoplaylist.add_to_playlist(path, label)
