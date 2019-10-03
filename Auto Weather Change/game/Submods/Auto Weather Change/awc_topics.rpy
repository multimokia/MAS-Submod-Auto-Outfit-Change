init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="awc_monika_player_location",
            prompt="[player]'s location",
            conditional="not store.awc_isInvalidAPIKey(store.persistent._awc_API_key)",
            action=EV_ACT_QUEUE,
            category=["you"],
            aff_range=(mas_aff.NORMAL,None)
        )
    )

label awc_monika_player_location:
    m 3eua "Hey, [player]?"
    m 1eka "I've always wondered what it'd be like to live where you do."
    m 1rksdlc "But since I can't really do that yet..."
    m 3eud "...I've modified how the weather works here."
    m 3rksdla "But the thing is, I need to ask you something."

    m 1eksdla "Is it okay if I know your location?{nw}"
    $ _history_list.pop()
    menu:
        m "Is it okay if I know your location?{fast}"

        "Yes.":
            m 3hub "Yay!"

            $ temp_city = renpy.input("So what city do you live in?", length=20).strip(' \t\n\r,').capitalize()

            if awc_isInvalidLocation(temp_city):
                m 2rsc "Hmm, I can't seem to find your city..."
                m 4wub "But maybe I can get your location by your ip instead!"

                m 1eka "Is that alright with you, [player]?{nw}"
                $ _history_list.pop()
                menu:
                    m "Is that alright with you, [player]?{fast}"

                    "Sure.":
                        m 1hua "Great!"
                        m 1dsa "Give me a second to get your location.{w=0.5}.{w=0.5}.{nw}"

                        python:
                            import geocoder
                            awc_savePlayerLatLonTup(geocoder.ip('me').latlng)
                            persistent._awc_player_location["loc_pref"] = "latlon"

                        m 3hua "There we go!"

                    "No.":
                        call awc_monika_player_location_uncomfortable

            else:
                if awc_hasMultipleLocations(temp_city):
                    m 3hua "Great!"
                    m 3hksdlb "Well, it seems that there's more than one [temp_city] in the world..."

                    show monika 1eua
                    #Display our scrollable
                    $ renpy.say(m, "So, which [temp_city] do you live in?", interact=False)
                    show monika at t21
                    call screen mas_gen_scrollable_menu(awc_buildCityMenuItems(temp_city),(evhand.UNSE_X, evhand.UNSE_Y, evhand.UNSE_W, 500), evhand.UNSE_XALIGN)
                    show monika at t11

                    $ latlon = _return
                    #Now save the latlon tuple
                    $ awc_savePlayerLatLonTup(latlon)
                    $ persistent._awc_player_location["loc_pref"] = "latlon"

                    m 1hua "Thanks so much!"

                else:
                    m 1wud "Wow [player].{w=0.5} It looks like you live in the only [temp_city] in the world!"
                    m 3hksdlb "Or at least from what I know, ahaha!"

                    $ awc_savePlayerCityCountryTup((temp_city, awc_getCityCountry(temp_city)))
                    $ persistent._awc_player_location["loc_pref"] = "citycountry"

                    m 1eka "Thanks for sharing where you live with me."

            call awc_monika_player_location_end

        "I'm not comfortable with that.":
            call awc_monika_player_location_uncomfortable

    #Just for safety
    $ mas_unlockEVL("awc_monika_player_location", "EVE")
    return

label awc_monika_player_location_end:
    m 3hua "It'll be like I'm living above you, ahaha!"
    m 3eua "The weather should change to be pretty close to what it is where you are, [player]."
    m 1ekbfa "Thanks for helping me feel closer to your reality."

    #Force a weather check
    $ awc_globals.weather_check_time -= datetime.timedelta(minutes=5)
    return

label awc_monika_player_location_uncomfortable:
    m 1eka "That's okay, [player], I understand."
    m 3eua "If you ever change your mind, feel free to let me know."
    return