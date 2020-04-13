init -990 python in mas_submod_utils:
    Submod(
        author="multimokia",
        name="Auto Hair Change",
        description="A submod which allows Monika to pick her own hairstyles for day and night.",
        version="2.3.1",
        version_updates={
            "multimokia_auto_hair_change_v2_3_0": "multimokia_auto_hair_change_v2_3_1"
        },
        settings_pane="auto_hair_change_settings_screen"
    )

init -1 python:
    layout.AHC_UJ_WHEN = (
        "Use this to migrate your hair jsons to work with this submod. "
        "You should only really need to do this if you just updated and/or reinstalled sprite jsons."
    )

#START: Settings pane
screen auto_hair_change_settings_screen():
    default tooltip = Tooltip("")
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000

        hbox:
            style_prefix mas_ui.cbx_style_prefix
            box_wrap False

            textbutton _("Update Jsons"):
                action Function(store.ahc_utils.__updateJsons)
                hovered tooltip.Action(layout.AHC_UJ_WHEN)

    text tooltip.value:
        xalign 0 yalign 1.0
        xoffset 300 yoffset -10
        style "main_menu_version"

#START: Update scripts
label multimokia_auto_hair_change_v2_3_0(version="v2_3_0"):
    return

label multimokia_auto_hair_change_v2_3_1(version="v2_3_1"):
    $ ahc_utils.__updateJsons()
    return

default persistent._ahc_last_set_hair = {
    "day": None,
    "night": None
}

#Fix for the removal of Rin
init python:
    mas_clothes_rin = None

init python in ahc_utils:
    import store
    import datetime

    #Reset force hair, so we can have Moni set her own hair next sesh
    store.persistent._mas_force_hair = False

    __BUILTIN_DAY_HAIR = [
        store.mas_hair_def,
        store.mas_hair_downtiedstrand
    ]

    __BUILTIN_NIGHT_HAIR = [
        store.mas_hair_down,
        store.mas_hair_downtiedstrand
    ]

    def __updateJsons():
        """
        Updates the jsons to add ex_props for this submod
        Additionally, will update sprites for runtime as well
        """
        import json

        JSON_PATH = "mod_assets/monika/j/"

        #filename: {ex_prop: value}
        json_update_map = {
            "orcaramelo_hair_bunbraid.json": {"day": True},
            "orcaramelo_hair_ponytailbraid.json": {"day": True},
            "orcaramelo_hair_twintails.json": {"day": True},
            "orcaramelo_hair_twinbun.json": {"day": True},
            "orcaramelo_hair_usagi.json": {"day": True}
        }

        for json_filename, added_ex_props in json_update_map.iteritems():
            if renpy.loadable(JSON_PATH + json_filename):
                with open("{0}/{1}{2}".format(renpy.config.gamedir, JSON_PATH, json_filename)) as jfile:
                    json_data = json.load(jfile)

                    #If there is no expsting ex_props field, we shoud create it
                    if "ex_props" not in json_data:
                        json_data["ex_props"] = dict()

                    #Now add the new data
                    json_data["ex_props"].update(added_ex_props)

                    #Now we want to update the runtime variant
                    hair_sprobj = store.mas_sprites.get_sprite(1, json_data["name"])
                    if hair_sprobj:
                        hair_sprobj.ex_props.update(added_ex_props)

                with open("{0}/{1}{2}".format(renpy.config.gamedir, JSON_PATH, json_filename), "w") as jfile:
                    #Now write the new json
                    json.dump(json_data, jfile, indent=4, sort_keys=True)


    def __compatibleOnly(hair_list):
        """
        Filters the given list to only return the MASHair objects which are compatible with the current clothes

        IN:
            hair_list:
                list() of MASHair objects which need to be filtered

        OUT:
            list() of MASHair objects which are compatible with the current outfit

        NOTE: Does NOT check if unlocked
        """
        return [
            hair
            for hair in hair_list
            if store.mas_sprites.is_clotheshair_compatible(store.monika_chr.clothes, hair)
        ]

    def getDayHair():
        """
        Gets day hair

        OUT:
            list() of unlocked MASHair objects which are suited for day and are compatible with the current clothes
        """
        global __BUILTIN_DAY_HAIR

        return __compatibleOnly([
            hair.get_sprobj()
            for hair in store.mas_selspr.filter_hair(True)
            if "day" in hair.get_sprobj().ex_props
            ] + __BUILTIN_DAY_HAIR
        )

    def getNightHair():
        """
        Gets night hair

        OUT:
            list() of unlocked MASHair objects which are suited for night and are compatible with the current clothes
        """
        global __BUILTIN_NIGHT_HAIR

        return __compatibleOnly([
            hair.get_sprobj()
            for hair in store.mas_selspr.filter_hair(True)
            if "night" in hair.get_sprobj().ex_props
            ] + __BUILTIN_NIGHT_HAIR
        )

    def isWearingDayHair():
        """
        Checks if Monika is wearing day hair

        OUT:
            boolean:
                True if Monika is wearing day hair
                False otherwise
        """
        global __BUILTIN_DAY_HAIR

        return (
            "day" in store.monika_chr.hair.ex_props
            or store.monika_chr.hair in __BUILTIN_DAY_HAIR
        )

    def isWearingNightHair():
        """
        Checks if Monika is wearing night hair

        OUT:
            boolean:
                True if Monika is wearing night hair
                False otherwise
        """
        global __BUILTIN_NIGHT_HAIR

        return (
            "night" in store.monika_chr.hair.ex_props
            or store.monika_chr.hair in __BUILTIN_NIGHT_HAIR
        )

    def has_and_unlocked(acs_name):
        """
        Returns True if we have the acs and it's unlocked
        """
        return acs_name in store.mas_selspr.ACS_SEL_MAP and store.mas_selspr.ACS_SEL_MAP[acs_name].unlocked

    def lastSeenOnDay(ev_label, _date=None):
        """
        Checks if the ev_label's event was last seen on _date

        IN:
            ev_label:
                The eventlabel of the event we want to check
            _date:
                Date we want to see if ev_label was last seen on
                If None, today is assumed
                (Default: None)

        OUT:
            boolean:
                True if last seen on _date
                False otherwise
        """
        #NOTE: This try/except is for use of this function in event conditionals
        #Since mas_getEV doesn't exist until init 6
        try:
            ev = store.mas_getEV(ev_label)
        except:
            ev = None

        #If the event doesn't exist, return None to note it
        if not ev:
            return None

        #No last seen means we know it wasn't seen on the date
        elif not ev.last_seen:
            return False

        #Otherwise let's do some work
        if _date is None:
            _date = datetime.date.today()

        #Otherwise let's check
        return ev.last_seen.date() == _date

    def hasHairDownRun():
        """
        Checks whether or not monika_sethair_down has run in the current night period or not.

        CONDITIONS:
            1) We haven't seen the label today
                - and current time is between sunset and midnight
                - or current time is between midnight and sunrise and we haven't seen the label yesterday between sunset and midnight
            2) We have seen the label today and
                - Current time is between sunset and midnight
                - and the last time we saw the label was between midnight and sunrise

        OUT:
            boolean:
                True if monika_sethair_down has run in the current night period
                False otherwise
        """
        #NOTE: This try/except is for use of this function in event conditionals
        #Since mas_getEV doesn't exist until init 6
        try:
            ev = store.mas_getEV("monika_sethair_down")
        except:
            ev = None

        #If we don't have the ev, we return None to note it
        if not ev:
            return None

        #If we've not seen it before, we know it hasn't run and don't need to do more work
        elif not ev.last_seen:
            return False

        _now = datetime.datetime.now()
        yesterday = datetime.date.today() - datetime.timedelta(1)

        return (
            (
                not lastSeenOnDay("monika_sethair_down")
                and (
                    store.mas_isSStoMN(_now)
                    or (
                        store.mas_isMNtoSR(_now)
                        and not (lastSeenOnDay("monika_sethair_down", yesterday)
                        and store.mas_isSStoMN(ev.last_seen))
                    )
                )
            )
            or (
                lastSeenOnDay("monika_sethair_down")
                and store.mas_isSStoMN(_now)
                and store.mas_isMNtoSR(ev.last_seen)
            )
        )

