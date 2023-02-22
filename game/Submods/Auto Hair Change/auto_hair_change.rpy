init -990 python in mas_submod_utils:
    ahc_submod = Submod(
        author="multimokia and Legendkiller21",
        name="Auto Outfit Change",
        description="A submod which allows Monika to pick her own hairstyles for day and night.",
        version="3.0.3",
        version_updates={},
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

#START: Update scripts (when we have them)

init -1 python:
    ahc_tt_when_to_auto_update = (
        "Just updated or reinstalled your spritepacks? Use this to get them working with AHC again."
    )
    ahc_tt_when_to_manually_update = (
        "Use this to manually adjust each outfit for your needs."
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

            textbutton _("Auto update Jsons"):
                action Function(store.ahc_utils.__updateJsons)
                hovered SetField(submods_screen_tt, "value", ahc_tt_when_to_auto_update)
                unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

            textbutton _("Manually update Jsons"):
                selected False
                action Show("ahc_sprites_settings_submenu")
                hovered SetField(submods_screen_tt, "value", ahc_tt_when_to_manually_update)
                unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

screen ahc_confirm_screen(prompt, yes_action, no_action):
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            align (0.5, 0.5)
            spacing 30

            label prompt:
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton "Yes":
                    action yes_action

                textbutton "No":
                    action no_action

screen ahc_sprites_settings_submenu():
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()

    default spr_data = store.ahc_utils.__get_sprites_data()

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            spacing 5

            if spr_data[store.mas_sprites_json.SP_ACS]:
                textbutton _("Adjust accessories"):
                    xalign 0.5
                    selected False
                    action (
                        Show("ahc_sprites_settings", all_spr_ex_props=store.ahc_utils.ACS_EX_PROPS, spr_data=spr_data[store.mas_sprites_json.SP_ACS]),
                        Hide("ahc_sprites_settings_submenu")
                    )

            if spr_data[store.mas_sprites_json.SP_HAIR]:
                textbutton _("Adjust hairstyles"):
                    xalign 0.5
                    selected False
                    action (
                        Show("ahc_sprites_settings", all_spr_ex_props=store.ahc_utils.HAIR_EX_PROPS, spr_data=spr_data[store.mas_sprites_json.SP_HAIR]),
                        Hide("ahc_sprites_settings_submenu")
                    )

            if spr_data[store.mas_sprites_json.SP_CLOTHES]:
                textbutton _("Adjust clothes"):
                    xalign 0.5
                    selected False
                    action (
                        Show("ahc_sprites_settings", all_spr_ex_props=store.ahc_utils.CLOTHES_EX_PROPS, spr_data=spr_data[store.mas_sprites_json.SP_CLOTHES]),
                        Hide("ahc_sprites_settings_submenu")
                    )

            textbutton _("Return"):
                xalign 0.5
                selected False
                action Hide("ahc_sprites_settings_submenu")

screen ahc_sprites_settings(all_spr_ex_props, spr_data):
    key "noshift_T" action NullAction()
    key "noshift_t" action NullAction()
    key "noshift_M" action NullAction()
    key "noshift_m" action NullAction()
    key "noshift_P" action NullAction()
    key "noshift_p" action NullAction()
    key "noshift_E" action NullAction()
    key "noshift_e" action NullAction()

    default og_spr_data = store.ahc_utils.deepcopy(spr_data)

    modal True

    zorder 200

    style_prefix "confirm"
    add mas_getTimeFile("gui/overlay/confirm.png")

    frame:
        vbox:
            ymaximum 400
            xmaximum 700
            xfill True
            yfill False
            spacing 10

            viewport:
                id "viewport"
                scrollbars "vertical"
                ymaximum 350
                xmaximum 680
                xfill True
                yfill False
                mousewheel True

                vbox:
                    xmaximum 680
                    xfill True
                    yfill False
                    box_wrap False

                    for spr in spr_data:
                        text spr["disp_name"]
                        hbox:
                            xpos 10
                            spacing 5
                            xmaximum 680
                            box_wrap True

                            for ex_prop in all_spr_ex_props:
                                textbutton ex_prop:
                                    style "check_button"
                                    ypos 1
                                    selected ex_prop in spr["current_ex_props"]
                                    action If(
                                        ex_prop in spr["current_ex_props"],
                                        true=ahc_utils.PopDict(
                                            dict=spr["current_ex_props"],
                                            key=ex_prop
                                        ),
                                        false=SetDict(
                                            dict=spr["current_ex_props"],
                                            key=ex_prop,
                                            value=all_spr_ex_props[ex_prop]
                                        )
                                    )

            hbox:
                xalign 0.5
                spacing 10
                textbutton "Save changes":
                    selected og_spr_data != spr_data
                    action If(
                        og_spr_data == spr_data,
                        true=None,
                        false=(
                            Function(store.ahc_utils.__save_sprites_changes, og_spr_data, spr_data),
                            SetScreenVariable("og_spr_data", store.ahc_utils.deepcopy(spr_data))
                        )
                    )

                textbutton "Return":
                    selected False
                    action If(
                        og_spr_data == spr_data,
                        true=(
                            Show("ahc_sprites_settings_submenu"),
                            Hide("ahc_sprites_settings")
                        ),
                        false=Show(
                            "ahc_confirm_screen",
                            prompt="You have {b}unsaved{/b} changes. Are you sure you want to leave?",
                            yes_action=(
                                Show("ahc_sprites_settings_submenu"),
                                Hide("ahc_sprites_settings"),
                                Hide("ahc_confirm_screen")
                            ),
                            no_action=Hide("ahc_confirm_screen")
                        )
                    )

                textbutton "Help":
                    selected False
                    action Show(
                        "ahc_confirm_screen",
                        prompt="This will open a new tab in your browser.",
                        yes_action=(
                            OpenURL("https://github.com/multimokia/MAS-Submod-Auto-Outfit-Change/blob/master/game/Submods/Auto%20Hair%20Change/ex_prop_explanation.md"),
                            Hide("ahc_confirm_screen")
                        ),
                        no_action=Hide("ahc_confirm_screen")
                    )

init -999:
    default persistent._ahc_sprite_settings = dict()

# Apply our settings
init 900 python:
    for sp_type, settings_dict in persistent._ahc_sprite_settings.iteritems():
        for sp_name, ex_props in settings_dict.iteritems():
            spr_obj = store.mas_sprites.get_sprite(sp_type, sp_name)
            if spr_obj is not None:
                spr_obj.ex_props.update(ex_props)


init python:
    #init these vars here to prevent crashes if we update from pre-submod framework version
    try:
        mas_clothes_rin
    except:
        mas_clothes_rin = None
    morning_flag = None

init -1 python in mas_globals:
    ahc_run_after_date = bool(store.persistent._mas_moni_chksum)

init -999 python in ahc_utils:
    @renpy.pure
    class PopDict(renpy.store.Action, renpy.store.FieldEquality):
        """
        An action that pops a key from a dict.
        """
        identity_fields = ["dict", "key"]

        def __init__(self, dict, key):
            self.dict = dict
            self.key = key

        def __call__(self):
            if self.key in self.dict:
                self.dict.pop(self.key)

            renpy.restart_interaction()

        def get_selected(self):
            if self.key not in self.dict:
                return True

            return False

init 2 python in ahc_utils:
    # Finally update this dict
    ALL_EX_PROPS.update(ACS_EX_PROPS)
    ALL_EX_PROPS.update(HAIR_EX_PROPS)
    ALL_EX_PROPS.update(CLOTHES_EX_PROPS)

init python in ahc_utils:
    import random
    import datetime
    import json
    from store import persistent
    from copy import deepcopy# This is used in our screens

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
        "finale_clothes_shirt_blue.json": {"home": True},
        "velius94_clothes_shirt_pink.json": {"home": True, "date": True}
    }

    EXPROPS_MAP = {
        "home": __BUILTIN_HOME_CLOTHES,
        "date": __BUILTIN_DATE_CLOTHES,
        "formal": __BUILTIN_FORMAL_CLOTHES,
        "light bracelet": __BUILTIN_LIGHT_BRACELET_CLOTHES,
        "dark bracelet": __BUILTIN_DARK_BRACELET_CLOTHES,
        "light": __BUILTIN_LIGHT_BRACELET_ACS,
        "dark": __BUILTIN_DARK_BRACELET_ACS
    }

    ACS_EX_PROPS = {"light": True, "dark": True}
    HAIR_EX_PROPS = {"day": True, "night": True, "down": True}
    CLOTHES_EX_PROPS = {
        "home": True,
        "date": True,
        "formal": True,
        "sweater": True,
        "jacket": True,
        "pajamas": True,
        "light bracelet": True,
        "dark bracelet": True,
        "no bracelet": True
    }
    # NOTE: this will be filled at init 2
    # to allow people override/add custom ex props at init 1
    ALL_EX_PROPS = dict()

    def add_builtin_to_list(obj, ex_prop):
        """
        Adds a builtin to a builtin list

        IN:
            obj - MASClothes or MASAccessory object to add to the appropritate list
                (NOTE: THESE ARE NOT VALIDATED FOR TYPE)
            ex_prop - ex_prop list to map to.
        """
        global EXPROPS_MAP

        if ex_prop not in EXPROPS_MAP:
            return

        EXPROPS_MAP[ex_prop].append(obj)

    def remove_builtin_from_list(obj, ex_prop):
        """
        Removes a builtin from the builtin list

        IN:
            obj - MASClothes or MASAccessory object to remove from the appropritate list
                (NOTE: If this isn't present in a list, this does nothing)
            ex_prop - ex_prop list to remove from
        """
        global EXPROPS_MAP

        if ex_prop not in EXPROPS_MAP:
            return

        if obj not in EXPROPS_MAP[ex_prop]:
            return

        EXPROPS_MAP[ex_prop].remove(obj)

    def __save_sprites_changes(og_spr_data, new_spr_data):
        """
        This method is being used in our screens. It checks which data was changed and updates/saves corresponding things.
        The data here is a list of dicts with various objects that hold different information about sprite objects (acs, hair, clothes).

        IN:
            og_spr_data - sprite data before the changes
            new_spr_data - sprite data after the changes
        """
        for old_data_dict, new_data_dict in zip(og_spr_data, new_spr_data):
            # Founds difference?
            if old_data_dict != new_data_dict:
                # If this sprite object is a sprite pack, then we update its json
                if new_data_dict["json_fp"] is not None:
                    _updateJson(new_data_dict["json_fp"], ex_props=new_data_dict["current_ex_props"], replace=True)

                # Otherwise we're editing a built-in sprite and need to save it in persistent
                else:
                    _sp_type = new_data_dict["spr_obj"].gettype()
                    _sp_name = new_data_dict["spr_obj"].name

                    if _sp_type not in persistent._ahc_sprite_settings:
                        persistent._ahc_sprite_settings[_sp_type] = dict()

                    # If we got an empty dict, then we want to remove it from the settings
                    if not new_data_dict["current_ex_props"]:
                        if _sp_name in persistent._ahc_sprite_settings[_sp_type]:
                            persistent._ahc_sprite_settings[_sp_type].pop(_sp_name)

                            if not persistent._ahc_sprite_settings[_sp_type]:
                                persistent._ahc_sprite_settings.pop(_sp_type)

                    else:
                        persistent._ahc_sprite_settings[_sp_type][_sp_name] = new_data_dict["current_ex_props"]

                    # Update it for runtime
                    spr_obj = store.mas_sprites.get_sprite(_sp_type, _sp_name)
                    if spr_obj is not None:
                        # We need to completely override, so pop the existing ex props
                        for key in spr_obj.ex_props.copy():
                            if key in ALL_EX_PROPS:
                                spr_obj.ex_props.pop(key)

                        spr_obj.ex_props.update(new_data_dict["current_ex_props"])

    def __get_sprites_data():
        """
        Returns all sprite objects, their name, jsons fp (if appopriate), and current custom ex_props

        OUT:
            dict of lists with the data where keys are spritepacks types (0-2 as of current)
            e.g.:
                {
                    0: [
                        {"disp_name": value, "spr_obj": value, "json_fp": value, "current_ex_props": value},
                        ...
                    ],
                    ...
                }
        """
        def add_to_rv(spr_obj, json_fp=None):
            """
            Inner method to help dealing with booplicated code

            IN:
                spr_obj - sprite object
                json_fp - path to the sprite object's json
            """
            # Get ex_props
            current_ex_props = {key: value for key, value in spr_obj.ex_props.iteritems() if key in ALL_EX_PROPS}
            # Get the selectable for name
            spr_obj_sel = store.mas_selspr.get_sel(spr_obj)
            if spr_obj_sel is not None:
                # Wait, but this is locked! Skip it
                if not spr_obj_sel.unlocked:
                    store.mas_utils.writelog(
                        "[AOC ERROR]: '{0}' is locked, ignoring.\n".format(spr_obj.name)
                    )
                    return
                disp_name = spr_obj_sel.display_name

            # If this spr object doesn't have a selectable, then we use its name in the code
            else:
                disp_name = spr_obj.name.replace("_", " ").capitalize()

            # Add this obj to rv
            rv_list = rv.get(spr_obj.gettype(), None)
            if rv_list is not None:
                rv_list.append(
                    {
                        "disp_name": disp_name,
                        "spr_obj": spr_obj,
                        "json_fp": json_fp,
                        "current_ex_props": current_ex_props
                    }
                )

            else:
                store.mas_utils.writelog(
                    "[AOC ERROR]: '{0}' has the invalid type '{1}'.\n".format(spr_obj.name, spr_obj.gettype())
                )

        rv = {
            store.mas_sprites_json.SP_ACS: list(),
            store.mas_sprites_json.SP_HAIR: list(),
            store.mas_sprites_json.SP_CLOTHES: list()
        }

        all_acs = store.mas_sprites.ACS_MAP.values()
        all_acs = filter(lambda item: item.mux_type and "wrist-bracelet" in item.mux_type, all_acs)# We care only about bracelets
        all_hair = store.mas_sprites.HAIR_MAP.values()
        all_hair = filter(lambda item: item.name != "custom", all_hair)# You don't need to adjust the "custom" hair
        all_clothes = store.mas_sprites.CLOTH_MAP.values()
        all_spr_objs = {
            store.mas_sprites_json.SP_ACS: all_acs,
            store.mas_sprites_json.SP_HAIR: all_hair,
            store.mas_sprites_json.SP_CLOTHES: all_clothes
        }
        # MAIN_FP = store.mas_sprites_json.sprite_station.station.replace("\\", "/")
        GAMEDIR_FP = renpy.config.gamedir.replace("\\", "/")
        JSONDIR_FP = "/mod_assets/monika/j/"
        all_json_fps = [JSONDIR_FP + json_fp for json_fp in store.mas_sprites_json.sprite_station.getPackageList(".json")]

        # First deal with custom sprites
        for json_fp in all_json_fps:
            if renpy.loadable(json_fp):
                with open(GAMEDIR_FP + json_fp) as jfile:
                    json_data = json.load(jfile)
                    if "type" in json_data and "name" in json_data:
                        spr_obj = store.mas_sprites.get_sprite(json_data["type"], json_data["name"])

                        if spr_obj is not None:
                            add_to_rv(spr_obj, json_fp)

                            # Don't forget to remove it from the list since we've already dealt with it
                            spr_obj_list = all_spr_objs.get(spr_obj.gettype(), None)
                            if spr_obj_list is not None:
                                spr_obj_list.remove(spr_obj)

                            else:
                                store.mas_utils.writelog(
                                    "[AOC ERROR]: '{0}' has the invalid type '{1}'.\n".format(spr_obj.name, spr_obj.gettype())
                                )

                        else:
                            store.mas_utils.writelog(
                                "[AOC ERROR]: Couldn't get a sprite object of the '{0}' type with the '{1}' name.\n".format(
                                    json_data["type"],
                                    json_data["name"]
                                )
                            )

                    else:
                        store.mas_utils.writelog(
                            "[AOC ERROR]: '{0}' is missing the 'type' and/or 'name' fields.\n".format(json_fp)
                        )

            else:
                store.mas_utils.writelog(
                    "[AOC ERROR]: '{0}' isn't loadable.\n".format(json_fp)
                )

        # Now deal with built-in sprites
        for spr_obj in (all_acs + all_hair + all_clothes):
            # These shouldn't be custom
            if not spr_obj.is_custom:
                add_to_rv(spr_obj)

            else:
                store.mas_utils.writelog(
                    "[AOC ERROR]: '{0}' is a custom sprite, but it wasn't removed with other json sprites.\n".format(spr_obj.name)
                )

        # Sort all by name
        for key in rv:
            rv[key].sort(key=lambda item: item["disp_name"])

        return rv

    def _updateJson(json_fp, ex_props={}, replace=False):
        """
        Updates a json, modifying its ex_props

        IN:
            json_fp - relative filepath to the json file
            ex_props - new ex_props
                (Default: empty dict)
            replace - if True, we'll remove all the existing custom ex_props and then add the new ones,
                otherwise we'll just update them
                (Default: False)
        """
        GAMEDIR = renpy.config.gamedir.replace("\\", "/")

        if renpy.loadable(json_fp):
            with open(GAMEDIR + json_fp) as jfile:
                json_data = json.load(jfile)

                #If there is no expsting ex_props field, we shoud create it
                if "ex_props" not in json_data:
                    json_data["ex_props"] = dict()

                # Replacing? Filter so we remove only submodded ex_props
                elif replace:
                    json_data["ex_props"] = {key: value for key, value in json_data["ex_props"].iteritems() if key not in ALL_EX_PROPS}

                # Update with the new ex_props
                json_data["ex_props"].update(ex_props)

                if not json_data["ex_props"]:
                    json_data.pop("ex_props")

                #Now we want to update the runtime variant
                spr_obj = store.mas_sprites.get_sprite(json_data["type"], json_data["name"])
                if spr_obj:
                    # See if we want to remove the existing ex props
                    if replace:
                        for key in spr_obj.ex_props.copy():
                            if key in ALL_EX_PROPS:
                                spr_obj.ex_props.pop(key)

                    spr_obj.ex_props.update(ex_props)

                #Now write the new json
                with open(GAMEDIR + json_fp, "w") as jfile:
                    json.dump(json_data, jfile, indent=4, sort_keys=True)

    def __updateJsons():
        """
        Updates the jsons to add ex_props for this submod
        Additionally, will update sprites for runtime as well
        """
        JSON_PATH = "/mod_assets/monika/j/"

        for json_filename, added_ex_props in json_update_map.iteritems():
            _updateJson(
                JSON_PATH + json_filename,
                ex_props=added_ex_props,
                replace=True
            )

    def _compatibleOnly(hair_list):
        """
        Filters the given list to only return the MASHair objects which are compatible with the current clothes

        IN:
            hair_list:
                list() of MASHair objects which need to be filtered

        OUT:
            list() of MASHair objects which are unlocked and compatible with the current outfit
        """
        return [
            hair
            for hair in hair_list
            if (
                store.mas_selspr.HAIR_SEL_MAP[hair.name].unlocked
                and store.mas_sprites.is_clotheshair_compatible(store.monika_chr.clothes, hair)
            )
        ]

    def getDayHair():
        """
        Gets day hair

        OUT:
            list() of unlocked MASHair objects which are suited for day and are compatible with the current clothes
        """
        global __BUILTIN_DAY_HAIR

        return _compatibleOnly([
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

        return _compatibleOnly([
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
            try:
                min_temp = store.awc_getTemperature(temp="temp_min")

            #Set to None here as this will also be consistent with those who do update AAC, as that _default will be None
            except:
                min_temp = None

            #If we couldn't get the temperature for any reason, we'll fall back to no-aac rules
            if min_temp is None:
                return no_aac_weather_exprop_get(indoor)

            #If the weather is below the cool thresh (cold), we'll opt for a jacket (unless indoors, in which case sweater)
            if min_temp <= TEMP_COLD_MAX:
                return "sweater" if indoor else "jacket"

            #Otherwise, if it's chilly out, we'll have a sweater
            elif TEMP_COLD_MAX < min_temp <= TEMP_COOL_MAX:
                return "sweater"

            else:
                return "home" if indoor else "date"

        else:
            return no_aac_weather_exprop_get(indoor)

    def no_aac_weather_exprop_get(indoor):
        """
        This gets the clothes exprops for outfits when we do NOT have AAC installed, or we cannot get a reading from it

        IN:
            indoor - Whether or not this is for indoor wear or outdoor weather

        CONDITIONS:
            - Fall: Always jacket outdoors when in the last month. Sweater indoors for that period
            - Winter: Always jacket outdoors, sweater indoors
            - Spring: Always jacket outdoors for the first month. Sweater indoors for that period

        OUT:
            string - exprop for clothes to use
        """
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
        for clothes in store.MASClothes.by_exprop(exprop, value):
            if store.mas_SELisUnlocked(clothes):
                return True

        if exprop in EXPROPS_MAP:
            for clothes in EXPROPS_MAP[exprop]:
                if store.mas_SELisUnlocked(clothes):
                    return True

        return False

    def getOutfitsOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A list of unlocked clothes of a specific exprop
        """
        # if there are no unlocked outfits then return
        if not hasUnlockedClothesOfExprop(exprop, value):
            return None

        clothes_pool = []

        clothes_with_exprop = store.MASClothes.by_exprop(exprop, value)

        for clothes in clothes_with_exprop:
            if store.mas_SELisUnlocked(clothes):
                clothes_pool.append(clothes)

        if exprop in EXPROPS_MAP:
            for clothes in EXPROPS_MAP[exprop]:
                if store.mas_SELisUnlocked(clothes):
                    clothes_pool.append(clothes)

        return clothes_pool


    def getRandOutfitOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A random unlocked cloth of a specific exprop
        """

        clothes_pool = getOutfitsOfExprop(exprop, value)

        if clothes_pool:
            return random.choice(clothes_pool)

    # ACS stuff
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

        if exprop in EXPROPS_MAP:
            for accessory in EXPROPS_MAP[exprop]:
                if store.mas_SELisUnlocked(accessory):
                    return True

        return False

    def getACSOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A list of unlocked ACS of a specific exprop
        """
        # if there are no unlocked ACS then return
        if not hasUnlockedACSOfExprop(exprop, value):
            return None

        acs_pool = [
            acs
            for acs in store.mas_sprites.ACS_MAP.itervalues()
            if acs.hasprop(exprop) and (value is None or value == acs.getprop(exprop)) and store.mas_SELisUnlocked(acs)
        ]

        if exprop in EXPROPS_MAP:
            for accessory in EXPROPS_MAP[exprop]:
                if store.mas_SELisUnlocked(accessory):
                    acs_pool.append(accessory)

        return acs_pool

    def getRandACSOfExprop(exprop, value=None):
        """
        IN:
            exprop - exprop to look for
            value - value the exprop should be. Set to None to ignore.
            (Default: None)

        OUT:
            A random unlocked acs of a specific exprop
        """

        acs_pool = getACSOfExprop(exprop, value)

        if acs_pool:
            return random.choice(acs_pool)

        return None

init 1 python in ahc_utils:
    def shouldChangeBracelet():
        """
        Checks whether the current bracelet matches the current outfit and wears the right bracelet if not
        """

        global __BUILTIN_LIGHT_BRACELET_ACS, __BUILTIN_DARK_BRACELET_ACS

        # Add these in the global namespace so that eval can use them
        global _is_wearing_light_bracelet, _is_wearing_dark_bracelet

        # Get our current bracelet
        _current_bracelet = store.monika_chr.get_acs_of_type("wrist-bracelet")

        # This is used for the cases where Monika is already wearing a bracelet
        # In these case she has a 33% chance to change to a different one
        _random_chance = renpy.random.randint(1,3) == 1

        # Default some vars here
        _should_wear_bracelet_of_type = None
        _is_wearing_light_bracelet = None
        _is_wearing_dark_bracelet = None

        if _current_bracelet:
            _is_wearing_light_bracelet = _current_bracelet.hasprop('light') or _current_bracelet in __BUILTIN_LIGHT_BRACELET_ACS
            _is_wearing_dark_bracelet = _current_bracelet.hasprop('dark') or _current_bracelet in __BUILTIN_DARK_BRACELET_ACS

        if isWearingClothesOfExprop("light bracelet"):
            _is_wearing_light_clothes = True
            _should_wear_bracelet_of_type = "light"

        if isWearingClothesOfExprop("dark bracelet"):
            _is_wearing_dark_clothes = True
            _should_wear_bracelet_of_type = "both" if _should_wear_bracelet_of_type else "dark"

        # If the outfit should not have a bracelet and Monika wears one, then remove it
        if isWearingClothesOfExprop("no bracelet") and _current_bracelet:
            store.monika_chr.remove_acs(_current_bracelet)

        # Monika is wearing clothes of both types
        elif _should_wear_bracelet_of_type == "both":
            _should_wear_bracelet_of_type = "light" if renpy.random.randint(0,1) else "dark"

            # Get the bracelet list
            _bracelet_list = getACSOfExprop(_should_wear_bracelet_of_type)

            if (
                _bracelet_list
                and (
                        (
                        _current_bracelet
                        and _random_chance
                        and (_is_wearing_light_bracelet or _is_wearing_dark_bracelet)
                        and _current_bracelet in _bracelet_list
                        and len(_bracelet_list) >= 2
                    )
                    or not (_is_wearing_light_bracelet or _is_wearing_dark_bracelet)
                )
            ):
                if _current_bracelet and _current_bracelet in _bracelet_list:
                    _bracelet_list.remove(_current_bracelet)
                store.mas_sprites._acs_wear_if_found(store.monika_chr, renpy.random.choice(_bracelet_list).name)

        # Otherwise only one type fits the current outfit
        elif _should_wear_bracelet_of_type:

            # Get the bracelet list
            _bracelet_list = getACSOfExprop(_should_wear_bracelet_of_type)

            if _bracelet_list:
                # If Monika already wears a bracelet there's a chance to change it
                if _current_bracelet and eval("_is_wearing_{0}_bracelet".format(_should_wear_bracelet_of_type)):

                    # We check the chance here so that we don't go in the else block if this is False
                    if _random_chance:
                        # Check if the current bracelet is in the list in case we ever have a bracelet that's part of an outfit
                        # and that is not unlocked
                        if _current_bracelet in _bracelet_list and len(_bracelet_list) >= 2:
                            _bracelet_list.remove(_current_bracelet)
                        store.mas_sprites._acs_wear_if_found(store.monika_chr, renpy.random.choice(_bracelet_list).name)

                # Otherwise choose a bracelet if we have one unlocked
                else:
                    store.mas_sprites._acs_wear_if_found(store.monika_chr, getRandACSOfExprop(_should_wear_bracelet_of_type).name)

        del _is_wearing_light_bracelet, _is_wearing_dark_bracelet

        return

    def isWearingClothesOfExprop(exprop):
        """
        Checks is Monika is wearing an outfit of the provided exprop
        """
        if exprop in EXPROPS_MAP:
            return (
                exprop in store.monika_chr.clothes.ex_props
                or store.monika_chr.clothes in EXPROPS_MAP[exprop]
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

        # Get the list with the outfits of the provided exprop
        _clothes_list = getOutfitsOfExprop(exprop)

        # If the list is empty then return
        if not _clothes_list:
            return

        # If Monika is not wearing clothes of this exprop, choose a random one from the list
        if not isWearingClothesOfExprop(exprop):
            store.mas_sprites._outfit_wear_if_gifted(store.monika_chr, renpy.random.choice(_clothes_list).name)

        # If Monika is wearing clothes of this exprop and there are more than 2 outfits in the list,
        # then depending on the chance var, she has a chance to change
        elif ((
                (chance and renpy.random.randint(1,3) == 1)
                or not chance
            )
            and isWearingClothesOfExprop(exprop)
            and len(_clothes_list) >= 2
        ):
            _clothes_list.remove(store.monika_chr.clothes)
            store.mas_sprites._outfit_wear_if_gifted(store.monika_chr, renpy.random.choice(_clothes_list).name)

        return

init 7 python:
    # Update the rules of these greetings so that she doesn't change on her own on startup, if any of these are chosen
    store.mas_getEVLPropValue("mas_crashed_start", "rules", dict()).update({"no_cloth_change": None})
    store.mas_getEVLPropValue("greeting_hairdown", "rules", dict()).update({"no_cloth_change": None})

init 990 python in ahc_utils:
    @store.mas_submod_utils.functionplugin("mas_dockstat_generic_rtg")
    def getReady():
        """
        Gets Monika ready for a date
        """
        #Make hair is either what player asked, or Moni's choice
        #NOTE: _mas_setting_ocb is not a consistent way to check for outfit mode as
        #change_clothes doesn't set this to True
        #TODO: Find a way to check if the current hairstyle/acs are part of the outfit
        if (
            not store.persistent._mas_force_hair
            and not (
                store.monika_chr.is_wearing_clothes_with_exprop("costume")
                and store.ahc_utils.isWearingClothesOfExpropValue("o31")
            )
            and not isWearingDayHair()
        ):
            store.monika_chr.change_hair(renpy.random.choice(getDayHair()), by_user=False)

        #We'll wear a ribbon if it's a special day and we're able to force and it's not O31
        if (
            store.mas_isSpecialDay()
            and not store.mas_isO31()
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
        if (
            not store.persistent._mas_force_clothes
            or isWearingClothesOfExprop("lingerie")
            or (
                isWearingClothesOfExprop("pajamas")
                and not isWearingClothesOfExprop(getClothesExpropForTemperature(indoor=False))
            )
        ):
            if store.mas_isSpecialDay():
                if store.mas_isF14() and store.mas_isDayNow():
                    changeClothesOfExprop("date")

                elif store.mas_farewells.dockstat_rtg_label == "bye_trick_or_treat_rtg":
                    if not store.ahc_utils.isWearingClothesOfExpropValue("o31"):
                        _o31_outfits_list = store.MASClothes.by_exprop("costume", "o31")

                        _current_o31_outfit = None

                        for costume in _o31_outfits_list:
                            if store.persistent._mas_o31_costumes_worn.get(costume.name) == datetime.date.today().year:
                                _current_o31_outfit = costume.name
                                break

                        if _current_o31_outfit:
                            store.mas_sprites._outfit_wear_if_gifted(
                                store.monika_chr,
                                _current_o31_outfit,
                                outfit_mode=True)

                        else:
                            changeClothesOfExprop(getClothesExpropForTemperature(indoor=False))

                # If we go for a date on O31 but not for ToT, get normal date clothes
                elif store.mas_isO31():
                    changeClothesOfExprop(getClothesExpropForTemperature(indoor=False))

                else:
                    changeClothesOfExprop("formal")

            else:
                changeClothesOfExprop(getClothesExpropForTemperature(indoor=False))

            #Check if we should change or remove the bracelet
            shouldChangeBracelet()

    @store.mas_submod_utils.functionplugin("ch30_post_exp_check")
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
                not check_first_day_d25s()
                and not store.mas_isO31()
                and not store.mas_isF14()
                and store.selected_greeting
                and "no_cloth_change" not in store.mas_getEVLPropValue(store.selected_greeting, "rules", {})
            )
        ):

            _clothes_exprop = getClothesExpropForTemperature()
            _now = datetime.datetime.now()

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

                if _ahc_label_ev is not None:
                    _ahc_label_ev.last_seen = _now

                    store.mas_rmEVL(_ahc_label)
                    # recond the label in case the conditions were stripped
                    store.ahc_recond_ahc_label(_ahc_label)

                    # The triggered label was monika_sethair_down
                    if _ahc_label == "monika_sethair_down":

                        # Update out persist var
                        store.setHairDownSuntimeStates()

                        # And check if we have unlocked pjs
                        if hasUnlockedClothesOfExprop("pajamas"):
                            # Recondition the pjs topic
                            store.ahc_recond_pjs()

            _ahc_pj_ev = store.mas_getEV("monika_setoutfit_pjs")

            if _ahc_pj_ev is not None and _ahc_pj_ev.start_date is not None:

                # If we're past the start_date or we're really close to the start_date, then trigger the pjs topic too
                if _ahc_pj_ev.start_date - datetime.timedelta(minutes=20) <= _now < _ahc_pj_ev.end_date:
                    if not store.ahc_utils.isWearingClothesOfExprop("pajamas"):
                        changeHairAndClothes(
                            _day_cycle="night",
                            _hair_random_chance=1,
                            _clothes_random_chance=2,
                            _exprop="pajamas"
                        )

                    store.mas_stripEVL("monika_setoutfit_pjs", list_pop=True)

                # If we're part the end_date, the strip and remove the event from the event list
                elif _ahc_pj_ev.end_date <= _now:
                    store.mas_stripEVL("monika_setoutfit_pjs", list_pop=True)

# Until the time we get in iostart we don't know if there are any custom farewell labels
# In order to be sure that we plug getReady to any future custom label we override the iostart label
# and we plug customLabelsGetReady into both the generic iowait and the custom one, if found.
# The function then checks and plugs getReady into the custom rtg label, if there's one.

init 991 python in ahc_utils:

    @store.mas_submod_utils.functionplugin("mas_dockstat_generic_iowait")
    def customLabelsGetReady():
        if renpy.has_label(store.mas_farewells.dockstat_rtg_label):
            store.mas_submod_utils.registerFunction(
                store.mas_farewells.dockstat_rtg_label,
                store.ahc_utils.getReady
            )

init 992 python:
    config.label_overrides["mas_dockstat_iostart"] = "mas_dockstat_iostart_ov"

label mas_dockstat_iostart_ov:
    show monika 2dsc
    python:
        persistent._mas_dockstat_going_to_leave = True
        first_pass = True

        # launch I/O thread
        promise = store.mas_dockstat.monikagen_promise
        promise.start()

    #Jump to the iowait label
    if renpy.has_label(mas_farewells.dockstat_iowait_label):
        $ mas_submod_utils.registerFunction(
            mas_farewells.dockstat_iowait_label,
            store.ml_utils.customLabelsGetReady
        )
        jump expression mas_farewells.dockstat_iowait_label
    #If the one passed in wasn't valid, then we'll use the generic iowait
    jump mas_dockstat_generic_iowait


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
        if not hair_type or hair_type.lower() not in ["day", "night"]:
            return False

        return (
            (
                (
                len(eval("get{0}Hair()".format(hair_type.capitalize()))) > 1
                and isWearingDayHair()
                and isWearingNightHair()
            )
            or (
                len(eval("get{0}Hair()".format(hair_type.capitalize()))) > 0
                and not eval("isWearing{0}Hair()".format(hair_type.capitalize()))
            )
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

        #Do clothes and acs logic
        do_clothes_logic(_clothes_random_chance, _exprop)

        #Now do hair logic
        do_hair_logic(_hair_random_chance, _day_cycle)

        #Do any post logic if need be
        store.mas_submod_utils.getAndRunFunctions()

        #Remove the thermos if we have one
        thermos_acs = store.monika_chr.get_acs_of_type("thermos-mug")

        if thermos_acs:
            store.monika_chr.remove_acs(thermos_acs)
            store.mas_rmallEVL("mas_consumables_remove_thermos")

        #Save Monika's new clothes/hair/acs
        store.monika_chr.save()
        store.renpy.save_persistent()

    def do_clothes_logic(_clothes_random_chance, _exprop):
        """
        Does logic related to clothes, including acs parts

        IN:
            _clothes_random_chance - chance for clothes to not change
            _exprop - exprop to get clothes from
        """
        # Change clothes section
        if (
            shouldChangeClothes(_exprop)
            and (
                not isWearingClothesOfExprop(_exprop)
                or (isWearingClothesOfExprop(_exprop) and _clothes_random_chance != 1)
            )
        ):
            changeClothesOfExprop(exprop=_exprop, chance=False)

            shouldChangeBracelet()

            #Do further acs management here
            store.mas_submod_utils.getAndRunFunctions()

    def do_hair_logic(_hair_random_chance, _day_cycle):
        """
        Does hair logic and changes hair as needed

        IN:
            _hair_random_chance - chance for hair to not change
            _day_cycle - time of day (day/night)
        """
        _hair_list = eval("get{0}Hair()".format(_day_cycle.capitalize()))

        # Change hairstyle section
        if ((
                (
                    len(_hair_list) > 1
                    and isWearingDayHair()
                    and isWearingNightHair()
                    and _hair_random_chance != 1
                )
                or (
                    len(_hair_list) > 0
                    and not eval("isWearing{0}Hair()".format(_day_cycle.capitalize()))
                )
            )
            and not store.persistent._mas_force_hair
        ):

            if eval("isWearing{0}Hair()".format(_day_cycle.capitalize())):
                _hair_list.remove(store.monika_chr.hair)

            store.monika_chr.change_hair(
                renpy.random.choice(_hair_list),
                by_user=False
            )

            store.mas_submod_utils.getAndRunFunctions()

    def isWearingClothesOfExpropValue(value):
        """
        Checks if the clothes Monika is currently wearing has an exprop with a provided value
        This is used in cases where we only care about the value of an exprop, like when we want to check
        if Monika is wearing a D25 or O31 outfit.
        """

        _current_outfit_props = store.monika_chr.clothes.ex_props

        if not _current_outfit_props:
            return False

        for prop, prop_value in _current_outfit_props.iteritems():
            if prop_value == value.lower():
                return True
        return False

init 8 python in ahc_utils:

    def check_first_day_d25s():
        """
        Checks if today is the first day of the d25 season

        OUT:
            True if today is the first day of d25s, False otherwise
        """
        hol_intro_last_seen = store.mas_getEVL_last_seen("mas_d25_monika_holiday_intro")

        if hol_intro_last_seen and hol_intro_last_seen.date() == datetime.date.today():
            return True

        if not hol_intro_last_seen or not store.mas_lastSeenInYear("mas_d25_monika_holiday_intro"):
            hol_intro_last_seen = store.mas_getEVL_last_seen("mas_d25_monika_christmas")
            return hol_intro_last_seen and hol_intro_last_seen.date() == datetime.date.today()

#TODO: Change the last condition of the return after TMA is in

    def should_AHC_return_on_d25():
        """
        Checks if the ahc labels should return without doing anything on D25
        CONDITIONS:
            1) We return home from a date
            2) The last seen of mas_d25_monika_christmas is today
            3) The last seen of mas_d25_monika_christmas is after the end of the last sesh
            4) We got the decor and mas_d25_monika_christmas through mas_d25_monika_holiday_intro_rh_rh which means
               that we haven't seen mas_d25_monika_holiday_intro yet
        """
        hol_intro_last_seen = store.mas_getEVL_last_seen("mas_d25_monika_christmas")

        return (
            hol_intro_last_seen
            and store.persistent.sessions.get("last_session_end")
            and not store.mas_lastSeenInYear("mas_d25_monika_holiday_intro")
            and store.mas_globals.ahc_run_after_date
            and hol_intro_last_seen.date() == datetime.date.today()
            and store.persistent.sessions["last_session_end"] < hol_intro_last_seen
        )

init 9 python in ahc_utils:

    def should_AHC_label_return():
        """
        Checks whether AHC labels should return without running if we're in D25, O31 or F14
        CONDITIONS:
            O31:
                1) Return if we're not in o31 mode. This assured that the labels won't run before the intro.
                2) Return if we're returning home from a date and Monika is wearing a costume.
            F14:
                1) Return if we're not in f14 mode. This assured that the labels won't run before the intro.
                2) Return if we're returning home from a date but f14 count is 0.
                   This means we came into f14 from a date but not a f14 date.
            D25:
                1) Return if we're not in d25 mode. This assured that the labels won't run before the intro.
                2) Return if the function returns True. Check should_AHC_return_on_d25 for the full conditions.
        """

        return (
                (
                store.mas_isO31()
                and (
                    not store.persistent._mas_o31_in_o31_mode
                    or (store.ahc_utils.isWearingClothesOfExpropValue("o31") and not store.mas_globals.ahc_run_after_date)
                )
            )
            or (
                store.mas_isF14()
                and (
                    not store.persistent._mas_f14_in_f14_mode
                    or (store.mas_globals.ahc_run_after_date and not store.persistent._mas_f14_date_count)
                )
            )
            or (
                store.mas_isD25Season()
                and (not store.persistent._mas_d25_in_d25_mode or store.ahc_utils.should_AHC_return_on_d25())
            )
        )

init -2 python in mas_sprites:
    import store

    def _outfit_wear_if_gifted(_moni_chr, outfit_name, by_user=False, outfit_mode=False):
        """
        Wears the outfit if it exists and has been gifted/reacted.
        It has been gifted/reacted if the selectable is unlocked.

        IN:
            _moni_chr - MASMonika object
            outfit_name - name of the outfit
            by_user - True if this action was mandated by user, False if not.
                (Default: False)
            outfit_mode - True means we should change hair/acs if it
                completes the outfit. False means we should not.
                (Default: False)
        """
        outfit_to_wear = store.mas_sprites.get_sprite(
            store.mas_sprites.SP_CLOTHES,
            outfit_name
        )
        if outfit_to_wear is not None and store.mas_SELisUnlocked(outfit_to_wear):
            _moni_chr.change_clothes(outfit_to_wear, by_user=by_user, outfit_mode=outfit_mode)

init -19 python in ahc_utils:
    import store
    import datetime
    import time

    def MASToDtTime(mas_time):
        """
        Converts a MAS time (settings menu) to datetime.datetime

        IN:
            mas_time - MAS settings time to convert to dt time

        OUT:
            the time in dt time.
        """
        return datetime.datetime.combine(datetime.date.today(), datetime.time(hour=mas_time/60, minute=mas_time%60))

default persistent.hair_down_suntime_states = []

init 50 python:
    def setHairDownSuntimeStates():
        # Save the following values that we will need for hasHairDownRun
        #   If currently it is between sunset and midnight
        #   If currently it is between midnight and sunrise
        #   Today's sunrise dt, converted from MAS time
        #   Today's sunset dt, converted from MAS time

        _now = datetime.datetime.now()

        persistent.hair_down_suntime_states = [
            store.mas_isSStoMN(_now),
            store.mas_isMNtoSR(_now),
            store.ahc_utils.MASToDtTime(store.persistent._mas_sunrise),
            store.ahc_utils.MASToDtTime(store.persistent._mas_sunset)
        ]

    #Reset the ahc evs here as well in case they somehow lost their conditionals/actions

    def ahc_recond_ponytail():
        """
        Recondition and action the ahc ponytail event
        """
        hairup_ev = mas_getEV("monika_sethair_ponytail")

        hairup_ev.conditional=(
            "mas_isDayNow() "
            "and (not store.ahc_utils.hasHairPonytailRun() "
            "or store.mas_globals.ahc_run_after_date) "
            "and (store.ahc_utils.shouldChangeHair('day') "
            "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
        )
        hairup_ev.action = EV_ACT_QUEUE

    def ahc_recond_down():
        """
        Recondition and action the ahc down event
        """
        hairdown_ev = mas_getEV("monika_sethair_down")

        hairdown_ev.conditional=(
            "mas_isNightNow() "
            "and (not store.ahc_utils.hasHairDownRun() "
            "or store.mas_globals.ahc_run_after_date) "
            "and (store.ahc_utils.shouldChangeHair('night') "
            "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
        )
        hairdown_ev.action = EV_ACT_QUEUE

    #Only ahc hair down event and the equivalent startup trigger event should be able to call this
    def ahc_recond_pjs():
        """
        Recondition and action the ahc pjs event
        """
        pjs_ev = mas_getEV("monika_setoutfit_pjs")

        if pjs_ev:
            _pj_thresh = 21
            _sunrise_hour = int(mas_cvToDHM(persistent._mas_sunrise)[0:2])
            _sunset_hour = int(mas_cvToDHM(persistent._mas_sunset)[0:2])
            _now = datetime.datetime.now()
            _yesterday = _now.date() - datetime.timedelta(days=1)

            _date = _now.date() if store.mas_isSStoMN(_now) else _yesterday

            # If the sunset is after the thresh, start_date will be an hour after the sunset hour
            if _sunset_hour >= _pj_thresh:
                _time = _sunset_hour + 1 if _sunset_hour < 23 else _sunset_hour
            # Else, if the sunset is us to an hour before the thresh, start_date will be an hour after the thresh
            elif _pj_thresh - _sunset_hour <= 1:
                _time = _pj_thresh + 1
            # Else the start_date will be the thresh
            else:
                _time = _pj_thresh

            pjs_ev.start_date = datetime.datetime.combine(_date, datetime.time(hour=_time))

            pjs_ev.end_date = datetime.datetime.combine(
                pjs_ev.start_date.date() + datetime.timedelta(days=1),
                datetime.time(hour=_sunrise_hour - 1 if _sunrise_hour > 0 else _sunrise_hour)
            )

            pjs_ev.action=EV_ACT_QUEUE

    ahc_recond_ponytail()
    ahc_recond_down()

init 51 python:
    def ahc_recond_ahc_label(label_name):
        label_map = {
            "monika_sethair_ponytail": "store.ahc_recond_ponytail()",
            "monika_sethair_down": "store.ahc_recond_down()",
            "monika_setoutfit_pjs": "store.ahc_recond_pjs()",
        }

        if label_name in label_map:
            eval(label_map[label_name])

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_sethair_ponytail",
            conditional=(
                "mas_isDayNow() "
                "and (not store.ahc_utils.hasHairPonytailRun() "
                "or store.mas_globals.ahc_run_after_date) "
                "and (store.ahc_utils.shouldChangeHair('day') "
                "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
            ),
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label monika_sethair_ponytail:

    #Need to recondition/action this
    $ store.ahc_recond_ponytail()

    if store.ahc_utils.should_AHC_label_return():
        #Reset our global var if we return
        if store.mas_globals.ahc_run_after_date:
            $ store.mas_globals.ahc_run_after_date = False
        return

    python:
        #NOTE: The random chances here are for chance to NOT change. A chance of 1 means that Monika won't change.

        # If we're coming home from a date always change clothes
        # Change hair only if Monika doesn't have day hair
        if store.mas_globals.ahc_run_after_date:
            _clothes_random_chance = 2
            _hair_random_chance = 2 if not store.ahc_utils.isWearingDayHair() else 1
        else:
            # Don't change clothes we saw the D25 intro today, it's F14 or O31
            # We assume that Monika already changed because of the intro
            if (
                store.ahc_utils.check_first_day_d25s()
                or store.mas_isF14()
                or store.mas_isO31()
            ):
                _clothes_random_chance = 1
            else:
                _clothes_random_chance = renpy.random.randint(1,3)

            # Don't change hair if it's O31 and Monika is wearing a costume.
            _hair_random_chance = 1 if (store.mas_isO31() and store.ahc_utils.isWearingClothesOfExpropValue("o31")) else renpy.random.randint(1,4)

        _clothes_exprop = store.ahc_utils.getClothesExpropForTemperature()

    if (
            (
            store.ahc_utils.shouldChangeClothes(_clothes_exprop)
            and (
                not store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop)
                or (
                    store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop)
                    and len(store.ahc_utils.getOutfitsOfExprop(_clothes_exprop)) > 1
                    and _clothes_random_chance != 1
                )
            )
        )
        or (
            (
                len(store.ahc_utils.getDayHair()) > 1
                and store.ahc_utils.isWearingDayHair()
                and store.ahc_utils.isWearingNightHair()
                and _hair_random_chance != 1
            )
            or (
                len(store.ahc_utils.getDayHair()) > 0
                and not store.ahc_utils.isWearingDayHair()
            )
        )
    ):

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            if store.mas_globals.ahc_run_after_date:
                m 1eua "I'm just going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{w=1}{nw}"
            else:
                m 3eua "I'm going to get ready for today.{w=0.5}.{w=0.5}.{w=1}{nw}"

        else:
            if store.mas_globals.ahc_run_after_date:
                m 1eua "Give me a moment [mas_get_player_nickname()], I'm going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{nw}"
            else:
                m 1eua "Give me a second, [mas_get_player_nickname()]."
                m 3eua "I'm just getting myself ready for the day.{w=0.5}.{w=0.5}.{nw}"

        #Reset our global var here
        if store.mas_globals.ahc_run_after_date:
            $ store.mas_globals.ahc_run_after_date = False

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
                "and (not store.ahc_utils.hasHairDownRun() "
                "or store.mas_globals.ahc_run_after_date) "
                "and (store.ahc_utils.shouldChangeHair('night') "
                "or store.ahc_utils.shouldChangeClothes(store.ahc_utils.getClothesExpropForTemperature())) "
            ),
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )


label monika_sethair_down:

    #Need to recondition/action this
    $ ahc_recond_down()

    # Update out persist var
    $ store.setHairDownSuntimeStates()

    if store.ahc_utils.should_AHC_label_return():
        #Reset our global var if we return
        if store.mas_globals.ahc_run_after_date:
            $ store.mas_globals.ahc_run_after_date = False
        return

    python:
        #NOTE: The random chances here are for chance to NOT change. A chance of 1 means that Monika won't change.

        # If we're coming home from a date always change clothes
        # Change hair only if Monika doesn't have day hair
        if store.mas_globals.ahc_run_after_date:
            _clothes_random_chance = 2
            _hair_random_chance = 2 if not store.ahc_utils.isWearingNightHair() else renpy.random.randint(1,4)
        else:
            # Don't change clothes we saw the D25 intro today, it's F14 or O31
            # We assume that Monika already changed because of the intro
            if (
                store.ahc_utils.check_first_day_d25s()
                or store.mas_isF14()
                or store.mas_isO31()
            ):
                _clothes_random_chance = 1
            else:
                _clothes_random_chance = renpy.random.randint(1,3)

            # Don't change hair if it's O31 and Monika is wearing a costume.
            _hair_random_chance = 1 if (store.mas_isO31() and store.ahc_utils.isWearingClothesOfExpropValue("o31")) else renpy.random.randint(1,4)

        _clothes_exprop = store.ahc_utils.getClothesExpropForTemperature()

        #Reset our global var here
        if store.mas_globals.ahc_run_after_date:
            store.mas_globals.ahc_run_after_date = False

        _time_till_start_date = None

        if store.ahc_utils.hasUnlockedClothesOfExprop("pajamas"):
            # Recond the pjs topic
            store.ahc_recond_pjs()

            pjs_ev = mas_getEV("monika_setoutfit_pjs")

            if pjs_ev is not None and pjs_ev.start_date is not None:
                _time_till_start_date = pjs_ev.start_date - datetime.datetime.now()

    if (
        (
            store.ahc_utils.shouldChangeClothes(_clothes_exprop)
            and (
                not store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop)
                or (
                    store.ahc_utils.isWearingClothesOfExprop(_clothes_exprop)
                    and len(store.ahc_utils.getOutfitsOfExprop(_clothes_exprop)) > 1
                    and _clothes_random_chance != 1
                )
            )
        )
        or (
            (
                len(store.ahc_utils.getNightHair()) > 1
                and store.ahc_utils.isWearingDayHair()
                and store.ahc_utils.isWearingNightHair()
                and _hair_random_chance != 1
            )
            or (
                len(store.ahc_utils.getNightHair()) > 0
                and not store.ahc_utils.isWearingNightHair()
            )
        )
        or _time_till_start_date and _time_till_start_date <= datetime.timedelta(hours=1)
    ):

        if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
            m 1eua "I'm just going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{w=1}{nw}"
        else:
            m 1eua "Give me a moment [mas_get_player_nickname()], I'm going to make myself a little more comfortable.{w=0.5}.{w=0.5}.{nw}"

        window hide
        call mas_transition_to_emptydesk

        python:
            renpy.pause(1.0, hard=True)

            # If we're close to the pj topic's start_date then change immediately to pjs
            if _time_till_start_date and _time_till_start_date <= datetime.timedelta(hours=1):
                store.ahc_utils.changeHairAndClothes(
                    _day_cycle="night",
                    _hair_random_chance=_hair_random_chance,
                    _clothes_random_chance=2,
                    _exprop="pajamas"
                )

                # Strip and remove the event from the event list so that it doesn't trigger twice
                store.mas_stripEVL("monika_setoutfit_pjs", list_pop=True)

            else:
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


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_setoutfit_pjs",
            action=EV_ACT_QUEUE,
            show_in_idle=True,
            rules={"skip alert": None}
        ),
        restartBlacklist=True
    )

label monika_setoutfit_pjs:

    #If we asked Monika to change clothes by the time this is triggered, the event was somehow triggered and we
    #a) don't have any unlocked PJ's, or Monika is already wearing them (possible gift reaction)
    #As such, we should return here.
    if not ahc_utils.shouldChangeClothes("pajamas") or ahc_utils.isWearingClothesOfExprop("pajamas"):
        return

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "I'm just going to put on my pajamas.{w=0.5}.{w=0.5}.{w=1}{nw}"
    else:
        m 1eua "Give me a moment [mas_get_player_nickname()], I'm going to put on my pajamas.{w=0.5}.{w=0.5}.{nw}"

    window hide
    call mas_transition_to_emptydesk

    python:
        renpy.pause(1.0, hard=True)

        store.ahc_utils.changeHairAndClothes(
            _day_cycle="night",
            _hair_random_chance=1,
            _clothes_random_chance=2,
            _exprop="pajamas"
        )

        renpy.pause(4.0, hard=True)

    call mas_transition_from_emptydesk("monika 1eua")
    window hide

    if store.mas_globals.in_idle_mode or (mas_canCheckActiveWindow() and not mas_isFocused()):
        m 1eua "That feels better.{w=1}{nw}"

    else:
        m 1eua "That feels much better."

    # If we took her out during the day and returned late in the night, there's a chance
    # that monika_setoutfit_pjs will run before monika_sethair_down.
    # This ensures that she won't change twice by removing monika_sethair_down from the event list.

    python:
        if (
            store.mas_inEVL("monika_sethair_down")
            or not store.ahc_utils.hasHairPonytailRun()
        ):
            mas_setEVLPropValues("monika_sethair_down", last_seen=datetime.datetime.now())
            store.mas_rmEVL("monika_sethair_down")
            store.ahc_recond_down()
            store.setHairDownSuntimeStates()
            if store.mas_globals.ahc_run_after_date:
                store.mas_globals.ahc_run_after_date = False

    return
