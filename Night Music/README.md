### General:
Adds a new music folder (`nightmusic`, in the DDLC directory) in which you can put songs (`.mp3` or `.ogg`) that Monika can pick from to play in the evening (assuming there's no music playing already)

### Some Nitty Gritty:
NOTE: Music menu has a new button, and the `prev`/`next` page options are on the top of the menu. `Playlist Mode` only works for the `Nightmusic` option.

It is possible to set songs to have a conditional. Simply put the condition (as python code) into the `genre` field of the song.

Example, if you wanted one song to only be picked during the d25 season, add `store.mas_isD25Season()` in. (Exceptions are logged)