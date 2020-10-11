# Add To Playlist
A Kodi add-on that allows users to add any video to an existing m3u playlist.

Currently Kodi support for static playlist is awkward to use, specially when editing
playlists. The main problem is that there is no quick way to add an item to a 
playlist while browing the library; the user has to queue the item first and hop
through some dialogs. The objective of this addon is to make that process easier.

This addon will add an "Add to playlist" context menu item to playable items 
(such as videos). The user can then select an existing playlist or create a new
one. The addon will save the playlist by placing the selected video at the end of it.

Currently only m3u static playlists are supported.

To install, download the code, create a zip file and install from zip file. As
this addon turns stable, I will consider submitting to the official Kodi repo.

Can be found on github script.addtoplaylist: https://github.com/bluefoot/script.addtoplaylist

## Acknowledgments 
Development of this addon was highly based on rmrector's playrandomvideos 
script: https://github.com/rmrector/script.playrandomvideos/

## Future work
- Fix bug where context menu is being shown on items other than single playable videos
- Research and decide if items of a playlist should be saved as absolute system 
paths or Kodi's file URL notation
- Add a context menu to allow the user to remove an item from an existing static playlist
- Support for other types of playlists other than m3u
