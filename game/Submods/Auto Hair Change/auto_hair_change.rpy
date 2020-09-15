init -990 python in mas_submod_utils:
    ahc_submod = Submod(
        author="multimokia", #And Legendkiller21 (Don't want to break update scripts)
        name="Auto Hair Change",
        description="A submod which allows Monika to pick her own hairstyles for day and night.",
        version="3.0.1",
        version_updates={
            "multimokia_auto_hair_change_v2_3_0": "multimokia_auto_hair_change_v2_3_1"
        },
        settings_pane="auto_hair_change_settings_screen"
    )

init -989 python in ahc_utils:
    import store

    #Register the updater if needed
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod=store.mas_submod_utils.ahc_submod,
            user_name="multimokia",
            repository_name="MAS-Submod-Auto-Outfit-Change",
            tag_formatter=lambda x: x[x.index('_') + 1:],
            update_dir="",
            attachment_id=None,
        )

init -1 python:
    tt_when_to_update = (
        "Just updated or reinstalled your hair spritepacks? Use this to get them working with AHC again."
    )

#START: Settings pane
screen auto_hair_change_settings_screen():
    $ submods_screen_tt = store.renpy.get_screen("submods", "screens").scope["tooltip"]
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000

        hbox:
            style_prefix "check"
            box_wrap False

            textbutton _("Update Jsons"):
                action Function(store.ahc_utils.__updateJsons)
                hovered SetField(submods_screen_tt, "value", tt_when_to_update)
                unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

#START: Update scripts
label multimokia_auto_hair_change_v2_3_0(version="v2_3_0"):
    return

label multimokia_auto_hair_change_v2_3_1(version="v2_3_1"):
    python:
        ahc_utils.__updateJsons()

        hairdown_ev = mas_getEV("monika_sethair_down")

        if hairdown_ev:
            correct_conditional=(
                "mas_isNightNow() "
                "and (store.ahc_utils.shouldChangeHair('night') or store.ahc_utils.shouldChangeClothes('home')) "
                "and (not store.ahc_utils.hasHairDownRun() "
                "or store.mas_globals.ahc_run_after_date) "
            )

            if hairdown_ev.conditional != correct_conditional:
                hairdown_ev.conditional = correct_conditional

            if hairdown_ev.action != EV_ACT_PUSH:
                hairdown_ev.action = EV_ACT_PUSH

        hairponytail_ev = mas_getEV("monika_sethair_ponytail")

        if hairponytail_ev:
            correct_conditional=(
                "mas_isDayNow() "
                "and (store.ahc_utils.shouldChangeHair('day') or store.ahc_utils.shouldChangeClothes('home')) "
                "and not store.ahc_utils.hasHairPonytailRun() "
            )

            if hairponytail_ev.conditional != correct_conditional:
                hairponytail_ev.conditional = correct_conditional

            if hairponytail_ev.action != EV_ACT_PUSH:
                hairponytail_ev.action = EV_ACT_PUSH

    return

init python:
    #init these vars here to prevent crashes if we update from pre-submod framework version
    try:
        mas_clothes_rin
    except:
        mas_clothes_rin = None
    morning_flag = None

init -1 python in mas_globals:
    ahc_run_after_date = bool(store.persistent._mas_moni_chksum)

