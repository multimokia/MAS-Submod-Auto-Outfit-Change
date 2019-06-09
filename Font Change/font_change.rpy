#START: Styledefs
#Create these styles to be used later
init -1 style journal_monika is normal:
    font "gui/font/m1.ttf"
    size 30

init -1 style journal_monika_slow is default_monika:
    font "gui/font/m1.ttf"
    size 30

init -1 python:
    style.hyperlink_text.font = "gui/font/m1.ttf"
    style.hyperlink_text.size = 30


#START: Overrides
#These are used in place of the ones in script-ch30.rpy so we get our custom font
init 6 python:
    def mas_enableTextSpeed():
        """
        Enables text speed
        """
        style.say_dialogue = style.journal_monika
        store.mas_globals.text_speed_enabled = True

    def mas_disableTextSpeed():
        """
        Disables text speed
        """
        style.say_dialogue = style.journal_monika_slow
        store.mas_globals.text_speed_enabled = False


#Screens override, so it uses Moni's font
screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport")):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                text h.what.replace("[","[[")

        if not _history_list:
            label _("The dialogue history is empty.")


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    font "gui/font/m1.ttf"
    size 31
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    font "gui/font/m1.ttf"
    size 31
    xpos gui.history_text_xpos + 3
    ypos gui.history_text_ypos - 5
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5