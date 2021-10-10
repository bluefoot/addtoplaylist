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

Can be found on github script.addtoplaylist: https://github.com/bluefoot/script.addtoplaylist.

## Installation
- Head over to the [latest releases page](https://github.com/bluefoot/addtoplaylist/releases/latest)
and download the addon package file.
- In Kodi, select Add-ons > Install from zip file. Browse the previously downloaded
file and follow the on-screen prompts to install it.

## Build
Simply zip the contents of the branch. There is a `build.sh` utility that can be used.

## Acknowledgments 
Development of this addon was highly based on rmrector's playrandomvideos 
script: https://github.com/rmrector/script.playrandomvideos/.

## Future work
- Add a context menu to allow the user to remove an item from an existing static playlist.
- Fix bug where context menu is being shown on items other than single playable videos.
- Research and decide if items of a playlist should be saved as absolute system.
paths or Kodi's file URL notation.
- Support for other types of playlists other than m3u.