init python in ahc_utils:
    import random
    import datetime

    #Reset force hair and outfit, so we can have Moni set her own next sesh
    store.persistent._mas_force_hair = False
    store.persistent._mas_force_clothes = False

    #CONSTS
    #NOTE: This is managed in terms of Celsius
    #TODO: Change these to work on live adjustment. Will be an AAC change to provide the utils to do this
    TEMP_COOL_MAX = 20
    TEMP_COLD_MAX = 10

    __BUILTIN_DAY_HAIR = [
        store.mas_hair_def,
        store.mas_hair_downtiedstrand
    ]

    __BUILTIN_NIGHT_HAIR = [
        store.mas_hair_down,
        store.mas_hair_downtiedstrand
    ]

    __BUILTIN_DOWN_HAIR = [
        store.mas_hair_down,
        store.mas_hair_downtiedstrand
    ]

    __BUILTIN_HOME_CLOTHES = [
        store.mas_clothes_sundress_white
    ]

    __BUILTIN_DATE_CLOTHES = [
        store.mas_clothes_sundress_white
    ]

    __BUILTIN_FORMAL_CLOTHES = [
        store.mas_clothes_dress_newyears,
        store.mas_clothes_blackdress
    ]

    __BUILTIN_LIGHT_BRACELET_CLOTHES = [
        store.mas_clothes_sundress_white,
        store.mas_clothes_dress_newyears
    ]

    __BUILTIN_DARK_BRACELET_CLOTHES = [
        store.mas_clothes_blackdress
    ]

    __BUILTIN_LIGHT_BRACELET_ACS = [
        store.mas_acs_hairties_bracelet_brown
    ]

    __BUILTIN_DARK_BRACELET_ACS = [
        store.mas_acs_hairties_bracelet_brown
    ]

    #filename: {ex_prop: value}
    json_update_map = {
        "orcaramelo_hair_bunbraid.json": {"day": True},
        "orcaramelo_hair_ponytailbraid.json": {"day": True},
        "orcaramelo_hair_twintails.json": {"day": True},
        "orcaramelo_hair_twinbun.json": {"day": True},
        "orcaramelo_hair_usagi.json": {"day": True},
        "mas_hair_bun.json": {"day": True},
        "orcaramelo_clothes_sweater_shoulderless.json": {"sweater": True, "dark bracelet": True},
        "finale_clothes_jacket_brown.json": {"jacket": True, "no bracelet": True},
        "velius94_clothes_dress_whitenavyblue.json": {"home": True, "date": True, "light bracelet": True, "dark bracelet": True},
        "finale_hoodie_green.json": {"sweater": True, "no bracelet": True},
        "velius94_acs_flower_bracelet_light.json": {"light": True},
        "velius94_acs_flower_bracelet_dark.json": {"dark": True}
    }

    def __updateJsons():
        """
        Updates the jsons to add ex_props for this submod
        Additionally, will update sprites for runtime as well
        """
        import json

        JSON_PATH = "mod_assets/monika/j/"

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

    def isWearingDownHair():
        """
        Checks if Monika is wearing down hair

        OUT:
            boolean:
                True if Monika is wearing down hair
                False otherwise
        """
        global __BUILTIN_DOWN_HAIR

        return (
            "down" in store.monika_chr.hair.ex_props
            or store.monika_chr.hair in __BUILTIN_DOWN_HAIR
        )

    def has_and_unlocked(acs_name):
        """
        Returns True if we have the acs and it's unlocked
        """
        return acs_name in store.mas_selspr.ACS_SEL_MAP and store.mas_selspr.ACS_SEL_MAP[acs_name].unlocked

    def outfit_has_and_unlocked(outfit_name):
        """
        Returns True if we have the outfit and it's unlocked
        """
        return outfit_name in store.mas_selspr.CLOTH_SEL_MAP and store.mas_selspr.CLOTH_SEL_MAP[outfit_name].unlocked

    def getClothesExpropForTemperature(indoor=True):
        """
        Gets a clothes exprop for the current temperature if Auto Atmos Change is installed
        Otherwise, we'll use a timeframe to determine

        IN:
            indoor - whether or not this is for indoors or not
            (Default: True)
        """
        #First, let's see if we have AAC
        if store.mas_submod_utils.isSubmodInstalled("Auto Atmos Change") and store.awc_canGetAPIWeath():
            min_temp = store.awc_getTemperature(temp="temp_min")

            #If the weather is below the cool thresh (cold), we'll opt for a jacket (unless indoors, in which case sweater)
            if min_temp <= TEMP_COLD_MAX:
                return "sweater" if indoor else  "jacket"

            #Otherwise, if it's chilly out, we'll have a sweater
            elif TEMP_COLD_MAX < min_temp <= TEMP_COOL_MAX:
                return "sweater"

            else:
                return "home" if indoor else "date"

        else:
            #If it's winter, then this is simplified
            if store.mas_isWinter():
                return "sweater" if indoor else "jacket"

            #Likewise summer
            elif store.mas_isSummer():
                return "home" if indoor else "date"

            #Otherwise, we need to do a bit more work
            else:
                #Firstly, let's deal with hemispheres
                if store.persistent._mas_pm_live_south_hemisphere:
                    winter_start = store.mas_summer_solstice
                    winter_end = store.mas_fall_equinox
                else:
                    winter_start = store.mas_winter_solstice
                    winter_end = store.mas_spring_equinox

                if store.mas_isSpring():
                    if datetime.date.today() <= store.mas_utils.add_months(winter_end, 1):
                        return "sweater" if indoor else "jacket"
                    else:
                        return "home" if indoor else "date"

                else:
                    if datetime.date.today() >= store.mas_utils.add_months(winter_start, -1):
                        return "sweater" if indoor else "jacket"
                    else:
                        return "home" if indoor else "date"


    # Clothes stuff
    def getRandOutfitOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A random unlocked cloth of a specific exprop
        """

        global __BUILTIN_HOME_CLOTHES, __BUILTIN_DATE_CLOTHES, __BUILTIN_FORMAL_CLOTHES, __BUILTIN_LIGHT_BRACELET_CLOTHES, __BUILTIN_DARK_BRACELET_CLOTHES

        exprops_map = {
            "home": __BUILTIN_HOME_CLOTHES,
            "date": __BUILTIN_DATE_CLOTHES,
            "formal": __BUILTIN_FORMAL_CLOTHES,
            "light bracelet": __BUILTIN_LIGHT_BRACELET_CLOTHES,
            "dark bracelet": __BUILTIN_DARK_BRACELET_CLOTHES
        }

        clothes_pool = []

        clothes_with_exprop = store.MASClothes.by_exprop(exprop, value)

        for clothes in clothes_with_exprop:
            if store.mas_SELisUnlocked(clothes):
                clothes_pool.append(clothes)

        if exprop in exprops_map:
            for clothes in exprops_map[exprop]:
                if store.mas_SELisUnlocked(clothes):
                    clothes_pool.append(clothes)

        if len(clothes_pool) < 1:
            return None

        elif len(clothes_pool) < 2:
            return clothes_pool[0]

        else:
            return random.choice(clothes_pool)

    def getOutfitsOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A list of unlocked clothes of a specific exprop
        """

        global __BUILTIN_HOME_CLOTHES, __BUILTIN_DATE_CLOTHES, __BUILTIN_FORMAL_CLOTHES, __BUILTIN_LIGHT_BRACELET_CLOTHES, __BUILTIN_DARK_BRACELET_CLOTHES

        exprops_map = {
            "home": __BUILTIN_HOME_CLOTHES,
            "date": __BUILTIN_DATE_CLOTHES,
            "formal": __BUILTIN_FORMAL_CLOTHES,
            "light bracelet": __BUILTIN_LIGHT_BRACELET_CLOTHES,
            "dark bracelet": __BUILTIN_DARK_BRACELET_CLOTHES
        }

        clothes_pool = []

        clothes_with_exprop = store.MASClothes.by_exprop(exprop, value)

        for clothes in clothes_with_exprop:
            if store.mas_SELisUnlocked(clothes):
                clothes_pool.append(clothes)

        if exprop in exprops_map:
            for clothes in exprops_map[exprop]:
                if store.mas_SELisUnlocked(clothes):
                    clothes_pool.append(clothes)

        if len(clothes_pool) < 1:
            return None

        elif len(clothes_pool) < 2:
            return clothes_pool[0]

        else:
            return clothes_pool

    def hasUnlockedClothesOfExprop(exprop, value=None):
        """
        Checks if we have unlocked clothes with a specific exprop

        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            boolean:
                True if we have unlocked clothes with the exprop + value provided
                False otherwise
        """

        global __BUILTIN_HOME_CLOTHES, __BUILTIN_DATE_CLOTHES, __BUILTIN_FORMAL_CLOTHES, __BUILTIN_LIGHT_BRACELET_CLOTHES, __BUILTIN_DARK_BRACELET_CLOTHES

        exprops_map = {
            "home": __BUILTIN_HOME_CLOTHES,
            "date": __BUILTIN_DATE_CLOTHES,
            "formal": __BUILTIN_FORMAL_CLOTHES,
            "light bracelet": __BUILTIN_LIGHT_BRACELET_CLOTHES,
            "dark bracelet": __BUILTIN_DARK_BRACELET_CLOTHES
        }

        for clothes in store.MASClothes.by_exprop(exprop, value):
            if store.mas_SELisUnlocked(clothes):
                return True

        if exprop in exprops_map:
            for clothes in exprops_map[exprop]:
                if store.mas_SELisUnlocked(clothes):
                    return True

        return False


    # ACS stuff
    def getRandACSOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A random unlocked acs of a specific exprop
        """

        global __BUILTIN_LIGHT_BRACELET_ACS, __BUILTIN_DARK_BRACELET_ACS

        exprops_map = {
            "light": __BUILTIN_LIGHT_BRACELET_ACS,
            "dark": __BUILTIN_DARK_BRACELET_ACS
        }

        acs_pool = []

        for acs_name in store.mas_sprites.ACS_MAP:
            accessory = store.mas_sprites.ACS_MAP[acs_name]
            if (
                accessory.hasprop(exprop)
                and (
                    value is None
                    or value == accessory.getprop(exprop)
                )
                and store.mas_SELisUnlocked(accessory)
            ):
                acs_pool.append(accessory)

        if exprop in exprops_map:
            for accessory in exprops_map[exprop]:
                if store.mas_SELisUnlocked(accessory):
                    acs_pool.append(accessory)

        if len(acs_pool) < 1:
            return None

        elif len(acs_pool) < 2:
            return acs_pool[0]

        else:
            return random.choice(acs_pool)

    def getACSOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A list of unlocked ACS of a specific exprop
        """

        global __BUILTIN_LIGHT_BRACELET_ACS, __BUILTIN_DARK_BRACELET_ACS

        exprops_map = {
            "light": __BUILTIN_LIGHT_BRACELET_ACS,
            "dark": __BUILTIN_DARK_BRACELET_ACS
        }

        acs_pool = []

        for acs_name in store.mas_sprites.ACS_MAP:
            accessory = store.mas_sprites.ACS_MAP[acs_name]
            if (
                accessory.hasprop(exprop)
                and (
                    value is None
                    or value == accessory.getprop(exprop)
                )
                and store.mas_SELisUnlocked(accessory)
            ):
                acs_pool.append(accessory)

        if exprop in exprops_map:
            for accessory in exprops_map[exprop]:
                if store.mas_SELisUnlocked(accessory):
                    acs_pool.append(accessory)

        if len(acs_pool) < 1:
            return None

        elif len(acs_pool) < 2:
            return acs_pool[0]

        else:
            return acs_pool

    def hasUnlockedACSOfExprop(exprop, value=None):
        """
        Checks if we have unlocked ACS with a specific exprop

        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            boolean:
                True if we have unlocked ACS with the exprop + value provided
                False otherwise
        """

        global __BUILTIN_LIGHT_BRACELET_ACS, __BUILTIN_DARK_BRACELET_ACS

        exprops_map = {
            "light": __BUILTIN_LIGHT_BRACELET_ACS,
            "dark": __BUILTIN_DARK_BRACELET_ACS
        }

        for acs_name in store.mas_sprites.ACS_MAP:
            accessory = store.mas_sprites.ACS_MAP[acs_name]
            if (
                accessory.hasprop(exprop)
                and (
                    value is None
                    or value == accessory.getprop(exprop)
                )
                and store.mas_SELisUnlocked(accessory)
            ):
                return True

        if exprop in exprops_map:
            for accessory in exprops_map[exprop]:
                if store.mas_SELisUnlocked(accessory):
                    return True

        return False

