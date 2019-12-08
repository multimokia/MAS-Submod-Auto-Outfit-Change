#Default this var so it works
default persistent._music_playlist_mode = False

#Add the label into the restart blacklist
init 1 python:
    evhand.RESTART_BLKLST.append('monika_welcome_home')

#START: Topic/Labels
init 50 python:
    #Reset ev
    home_ev = mas_getEV('monika_welcome_home')
    home_ev.conditional=(
        "not mas_isMorning() "
        "and not persistent.current_track"
    )
    home_ev.action=EV_ACT_QUEUE

    #Don't need this anymore, delet
    del home_ev

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_welcome_home",
            conditional=(
                "not mas_isMorning() "
                "and not persistent.current_track"
            ),
            action=EV_ACT_QUEUE,
            rules={"skip alert": None}
        )
    )


label monika_welcome_home:
    #Sanity check this since for whatever reason this conditional runs anyway.
    if not mas_isMorning() or persistent.current_track:
        #Set up the notif
        $ display_notif(m_name,["Hey [player]..."],"Topic Alerts")

        #Set up a docking station and get a list of ogg files
        python:
            nightMusicStation = store.MASDockingStation(renpy.config.basedir+"/nightmusic/")
            listOgg = nightMusicStation.getPackageList(".ogg") + nightMusicStation.getPackageList(".mp3")

        #Ensure list actually has things in it
        if len(listOgg) > 0:
            $ song = (nightMusicStation.station + random.choice(listOgg)).replace("\\","/")
        else:
            #Don't show this if there's nothing in there to pick
            return

        m 1eka "Hey [player]..."
        m 3eka "Now that we're home together, I'm going to put on a song for us to relax to.{w=0.5}.{w=0.5}.{nw}"

        $ play_song(song, fadein=3.0)

        m 1hua "There we go."
        show monika 5eubla at t11 zorder MAS_MONIKA_Z with dissolve
        m 5eubla "Let's have a relaxing evening together, [player]."

    else:
        #Reset ev if not night
        $ home_ev = mas_getEV('monika_welcome_home')
        $ home_ev.conditional=(
            "not mas_isMorning() "
            "and not persistent.current_track"
        )
        $ home_ev.action=EV_ACT_QUEUE

        #Fix the shown count
        $ home_ev.shown_count -= 1
        #Don't need this anymore, delet
        $ del home_ev
    return

#START: zz_music_selector.rpy overrides
init python in songs:
    import os
    import mutagen.mp3 as muta3
    import mutagen.oggopus as mutaopus
    import mutagen.oggvorbis as mutaogg
    import store

    def getFilesByType(station,ext):
        import os
        return [
            (station + "/" + package).replace("\\","/")
            for package in os.listdir(station)
            if package.endswith(ext)
        ]



    NIGHTMUSIC = "Nightmusic"
    FP_NIGHTMUSIC = "nightmusic"

    def initMusicChoices(sayori=False):
        #
        # Sets up the music choices list
        #
        # IN:
        #   sayori - True if the player name is sayori, which means only
        #       allow Surprise in the player

        global music_choices
        global music_pages
        music_choices = list()
        # SONGS:
        # if you want to add a song, add it to this list as a tuple, where:
        # [0] -> Title of song
        # [1] -> Path to song
        if not sayori:
            music_choices.append((JUST_MONIKA, FP_JUST_MONIKA))
            music_choices.append((YOURE_REAL, FP_YOURE_REAL))

            # Shoutout to Rune0n for this wonderful piano cover!
            music_choices.append((PIANO_COVER, FP_PIANO_COVER))

            # Shoutout to TheAloofPotato for this wonderful eurobeat version!
            music_choices.append((YR_EUROBEAT, FP_YR_EUROBEAT))

            #music_choices.append((KAZOO_COVER, FP_KAZOO_COVER)) Fuck right off
            music_choices.append((STILL_LOVE, FP_STILL_LOVE))
            music_choices.append((MY_FEELS, FP_MY_FEELS))
            music_choices.append((MY_CONF, FP_MY_CONF))
            music_choices.append((OKAY_EV_MON, FP_OKAY_EV_MON))
            music_choices.append((PLAYWITHME_VAR6, FP_PLAYWITHME_VAR6))

            # BIG SHOUTOUT to HalHarrison for this lovely track!
            music_choices.append((DDLC_MT_80, FP_DDLC_MT_80))

            #And the nightmusic
            music_choices.append((NIGHTMUSIC, FP_NIGHTMUSIC))

            # NOTE: this is locked until we can set this up later.
