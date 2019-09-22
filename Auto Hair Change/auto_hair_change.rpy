init 999 python:
    #Reset force hair, so we can have Moni set her own hair next sesh
    renpy.game.persistent._mas_force_hair = False

    #Override this label so we always end up here when taking Monika somewhere
    config.label_overrides["bye_going_somewhere_post_aff_check"] = "bye_going_somewhere_post_aff_check_override"
    config.label_overrides["bye_going_somewhere_iostart"] = "bye_going_somewhere_iostart_override"

    def ahc_getDayHair():
        """
        Returns a list of all MASHair objects (that are unlocked) that's not down hair
        """
        return [hair.get_sprobj() for hair in mas_selspr.filter_hair(True) if hair.name != "down"]


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_ponytail",
            conditional=(
                "mas_isMorning() "
                "and monika_chr.hair == store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
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
    $ monika_chr.change_hair(renpy.random.choice(ahc_getDayHair()),by_user=False)

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
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
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
                "and monika_chr.hair != store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
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
                "and monika_chr.hair != store.mas_hair_down "
                "and (monika_chr.clothes != store.mas_clothes_marisa and monika_chr.clothes != store.mas_clothes_rin) "
                "and not store.persistent._mas_force_hair "
            )
        hairdown_ev.action = EV_ACT_QUEUE
    return

#START: Overridden labels
#NOTE: We only override the post_aff_check because it falls through to the rest rather than jumps/calls
label bye_going_somewhere_post_aff_check_override:

    if mas_isO31():
        m 1wub "Oh! Are we going trick or treating, [player]?{nw}"
        $ _history_list.pop()
        menu:
            m "Oh! Are we going trick or treating, [player]?{fast}"
            "Yes.":
                jump bye_trick_or_treat

            "No.":
                m 2ekp "Oh, okay."


label bye_going_somewhere_iostart_override:
    # NOTE: jump back to this label to begin io generation

    show monika 2dsc
    $ persistent._mas_dockstat_going_to_leave = True
    $ first_pass = True

    # launch I/O thread
    $ promise = store.mas_dockstat.monikagen_promise
    $ promise.start()

label bye_going_somewhere_iowait_override:
    hide screen mas_background_timed_jump

    # we want to display the menu first to give users a chance to quit
    if first_pass:
        $ first_pass = False

    elif promise.done():
        # i/o thread is done!

        #Make hair is either what player asked, or Moni's choice
        if not persistent._mas_force_hair and monika_chr.hair == mas_hair_down:
            $ monika_chr.change_hair(renpy.random.choice(ahc_getDayHair()), by_user=False)

        #We'll wear a ribbon if it's a special day
        if mas_isSpecialDay():
            if 'ribbon_black' in store.mas_selspr.ACS_SEL_MAP and store.mas_selspr.ACS_SEL_MAP['ribbon_black'].unlocked:
                $ monika_chr.wear_acs(mas_acs_ribbon_black)
            else:
                $ monika_chr.wear_acs(mas_acs_ribbon_def)
        jump bye_going_somewhere_rtg

    else:
        #clean up the history list so only one "give me a second..." should show up
        $ _history_list.pop()

    # display menu options
    # 4 seconds seems decent enough for waiting.
    show screen mas_background_timed_jump(4, "bye_going_somewhere_iowait_override")
    menu:
        m "Give me a second to get ready.{fast}"
        "Wait, wait!":
            hide screen mas_background_timed_jump
            $ persistent._mas_dockstat_cm_wait_count += 1

    # fall thru to the wait wait flow
    show monika 1ekc
    menu:
        m "What is it?"
        "Actually, I can't take you right now.":
            call mas_dockstat_abort_gen
            jump bye_going_somewhere_leavemenu

        "Nothing.":
            # if we get here, we should jump back to the top so we can
            # continue waiting
            m 2hub "Oh, good! Let me finish getting ready."

    # by default, continue looping
    jump bye_going_somewhere_iowait_override