init 1 python in ahc_utils:
    def shouldChangeBracelet():
        """
        Checks whether the current bracelet matches the current outfit and wears the right bracelet if not
        """

        _current_bracelet = store.monika_chr.get_acs_of_type("wrist-bracelet")

        if not _current_bracelet:
            return

        if (
            isWearingClothesOfExprop("light bracelet")
            and isWearingClothesOfExprop("dark bracelet")
            and (_current_bracelet.hasprop('light') or _current_bracelet.hasprop('dark'))
        ):
            if (
                _current_bracelet.hasprop('dark')
                and hasUnlockedACSOfExprop('light')
                and renpy.random.randint(1,5) == 1
            ):
                store.mas_sprites._acs_wear_if_found(store.monika_chr, getRandACSOfExprop("light").name)

            elif (
                _current_bracelet.hasprop('light')
                and hasUnlockedACSOfExprop('dark')
                and renpy.random.randint(1,5) == 1
            ):
                store.mas_sprites._acs_wear_if_found(store.monika_chr, getRandACSOfExprop("dark").name)

        elif (
            isWearingClothesOfExprop("light bracelet")
            and not _current_bracelet.hasprop('light')
            and hasUnlockedACSOfExprop('light')
        ):
            store.mas_sprites._acs_wear_if_found(store.monika_chr, getRandACSOfExprop("light").name)

        elif (
            isWearingClothesOfExprop("dark bracelet")
            and not _current_bracelet.hasprop('dark')
            and hasUnlockedACSOfExprop('dark')
        ):
            store.mas_sprites._acs_wear_if_found(store.monika_chr, getRandACSOfExprop("dark").name)

        elif isWearingClothesOfExprop("no bracelet"):
            store.monika_chr.remove_acs(_current_bracelet)

        return

    def isWearingClothesOfExprop(exprop):
        """
        Checks is Monika is wearing an outfit of the provided exprop
        """

        global __BUILTIN_HOME_CLOTHES, __BUILTIN_DATE_CLOTHES, __BUILTIN_FORMAL_CLOTHES, __BUILTIN_LIGHT_BRACELET_CLOTHES, __BUILTIN_DARK_BRACELET_CLOTHES

        exprops_map = {
            "home": __BUILTIN_HOME_CLOTHES,
            "date": __BUILTIN_DATE_CLOTHES,
            "formal": __BUILTIN_FORMAL_CLOTHES,
            "light bracelet": __BUILTIN_LIGHT_BRACELET_CLOTHES,
            "dark bracelet": __BUILTIN_DARK_BRACELET_CLOTHES
        }

        if exprop in exprops_map:
            return (
                exprop in store.monika_chr.clothes.ex_props
                or store.monika_chr.clothes in exprops_map[exprop]
            )
        else:
            return exprop in store.monika_chr.clothes.ex_props