#            music_choices.append((MONIKA_LULLABY, FP_MONIKA_LULLABY))

        # sayori only allows this
        if store.persistent._mas_sensitive_mode:
            sayonara_name = SAYO_NARA_SENS
        else:
            sayonara_name = SAYO_NARA
        music_choices.append((sayonara_name, FP_SAYO_NARA))

        # grab custom music
        __scanCustomBGM(music_choices)

        # separte the music choices into pages
        music_pages = __paginate(music_choices)

    def __paginate(music_list):
        """
        Paginates the music list and returns a dict of the pages.

        IN:
            music_list - list of music choice tuples (see initMusicChoices)

        RETURNS:
            dict of music choices, paginated nicely:
            [0]: first page of music
            [1]: next page of music
            ...
            [n]: last page of music
        """
        pages_dict = dict()
        page = 0
        leftovers = music_list
        while len(leftovers) > 0:
            music_page, leftovers = __genPage(leftovers)
            pages_dict[page] = music_page
            page += 1

        return pages_dict


    def __genPage(music_list):
        """
        Generates the a page of music choices

        IN:
            music_list - list of music choice tuples (see initMusicChoices)

        RETURNS:
            tuple of the following format:
                [0] - page of the music choices
                [1] - reamining items in the music_list
        """
        return (music_list[:PAGE_LIMIT], music_list[PAGE_LIMIT:])


    def __scanCustomBGM(music_list):
        """
        Scans the custom music directory for custom musics and adds them to
        the given music_list.

        IN/OUT:
            music_list - list of music tuples to append to
        """
        # TODO: make song names / other tags configurable

        # No custom directory? abort
        if not os.access(custom_music_dir, os.F_OK):
            return

        # get the oggs
        found_files = os.listdir(custom_music_dir)
        found_oggs = [
            ogg_file
            for ogg_file in found_files # these are not all just oggs.
            if (
                isValidExt(ogg_file)
                and os.access(custom_music_dir + ogg_file, os.R_OK)
            )
        ]

        if len(found_oggs) == 0:
            # no custom songs found, please move on
            return

        # otherwise, we got some songs to add
        for ogg_file in found_oggs:
            # time to tag
            filepath = custom_music_dir + ogg_file

            _audio_file, _ext = _getAudioFile(filepath)

            if _audio_file is not None:
                # we only care if we even have an audio file
                disp_name = _getDispName(_audio_file, _ext, ogg_file)

                # loop prefix
                loop_prefix = _getLoopData(_audio_file, _ext)

                # add to the menu
                music_list.append((
                    cleanGUIText(disp_name),
                    loop_prefix + custom_music_reldir + ogg_file
                ))

                # we added something!
                store.persistent._mas_pm_added_custom_bgm = True

#START: Music Menu Section
init 1 python:
    def select_music():
        # check for open menu
        if songs.enabled and not songs.menu_open:

            # disable unwanted interactions
            mas_RaiseShield_mumu()

            # music menu label
            selected_track = renpy.call_in_new_context("display_music_menu_ov")
            if selected_track == songs.NO_SONG:
                selected_track = songs.FP_NO_SONG

            # workaround to handle new context
            if selected_track == songs.FP_NIGHTMUSIC:
                #Set up the stations
                nightMusicStation = store.MASDockingStation(renpy.config.basedir+"/nightmusic/")
                listOgg = songs.getFilesByType(nightMusicStation.station,".mp3") + songs.getFilesByType(nightMusicStation.station,".ogg")

                #Ensure list actually has things in it
                if len(listOgg) > 0:
                    #We want to loop through all songs in the list
                    if persistent._music_playlist_mode:
                        renpy.random.shuffle(listOgg)
                        play_song(listOgg)

                    #We just want it in single song mode
                    else:
                        song = random.choice(listOgg)
                        play_song(song)

            elif selected_track != songs.current_track:
                play_song(selected_track, set_per=True)

            # unwanted interactions are no longer unwanted
            if store.mas_globals.dlg_workflow:
                # the dialogue workflow means we should only enable
                # music menu interactions
                mas_MUMUDropShield()

            elif store.mas_globals.in_idle_mode:
                # to idle
                mas_mumuToIdleShield()

            else:
                # otherwise we can enable interactions normally
                mas_DropShield_mumu()

#START: Music Menu Override
# MUSIC MENU ##################################################################
# This is the music selection menu
###############################################################################