init 999 python in ahc_utils:
    @store.mas_submod_utils.functionplugin("bye_going_somewhere_rtg")
    def getReady():
        """
        Gets Monika ready for a date
        """
        #Make hair is either what player asked, or Moni's choice
        if (
            (not store.persistent._mas_force_hair or store.monika_chr.is_wearing_clothes_with_exprop("costume"))
            and not isWearingDayHair()
        ):
            store.monika_chr.change_hair(renpy.random.choice(getDayHair()), by_user=False)

            #We'll wear a ribbon if it's a special day and we're able to force
            if store.mas_isSpecialDay():
                if (
                    has_and_unlocked("multimokia_bow_black")
                    and not store.monika_chr.is_wearing_hair_with_exprop("twintails")
                ):
                    store.mas_sprites._acs_wear_if_found(store.monika_chr, "multimokia_bow_black")

                elif has_and_unlocked("ribbon_black"):
                    store.monika_chr.wear_acs(mas_acs_ribbon_black)

                else:
                    store.monika_chr.wear_acs(mas_acs_ribbon_def)

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_ponytail",
            conditional=(
                "mas_isMorning() "
                "and not store.persistent._mas_force_hair "
                "and ((len(store.ahc_utils.getDayHair()) > 1 "
                "and store.ahc_utils.isWearingDayHair() and store.ahc_utils.isWearingNightHair()) "
                "or not store.ahc_utils.isWearingDayHair()) "
                "and mas_timePastSince(persistent._ahc_last_set_hair['day'], datetime.timedelta(hours=12))"
            ),
            action=EV_ACT_PUSH,
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label monika_sethair_ponytail:
    if ahc_utils.lastSeenOnDay("monika_sethair_ponytail"):
        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 3eua "I'm going to change my hairstyle, I'll be right back.{w=0.5}.{w=0.5}.{w=2}{nw}"
        else:
            m 1esa "Give me a moment, [player]."
            m 1eua "I'm just going to change my hairstyle a little bit.{w=0.5}.{w=0.5}.{nw}"

    else:
        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 3eua "I'm going to get ready for today.{w=0.5}.{w=0.5}.{w=2}{nw}"

        else:
            m 1eua "Give me a second, [player]."
            m 3eua "I'm just getting myself ready for the day.{w=0.5}.{w=0.5}.{nw}"

    window hide
    call mas_transition_to_emptydesk

    python:
        renpy.pause(3.0, hard=True)

        day_hair_list = ahc_utils.getDayHair()

        if ahc_utils.isWearingDayHair():
            day_hair_list.remove(monika_chr.hair)

        monika_chr.change_hair(
            renpy.random.choice(day_hair_list),
            by_user=False
        )

        thermos_acs = monika_chr.get_acs_of_type("thermos-mug")

        if thermos_acs:
            monika_chr.remove_acs(thermos_acs)
            mas_rmallEVL("mas_consumables_remove_thermos")

        renpy.pause(2.0, hard=True)

        persistent._ahc_last_set_hair["day"] = datetime.datetime.now()

    call mas_transition_from_emptydesk("monika 3hub")
    window auto

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3hub "All done!{w=1}{nw}"

    else:
        m 3hub "All done!"
        m 1eua "If you want me to change my hairstyle, just ask, okay?"

    #Need to recondition/action this
    python:
        hairup_ev = mas_getEV("monika_sethair_ponytail")

        hairup_ev.conditional=(
            "mas_isMorning() "
            "and not store.persistent._mas_force_hair "
            "and ((len(store.ahc_utils.getDayHair()) > 1 "
            "and store.ahc_utils.isWearingDayHair() and store.ahc_utils.isWearingNightHair()) "
            "or not store.ahc_utils.isWearingDayHair()) "
            "and mas_timePastSince(persistent._ahc_last_set_hair['day'], datetime.timedelta(hours=12))"
        )
        hairup_ev.action = EV_ACT_PUSH
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_down",
            conditional=(
                "not mas_isMorning() "
                "and not store.persistent._mas_force_hair "
                "and ((len(store.ahc_utils.getNightHair()) > 1 "
                "and store.ahc_utils.isWearingNightHair() and store.ahc_utils.isWearingDayHair()) "
                "or not store.ahc_utils.isWearingNightHair()) "
                "and mas_timePastSince(persistent._ahc_last_set_hair['night'], datetime.timedelta(hours=12))"
            ),
            action=EV_ACT_PUSH,
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label monika_sethair_down:
    if ahc_utils.hasHairDownRun():
        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1eua "I'm just going to change my hair a little bit, give me a second.{w=0.5}.{w=0.5}.{w=2}{nw}"
        else:
            m 1eua "Give me a second [player], I'm just going to change my hairstyle a little bit.{w=0.5}.{w=0.5}.{nw}"

    else:
        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1eua "I'm just going to make myself a little more comfortable, I'll be right back.{w=0.5}.{w=0.5}.{w=2}{nw}"
        else:
            m 1eua "Give me a moment [player], I'm going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{nw}"

    window hide
    call mas_transition_to_emptydesk

    python:
        renpy.pause(3.0, hard=True)

        #Get the night hair
        night_hair_list = ahc_utils.getNightHair()

        #If we're already wearing night hair, we don't want to come back as the same
        if ahc_utils.isWearingNightHair():
            night_hair_list.remove(monika_chr.hair)

        monika_chr.change_hair(
            renpy.random.choice(night_hair_list),
            by_user=False
        )

        thermos_acs = monika_chr.get_acs_of_type("thermos-mug")

        if thermos_acs:
            monika_chr.remove_acs(thermos_acs)
            mas_rmallEVL("mas_consumables_remove_thermos")

        renpy.pause(2.0, hard=True)

        persistent._ahc_last_set_hair["night"] = datetime.datetime.now()

    call mas_transition_from_emptydesk("monika 1eua")
    window auto

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "That feels better.{w=1}{nw}"

    else:
        m 1eua "That feels much better."
        if not renpy.has_label('monika_welcome_home'):
            show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve
            m 5eua "Let's have a nice evening together, [player]."

        else:
            show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve

        m 5hua "If you'd like me to change my hair back, just ask~"


    #Need to recondition/action this
    python:
        hairdown_ev = mas_getEV("monika_sethair_down")

        hairdown_ev.conditional=(
            "not mas_isMorning() "
            "and not store.persistent._mas_force_hair "
            "and ((len(store.ahc_utils.getNightHair()) > 1 "
            "and store.ahc_utils.isWearingNightHair() and store.ahc_utils.isWearingDayHair()) "
            "or not store.ahc_utils.isWearingNightHair()) "
            "and mas_timePastSince(persistent._ahc_last_set_hair['night'], datetime.timedelta(hours=12))"
        )
        hairdown_ev.action = EV_ACT_PUSH
    return