init 2 python in ahc_utils:

    def changeClothesOfExprop(exprop, chance=True):
        """
        Chooses and wears an outfit of the provided exprop

        IN:
            exprop - exprop to choose an outfit from
            chance - Monika has a 66.66% (repeating of course) chance (2/3) to chance clothes if she already wears an outfit of the provided exprop
                Set it to False in order to ignore that chance and always change clothes (Default: True)
        """

        if not exprop or not hasUnlockedClothesOfExprop(exprop):
            return

        # We assign a random value, other than 1, to this. This way, if chance is False, we're guarenteed to
        # get in the elif block
        _random_chance = 2

        # Define this here so that we don't crash if we don't get in the below if/elif block
        _new_clothes = None

        if chance:
            _random_chance = renpy.random.randint(1,3)

        if not isWearingClothesOfExprop(exprop):
            _new_clothes = getRandOutfitOfExprop(exprop).name

        elif (
            isWearingClothesOfExprop(exprop)
            and isinstance(getOutfitsOfExprop(exprop), list)
            and _random_chance != 1
        ):
            _clothes_list = getOutfitsOfExprop(exprop)
            _clothes_list.remove(store.monika_chr.clothes)
            _new_clothes = renpy.random.choice(_clothes_list).name

        if _new_clothes:
            store.mas_sprites._outfit_wear_if_gifted(store.monika_chr, _new_clothes)

        return