# here we are copying game_menu's layout

#style music_menu_outer_frame is empty
#style music_menu_navigation_frame is empty
#style music_menu_content_frame is empty
#style music_menu_viewport is gui_viewport
#style music_menu_side is gui_side
#style music_menu_scrollbar is gui_vscrollbar

#style music_menu_label is gui_label
#style music_menu_label_text is gui_label_text

#style music_menu_return_button is navigation_button
style music_menu_return_button_text is navigation_button_text
style music_menu_prev_button_text is navigation_button_text:
    min_width 135
    text_align 1.0

style music_menu_outer_frame is game_menu_outer_frame
style music_menu_navigation_frame is game_menu_navigation_frame
style music_menu_content_frame is game_menu_content_frame
style music_menu_viewport is game_menu_viewport
style music_menu_side is game_menu_side
style music_menu_label is game_menu_label
style music_menu_label_text is game_menu_label_text

style music_menu_return_button is return_button:
    xminimum 0
    xmaximum 200
    xfill False

style music_menu_prev_button is return_button:
    xminimum 0
    xmaximum 135
    xfill False

style music_menu_outer_frame:
    background "mod_assets/music_menu.png"

style music_menu_button is navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")
    hover_sound gui.hover_sound
    activate_sound gui.activate_sound

style music_menu_button_text is navigation_button_text:
    properties gui.button_text_properties("navigation_button")
    font "mod_assets/font/mplus-2p-regular.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]


# Music menu 
#
# IN:
#   music_page - current page of music
#   page_num - current page number
#   more_pages - true if there are more pages left
#
screen music_menu_ov(music_page, page_num=0, more_pages=False):
    modal True

    $ import store.songs as songs

    # logic to ensure Return works
    if songs.current_track is None:
        $ return_value = songs.NO_SONG
    else:
        $ return_value = songs.current_track


    # allows the music menu to quit using hotkey
    key "noshift_M" action Return(return_value)
    key "noshift_m" action Return(return_value)

    zorder 200

    style_prefix mas_ui.mms_style_prefix

    frame:
        hbox:
            # dynamic prevous text, so we can keep button size alignments
            if page_num > 0:
                textbutton _("<<<< Prev"):
                    style mas_ui.mms_button_prev_style
                    action Return(page_num - 1)

            else:
                textbutton _( " "):
                    style mas_ui.mms_button_prev_style
                    sensitive False

            if more_pages:
                textbutton _("Next >>>>"):
                    style mas_ui.mms_button_return_style
                    action Return(page_num + 1)
        style mas_ui.mms_frame_outer_style

        hbox:

            frame:
                style mas_ui.mms_frame_navigation_style

            frame:
                style mas_ui.mms_frame_content_style

                transclude

        # this part copied from navigation menu
        vbox:
            style_prefix mas_ui.mms_style_prefix

            xpos gui.navigation_xpos
    #        yalign 0.4
            spacing gui.navigation_spacing

            # wonderful loop so we can dynamically add songs
            for name,song in music_page:
                textbutton _(name) action Return(song)

            vbox:
                style_prefix mas_ui.cbx_style_prefix
                textbutton _("Playlist Mode"):
                    action ToggleField(persistent, "_music_playlist_mode")
                    selected persistent._music_playlist_mode

    vbox:
        yalign 1.0

        textbutton _(songs.NO_SONG):
            style mas_ui.mms_button_return_style
            action Return(songs.NO_SONG)

        textbutton _("Return"):
            style mas_ui.mms_button_return_style
            action Return(return_value)

    label "Music Menu"


# sets locks and calls the appropriate screen
label display_music_menu_ov:
    # set var so we can block multiple music menus
    python:
        import store.songs as songs
        songs.menu_open = True
        song_selected = False
        curr_page = 0

    # loop until we've selected a song
    while not song_selected:

        # setup pages
        $ music_page = songs.music_pages.get(curr_page, None)

        if music_page is None:
            # this should never happen. Immediately quit with None
            return songs.NO_SONG

        # otherwise, continue formatting args
        $ next_page = (curr_page + 1) in songs.music_pages

        call screen music_menu_ov(music_page, page_num=curr_page, more_pages=next_page)

        # obtain result
        $ curr_page = _return

        python:
            try:
                song_selected = _return not in songs.music_pages
            except:
                #We know that this was nightmusic on playlist mode, so a song was selected then
                song_selected = True

    $ songs.menu_open = False
    return _return
