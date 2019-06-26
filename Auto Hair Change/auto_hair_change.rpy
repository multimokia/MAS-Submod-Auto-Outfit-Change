init 999 python:
    renpy.game.persistent._mas_force_hair = False

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_ponytail",
            conditional=(
                "mas_isMorning() "
                "and monika_chr.hair == store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa or monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            ),
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label monika_sethair_ponytail:
    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3eua "I'm going to get ready for today.{w=0.5}.{w=0.5}.{w=2}{nw}"

    else:
        m 1eua "Give me a second, [player]."
        m 2dsa "I'm just getting myself ready for the day.{w=0.5}.{w=0.5}.{nw}"

    # this should auto lock/unlock stuff
    $ monika_chr.change_hair(mas_hair_def,by_user=False)
    $ monika_chr.wear_acs(mas_acs_ribbon_def)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 3hub "All done!{w=1}{nw}"

    else:
        m 3hub "All done!"
        m 1eua "If you want me to let my hair down, just ask, okay?"

    #Need to recondition/action this
    python:
        hairup_ev = mas_getEV("monika_sethair_ponytail")

        hairup_ev.conditional=(
                "mas_isMorning() "
                "and monika_chr.hair == store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa or monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            )
        hairup_ev.action = EV_ACT_QUEUE
    return


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_down",
            conditional=(
                "not mas_isMorning() "
                "and monika_chr.hair == store.mas_hair_def "
                "and (monika_chr.clothes != store.mas_clothes_marisa or monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            ),
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        )
    )

label monika_sethair_down:
    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 2dsa "I'm just going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{w=2}{nw}"
    else:
        m 2dsa "Give me a moment [player], I'm going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{nw}"

    $ monika_chr.change_hair(mas_hair_down,by_user=False)

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m "That feels better.{w=1}{nw}"

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
                "and monika_chr.hair == store.mas_hair_def "
                "and (monika_chr.clothes != store.mas_clothes_marisa or monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            )
        hairdown_ev.action = EV_ACT_QUEUE
    return