init 7 python:

    # Update the rules of these greetings so that she doesn't change on her own on startup, if any of these are chosen

    store.mas_getEVLPropValue("mas_crashed_start", "rules", dict()).update({"no_cloth_change": None})
    store.mas_getEVLPropValue("greeting_hairdown", "rules", dict()).update({"no_cloth_change": None})

init 999 python in ahc_utils:

    @store.mas_submod_utils.functionplugin("mas_dockstat_generic_rtg")
    def getReady():
        """
        Gets Monika ready for a date
        """
        #Make hair is either what player asked, or Moni's choice
        if (
            not store.persistent._mas_force_hair
            and not (
                store.monika_chr.is_wearing_clothes_with_exprop("costume")
                and persistent._mas_setting_ocb
            )
            and not isWearingDayHair()
        ):
            store.monika_chr.change_hair(renpy.random.choice(getDayHair()), by_user=False)

        #We'll wear a ribbon if it's a special day and we're able to force
        if (
            store.mas_isSpecialDay()
            and (isWearingDayHair() and not isWearingDownHair())
            and not store.monika_chr.is_wearing_ribbon()
        ):
            if (
                has_and_unlocked("multimokia_bow_black")
                and not store.monika_chr.is_wearing_hair_with_exprop("twintails")
            ):
                store.mas_sprites._acs_wear_if_found(store.monika_chr, "multimokia_bow_black")

            elif has_and_unlocked("ribbon_black"):
                store.monika_chr.wear_acs(store.mas_acs_ribbon_black)

            else:
                store.monika_chr.wear_acs(store.mas_acs_ribbon_def)

        #Moni changes her clothes depending on certain conditions or wears what the player asked
        if not store.persistent._mas_force_clothes:

            if store.mas_isSpecialDay():
                changeClothesOfExprop("formal")

            else:
                changeClothesOfExprop(getClothesExpropForTemperature(indoor=False))

            #Check if we should change or remove the bracelet
            shouldChangeBracelet()

    @store.mas_submod_utils.functionplugin("ch30_preloop")
    def startupAHCTrigger():
        """
        This allows Monika to change her hairstyle and clothes if we went from one day cycle to another
        while the game was closed (going from day to night or v.v.).

        This won't run is we came back from a date this session, if we saw the d25 intro today or
        if today is O31 or F14 or if 'no_cloth_change' is in the greeting's rules.
        """
        if (
            not store.mas_globals.returned_home_this_sesh
            and (
                check_first_day_d25s()
                and not store.mas_isO31()
                and not store.mas_isF14()
                and "no_cloth_change" not in store.mas_getEVLPropValue(store.selected_greeting, "rules", {})
            )
        ):

            _clothes_exprop = getClothesExpropForTemperature()

            if (
                (
                    store.mas_isDayNow()
                    and (shouldChangeHair('day') or shouldChangeClothes(_clothes_exprop))
                    and not hasHairPonytailRun()
                )
                or (
                    store.mas_isNightNow()
                    and (shouldChangeHair('night') or shouldChangeClothes(_clothes_exprop))
                    and not hasHairDownRun()
                )
            ):
                _hair_random_chance = renpy.random.randint(1,4)
                _clothes_random_chance = renpy.random.randint(1,3)

                if store.mas_isDayNow():
                    _day_cycle = "day"
                    _ahc_label = "monika_sethair_ponytail"

                else:
                    _day_cycle = "night"
                    _ahc_label = "monika_sethair_down"

                changeHairAndClothes(
                    _day_cycle=_day_cycle,
                    _hair_random_chance=_hair_random_chance,
                    _clothes_random_chance=_clothes_random_chance,
                    _exprop=_clothes_exprop
                )

                _ahc_label_ev = store.mas_getEV(_ahc_label)

                if (
                    _ahc_label_ev is not None
                    and _ahc_label_ev.last_seen is not None
                ):
                    _ahc_label_ev.last_seen = datetime.datetime.now()

                store.mas_rmEVL(_ahc_label)

