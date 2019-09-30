init -999 python:
    import datetime
    _persist = renpy.game.persistent

    ev_dat = _persist.event_database.get("awc_monika_player_location")

    if ev_dat and ev_dat[14] and ev_dat[14].date() < datetime.date(2019, 9, 30):
        _persist.event_database.pop("awc_monika_player_location")

    try:
        del _persist._mas_API_key
        del _persist._awc_player_coords_flag
    except:
        pass

init 999 python:
    #Delete this
    store.mas_utils.trydel(renpy.config.basedir + "/" + renpy.get_filename_line()[0])
    store.mas_utils.trydel(renpy.config.basedir + "/" + renpy.get_filename_line()[0] + 'c')