init 3 python in ahc_utils:
    import datetime

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

        elif _date is None:
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
            hairdown_ev = store.mas_getEV("monika_sethair_down")
        except:
            hairdown_ev = None

        #If we don't have the ev, we return None to note it
        if not hairdown_ev:
            return None

        #If we've not seen it before, we know it hasn't run and don't need to do more work
        elif not hairdown_ev.last_seen:
            return False

        _now = datetime.datetime.now()
        yesterday = datetime.date.today() - datetime.timedelta(1)

        return not (
            (
                lastSeenOnDay("monika_sethair_down")
                and store.mas_isSStoMN(_now)
                and (
                    store.mas_isMNtoSR(hairdown_ev.last_seen + datetime.timedelta(minutes=5))
                    or store.mas_isMNtoSR(hairdown_ev.last_seen - datetime.timedelta(minutes=5))
                )
            )
            or (
                not lastSeenOnDay("monika_sethair_down")
                and (
                    store.mas_isSStoMN(_now)
                    or (
                        store.mas_isMNtoSR(_now)
                        and (
                            not (
                                lastSeenOnDay("monika_sethair_down", yesterday)
                                and (
                                    store.mas_isSStoMN(hairdown_ev.last_seen + datetime.timedelta(minutes=5))
                                    or store.mas_isSStoMN(hairdown_ev.last_seen - datetime.timedelta(minutes=5))
                                )
                            )
                            or (
                                lastSeenOnDay("monika_sethair_down", yesterday)
                                and store.mas_o31 == yesterday
                                and not store.persistent._mas_o31_in_o31_mode
                            )
                        )
                    )
                )
            )
        )

    def hasHairPonytailRun():
        """
        Checks whether or not monika_sethair_ponytail has run in the current day period or not.
        OUT:
            boolean:
                True if monika_sethair_ponytail has run in the current day period
                False otherwise
        """
        #NOTE: This try/except is for use of this function in event conditionals
        #Since mas_getEV doesn't exist until init 6
        try:
            hairponytail_ev = store.mas_getEV("monika_sethair_ponytail")
        except:
            hairponytail_ev = None

        #If the event doesn't exist, return None to note it
        if not hairponytail_ev:
            return None

        #No last seen means we know it wasn't seen on the date
        elif not hairponytail_ev.last_seen:
            return False

        return lastSeenOnDay("monika_sethair_ponytail")

    def shouldChangeHair(hair_type):
        """
        Checks whether Monika should change her hair
        """
        if not hair_type:
            return False

        return (
            (
                (
                len(eval("get{0}Hair()".format(hair_type.capitalize()))) > 1
                and isWearingDayHair()
                and isWearingNightHair()
            )
            or not eval("isWearing{0}Hair()".format(hair_type.capitalize()))
            )
            and not store.persistent._mas_force_hair
        )

    def shouldChangeClothes(exprop):
        """
        Checks whether Monika should change her clothes
        """
        if not exprop:
            return False

        return not store.persistent._mas_force_clothes and hasUnlockedClothesOfExprop(exprop)


init 4 python in ahc_utils:

    def changeHairAndClothes(_day_cycle, _hair_random_chance, _clothes_random_chance, _exprop):
        """
        Allows Monika to change her hair and clothes depending on day cycle and random chance.
        IN:
            _day_cycle:
                The day cycle that corresponds to the type of hair/clothes we want Monika to change to.
                (Acceptable values: 'day', 'night')
            _hair_random_chance:
                Random chance that determines whether Monika should change her hair.
                If _hair_random_chance is 1 then Monika keeps the current hairstyle.
            _clothes_random_chance:
                Random chance that determines whether Monika should change her clothes.
                If _clothes_random_chance is 1 then Monika keeps the current outfit.
            _exprop:
                Exprop that determines what kind of outfits Monika can change into.
        """

        if _day_cycle.lower() not in ["day", "night"]:
            return

        if _day_cycle.lower() == "day":
            # Remove the ribbon if it's still there from the last time she changed to a non-down hairstyle
            if store.monika_chr.is_wearing_ribbon():
                prev_ribbon = store.monika_chr.get_acs_of_type("ribbon")
                if prev_ribbon is None:
                    prev_ribbon = store.monika_chr.get_acs_of_exprop("ribbon-like")
                if prev_ribbon is not None:
                    store.monika_chr.remove_acs(prev_ribbon)

        # Change clothes section
        if (
            shouldChangeClothes(_exprop)
            and (
                not isWearingClothesOfExprop(_exprop)
                or (isWearingClothesOfExprop(_exprop) and _clothes_random_chance != 1)
            )
        ):
            changeClothesOfExprop(exprop=_exprop, chance=False)

            prev_bracelet = store.monika_chr.get_acs_of_type("wrist-bracelet")

            if prev_bracelet:
                shouldChangeBracelet()
            else:

                if (
                    isWearingClothesOfExprop("dark bracelet")
                    and isWearingClothesOfExprop("light bracelet")
                ):
                    if renpy.random.randint(1,2) == 1:
                        store.mas_sprites._acs_wear_if_found(store.monika_chr, "flower_bracelet_dark")
                    else:
                        store.mas_sprites._acs_wear_if_found(store.monika_chr, "flower_bracelet_light")

                elif isWearingClothesOfExprop("dark bracelet"):
                    store.mas_sprites._acs_wear_if_found(store.monika_chr, "flower_bracelet_dark")

                elif isWearingClothesOfExprop("light bracelet"):
                    store.mas_sprites._acs_wear_if_found(store.monika_chr, "flower_bracelet_light")

        # Change hairstyle section
        if (
            (
                (
                len(eval("get{0}Hair()".format(_day_cycle.capitalize()))) > 1
                and isWearingDayHair()
                and isWearingNightHair()
                and _hair_random_chance != 1
            )
            or not eval("isWearing{0}Hair()".format(_day_cycle.capitalize()))
            )
            and not store.persistent._mas_force_hair
        ):

            _hair_list = eval("get{0}Hair()".format(_day_cycle.capitalize()))

            if eval("isWearing{0}Hair()".format(_day_cycle.capitalize())):
                _hair_list.remove(store.monika_chr.hair)

            store.monika_chr.change_hair(
                renpy.random.choice(_hair_list),
                by_user=False
            )

        # Remove the thermos if we have one

        thermos_acs = store.monika_chr.get_acs_of_type("thermos-mug")

        if thermos_acs:
            store.monika_chr.remove_acs(thermos_acs)
            store.mas_rmallEVL("mas_consumables_remove_thermos")

init 8 python in ahc_utils:

    def check_first_day_d25s():
        """
        Checks if today is the first day of the d25 season

        OUT:
            True if today is the first day of d25s, False otherwise
        """
        hol_intro_last_seen = store.mas_getEVL_last_seen("mas_d25_monika_holiday_intro")
        return hol_intro_last_seen and hol_intro_last_seen.date() == datetime.date.today()

init -2 python in mas_sprites:
    import store

    def _outfit_wear_if_gifted(_moni_chr, outfit_name, by_user=False):
        """
        Wears the outfit if it exists and has been gifted/reacted.
        It has been gifted/reacted if the selectable is unlocked.

        IN:
            _moni_chr - MASMonika object
            outfit_name - name of the outfit
            by_user - True if this action was mandated by user, False if not.
                (Default: False)
        """
        outfit_to_wear = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_CLOTHES,
            outfit_name
        )
        if outfit_to_wear is not None and store.mas_SELisUnlocked(outfit_to_wear):
            _moni_chr.change_clothes(outfit_to_wear, by_user=by_user)

init 50 python:
    #Reset the ahc evs here as well in case they somehow lost their conditionals/actions

    def ahc_recond_ponytail():
        """
        Recondition and action the ahc ponytail event
        """
        hairup_ev = mas_getEV("monika_sethair_ponytail")

        hairup_ev.conditional=(
            "mas_isDayNow() "
            "and (store.ahc_utils.shouldChangeHair('day') "
            "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
            "and not store.ahc_utils.hasHairPonytailRun() "
        )
        hairup_ev.action = EV_ACT_PUSH

    def ahc_recond_down():
        """
        Recondition and action the ahc down event
        """
        hairdown_ev = mas_getEV("monika_sethair_down")

        hairdown_ev.conditional=(
            "mas_isNightNow() "
            "and (store.ahc_utils.shouldChangeHair('night') "
            "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
            "and (not store.ahc_utils.hasHairDownRun() "
            "or store.mas_globals.ahc_run_after_date) "
        )
        hairdown_ev.action = EV_ACT_PUSH


    ahc_recond_ponytail()
    ahc_recond_down()

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_ponytail",
            conditional=(
                "mas_isDayNow() "
                "and (store.ahc_utils.shouldChangeHair('day') "
                "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
                "and not store.ahc_utils.hasHairPonytailRun() "
            ),
            action=EV_ACT_PUSH,
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label monika_sethair_ponytail:

    #Need to recondition/action this
    $ ahc_recond_ponytail()

    if (
        store.ahc_utils.check_first_day_d25s()
        or mas_isO31()
        or mas_isF14()
    ):
        return

    $ _hair_random_chance = renpy.random.randint(1,4)
    $ _clothes_random_chance = renpy.random.randint(1,3)
    $ _clothes_exprop = store.ahc_utils.getClothesExpropForTemperature()

    if (
        (
            store.ahc_utils.shouldChangeClothes(_clothes_exprop)
            and (
                not store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop)
                or (store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop) and _clothes_random_chance != 1)
            )
        )
        or (
            (
                len(store.ahc_utils.getDayHair()) > 1
                and store.ahc_utils.isWearingDayHair()
                and store.ahc_utils.isWearingNightHair()
                and _hair_random_chance != 1
            )
            or not store.ahc_utils.isWearingDayHair()
        )
    ):

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 3eua "I'm going to get ready for today.{w=0.5}.{w=0.5}.{w=1}{nw}"

        else:
            m 1eua "Give me a second, [mas_get_player_nickname()]."
            m 3eua "I'm just getting myself ready for the day.{w=0.5}.{w=0.5}.{nw}"

        window hide
        call mas_transition_to_emptydesk

        python:
            renpy.pause(1.0, hard=True)

            store.ahc_utils.changeHairAndClothes(
                _day_cycle="day",
                _hair_random_chance=_hair_random_chance,
                _clothes_random_chance=_clothes_random_chance,
                _exprop=_clothes_exprop
            )

            renpy.pause(4.0, hard=True)

        window hide
        call mas_transition_from_emptydesk("monika 3hub")

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 3hub "All done!{w=1}{nw}"

        else:
            m 3hub "All done!"
            m 1eua "If you want me to change my hairstyle, just ask, okay?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_down",
            conditional=(
                "mas_isNightNow() "
                "and (store.ahc_utils.shouldChangeHair('night') "
                "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
                "and (not store.ahc_utils.hasHairDownRun() "
                "or store.mas_globals.ahc_run_after_date) "
            ),
            action=EV_ACT_PUSH,
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )


label monika_sethair_down:

    #Need to recondition/action this
    $ ahc_recond_down()

    #Reset our global var here
    if store.mas_globals.ahc_run_after_date:
        $ store.mas_globals.ahc_run_after_date = False

    if store.ahc_utils.check_first_day_d25s() or mas_isO31():
        return

    #NOTE: The random chances here are for chance to NOT change
    $ _hair_random_chance = renpy.random.randint(1,4)
    $ _clothes_random_chance = 1 if mas_isF14() else renpy.random.randint(1,3)
    $ _clothes_exprop = store.ahc_utils.getClothesExpropForTemperature()

    if (
        (
            store.ahc_utils.shouldChangeClothes(_clothes_exprop)
            and (
                not store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop)
                or (store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop) and _clothes_random_chance != 1)
            )
        )
        or (
            (
                len(store.ahc_utils.getNightHair()) > 1
                and store.ahc_utils.isWearingDayHair()
                and store.ahc_utils.isWearingNightHair()
                and _hair_random_chance != 1
            )
            or not store.ahc_utils.isWearingNightHair()
        )
    ):

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1eua "I'm just going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{w=1}{nw}"
        else:
            m 1eua "Give me a moment [player], I'm going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{nw}"

        window hide
        call mas_transition_to_emptydesk

        python:
            renpy.pause(1.0, hard=True)

            store.ahc_utils.changeHairAndClothes(
                _day_cycle="night",
                _hair_random_chance=_hair_random_chance,
                _clothes_random_chance=_clothes_random_chance,
                _exprop=_clothes_exprop
            )

            renpy.pause(4.0, hard=True)

        call mas_transition_from_emptydesk("monika 1eua")
        window hide

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1eua "That feels better.{w=1}{nw}"

        else:
            m 1eua "That feels much better."
            if not renpy.has_label('monika_welcome_home'):
                show monika 5eua at t11 zorder MAS_MONIKA_Z with dissolve_monika
                m 5eua "Let's have a nice evening together, [mas_get_player_nickname()]."

            else:
                show monika 5hua at t11 zorder MAS_MONIKA_Z with dissolve_monika

            m 5hua "If you'd like me to change, just ask~"

    return
