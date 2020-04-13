init -990 python in mas_submod_utils:
    Submod(
        author="multimokia and Legendkiller21",
        name="Auto Atmos Change",
        description="This submod allows Monika's room to match either the weather or the sunrise and sunset times (or both) to your own location.",
        version="2.0.0",
        settings_pane="auto_atmos_change_settings"
    )

init -1 python:
    tt_awc_desc = (
        "Enable this to allow {i}progressive{/i} weather to automatically match the weather at your location."
    )

    tt_ast_desc = (
        "Enable this to allow the sunrise and sunset times in MAS to match your location."
    )

#Our settings + Status pane
screen auto_atmos_change_settings():
    $ submods_screen_tt = store.renpy.get_screen("submods", "screens").scope["tooltip"]
    vbox:
        box_wrap False
        xfill True
        xmaximum 1000

        hbox:
            if bool(persistent._awc_API_key):
                style_prefix mas_ui.cbx_style_prefix
                box_wrap False
                textbutton _("Auto Weather Change"):
                    action ToggleField(persistent, "_awc_enabled")
                    selected persistent._awc_enabled
                    hovered SetField(submods_screen_tt, "value", tt_awc_desc)
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

                textbutton _("Auto Sun Times"):
                    action Function(store.awc_utils.toggleAST)
                    selected persistent._awc_ast_enabled
                    hovered SetField(submods_screen_tt, "value", tt_ast_desc)
                    unhovered SetField(submods_screen_tt, "value", submods_screen_tt.default)

            else:
                text "Please add a valid API key to use this submod.": #You can create one {a=https://openweathermap.org/api}{i}{u}here{/u}{/i}{/a}.":
                    xalign 1.0 yalign 0.0
                    style mas_ui.mm_tt_style

    if bool(persistent._awc_API_key):
        text "API Key Valid":
            xalign 1.0 yalign 0.0
            xoffset -10
            style mas_ui.mm_tt_style

#The api key we'll use to access Open Weather Network's data
default persistent._awc_API_key = None

#Whether or not we have Auto Weather Change enabled
default persistent._awc_enabled = True

#Whether or not we have Auto Sun Times enabled
default persistent._awc_ast_enabled = True

init -18 python:
    #Initialize the lookup
    awc_buildCityLookupDict()

    #Create our async wrapper for weather progress
    await_weatherProgress = store.mas_threading.MASAsyncWrapper(
        store.awc_weatherProgress
    )

init -10 python in awc_utils:
    import store
    def toggleAST():
        """
        Toggles the auto-sun-times functionality
        """
        if store.persistent._awc_ast_enabled:
            store.persistent._awc_ast_enabled = False

        else:
            #If we're enabling this, we should reajust the values
            store.persistent._awc_ast_enabled = True
            store.persistent._mas_sunrise = store.awc_dtToMASTime(store.awc_getSunriseDT())
            store.persistent._mas_sunset = store.awc_dtToMASTime(store.awc_getSunsetDT())

    #And do the startup check here too
    if (
        store.persistent._awc_ast_enabled
        and store.awc_canGetAPIWeath()
        and store.awc_testConnection()
    ):
        store.persistent._mas_sunrise = store.awc_dtToMASTime(store.awc_getSunriseDT())
        store.persistent._mas_sunset = store.awc_dtToMASTime(store.awc_getSunsetDT())

init -200 python in awc_globals:
    #Store base url in a global store
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    #Stores the time at which it should check whether weather should change
    weather_check_time = None

    #Stores the time when we go back to normal progressive weather if no connection
    weather_offline_timeout = None

# Api key setup
init -21 python:
    import store
    import urllib2
    def awc_testURL(url):
        """
        Attempts to open the url provided

        IN:
            url - url to test

        OUT:
            True if successful, error code if connected, but got error. False if no connection
        """
        try:
            urllib2.urlopen(url)
            return True
        except urllib2.HTTPError as e:
            return e.code
        except urllib2.URLError:
            return False

    def awc_testConnection():
        """
        Checks if we have internet connection

        OUT:
            True if successful, False otherwise
        """
        if not awc_testURL("http://www.google.com"):
            return False
        return True

    def awc_isInvalidAPIKey(api_key):
        """
        Checks if api key is invalid

        IN:
            api_key - api key to check

        OUT:
            True if api key returns a 401 error (invalid), False otherwise
        """
        return awc_testURL(store.awc_globals.BASE_URL + "appid=" + str(api_key) + "&q=London,uk") == 401

    def awc_apiKeySetup():
        """
        Sets up the api key from the txt file.

        OUT:
            True if api key was good. False otherwise
        """
        api_key = (renpy.config.basedir + '/apikey.txt').replace("\\", "/")

        #If file isn't loadable, return
        if not renpy.loadable(api_key):
            return False

        with renpy.file(api_key) as apik_data:
            for line in apik_data:
                line = line.strip()

                #Only set if api key is valid
                if not awc_isInvalidAPIKey(line):
                    store.persistent._awc_API_key = line
                    return True
        return False

init -20 python in awc_globals:
    #First append sys path here
    import sys
    import store
    sys.path.append(renpy.config.gamedir + '\\python-packages\\pyowm-2.8.0-py2.7.egg')

    #Let's get our weather bit
    from pyowm import OWM

    #Call the api key setup
    if store.awc_isInvalidAPIKey(store.persistent._awc_API_key):
        store.awc_apiKeySetup()

    #Now create the open weather map object
    owm = OWM(store.persistent._awc_API_key)

    #Weather status keywords
    SUN_KW = ['clear', 'sun']
    THUNDER_KW = ['storm', 'hurricane', 'tornado', 'thunderstorm']
    SNOW_KW = ['snow', 'sleet']

    #Weather thresh constants
    OVERCAST_CLOUD_THRESH = 75
    RAIN_RATE_THRESH = 3

    #Depreciated
    OVERCAST_KW = ['clouds', 'fog', 'haze', 'mist', 'light rain', 'broken clouds']
    RAIN_KW = ['rain', 'drizzle']

#NOTE: We create this dict here so we can check for existence of player location at the right init
#If player just installed a submod requiring something being done on load
init -20 python:
    if not store.persistent._awc_player_location:
        store.persistent._awc_player_location = {
            "city": None,
            "country": None,
            "lat": None,
            "lon": None,
            "loc_pref": None
        }

#Helper methods
init -19 python:
    import store
    import datetime
    import time
    import random

    def awc_isInvalidLocation(city_code, country_code=""):
        """
        Checks if location is invalid

        IN:
            city_code - the city to check
            country_code - the country to check (optional)

        OUT:
            True if we get a 404 error, False otherwise

        NOTE: It is assumed that we checked for a valid api key first, since bad api key rets False.
        """
        #First, check if valid api key
        if awc_isInvalidAPIKey(store.persistent._awc_API_key):
            return False

        #Now, test the url
        if not country_code:
            return awc_testURL(store.awc_globals.BASE_URL + "appid=" + persistent._awc_API_key + "&q=" + city_code) == 404
        else:
            return awc_testURL(store.awc_globals.BASE_URL + "appid=" + persistent._awc_API_key + "&q=" + city_code + "," + country_code) == 404

    def awc_getCityCountry(city_name):
        """
        Gets the country the provided city is in

        IN:
            city_name - the city to get the country of.

        OUT:
            the country code of the city given

        NOTE: Assumes that city_name is a valid city
        """
        return store.awc_globals.owm.weather_at_place(city_name).get_location().get_country()

    def awc_getFriendlyCityCountry(city_name):
        """
        Gets the friendly country for city_name

        IN:
            city_name - the city to get the country of

        OUT:
            the full country city_name is located in

        NOTE: Assumes that city_name is a valid city
        """
        return store.awc_utils.country_code_lookup.get(awc_getCityCountry(city_name),awc_getCityCountry(city_name))

    def awc_getFriendlyCountry(country_code):
        """
        Gets the friendly country name for country_code

        IN:
            country_code - the country code to check for

        OUT:
            the full country name
        """
        return store.awc_utils.country_code_lookup.get(country_code, country_code)

    def awc_getSunriseDT():
        """
        Gets the datetime.datetime of sunrise for player location

        OUT:
            datetime.datetime representing sunrise for player location (timezone calculated)

        NOTE: Assumes we can get an observation
        """
        if time.localtime().tm_isdst:
            return (
                awc_getObservation().get_weather().get_sunrise_time('date')
                - datetime.timedelta(seconds=time.timezone)
                + datetime.timedelta(hours=1)
            ).replace(tzinfo=None)

        else:
            return (
                awc_getObservation().get_weather().get_sunrise_time('date') - datetime.timedelta(seconds=time.timezone)
            ).replace(tzinfo=None)

    def awc_getSunsetDT():
        """
        Gets the datetime.datetime of sunset for player location

        OUT:
            datetime.datetime representing sunset for player location (timezone calculated)

        NOTE: Assumes we can get an observation
        """
        if time.localtime().tm_isdst:
            return (
                awc_getObservation().get_weather().get_sunset_time('date')
                - datetime.timedelta(seconds=time.timezone)
                + datetime.timedelta(hours=1)
            ).replace(tzinfo=None)
        else:
            return (
                awc_getObservation().get_weather().get_sunset_time('date') - datetime.timedelta(seconds=time.timezone)
            ).replace(tzinfo=None)

    def awc_dtToMASTime(dt):
        """
        Converts a datetime.datetime to MAS time (settings menu)

        IN:
            dt - datetime.datetime object of the time to convert to MAS time

        OUT:
            the time in MAS settings time.
        """
        return dt.minute + dt.hour * 60

    def awc_lookupCity(city_name):
        """
        Gets a list of all cities with city_name from the reference dict

        IN:
            city_name - the city to lookup

        OUT:
            if city is in the lookup table, then return the list from the lookup
            else, we return None (NOTE: this IS possible)
        """

        #First, build the lookup dict
        if not store.awc_utils.city_lookup:
            awc_buildCityLookupDict()

        return store.awc_utils.city_lookup.get(city_name)

    def awc_hasMultipleLocations(city_name):
        """
        Checks if there's more than one location for city_name

        IN:
            city_name - the city to check for

        OUT:
            if more than one location present, True. False otherwise
            False also if city isn't in lookup table
        """
        city_matches = awc_lookupCity(city_name)

        if city_matches:
            return len(city_matches) > 1
        return False

    def awc_buildCityMenuItems(city_name):
        """
        Builds a displayable city name/list of names (for buttons/dlg)

        IN:
            city_name - the city to build the full name for

        OUT:
            list of display names for the city in the form for a scrollable menu
        """
        city_matches = awc_lookupCity(city_name)

        scrollable_list = []
        if city_matches:
            for place in city_matches:
                #Build the name
                disp_text = city_name + ", " + place[3] + ", " + awc_getFriendlyCountry(place[0])
                scrollable_list.append((
                    disp_text,
                    (place[1], place[2]),
                    False,
                    False
                ))
        return scrollable_list

    def awc_buildWeatherLocation(city_name, country_code):
        """
        Builds a weather name (for owm to get weather from place)

        IN:
            city_name - the city name
            country_code - the country code

        OUT:
            the player location (city/country code) in the weather_at_place() acceptable form
        """
        return city_name + ", " + country_code

    def awc_savePlayerLatLonTup(latlon):
        """
        Saves the weather location tuple to the persist _awc_player_location dict

        IN:
            latlon - latlon tuple to save
        """
        lat, lon = latlon

        if lat and lon:
            store.persistent._awc_player_location["lat"] = lat
            store.persistent._awc_player_location["lon"] = lon

    def awc_savePlayerCityCountryTup(citycountry):
        """
        Saves the weather location tuple to the persist _awc_player_location dict

        IN:
            citycountry - the citycountry tuple to save
        """

        city, country = citycountry

        if city and country:
            store.persistent._awc_player_location["city"] = city
            store.persistent._awc_player_location["country"] = country

    def awc_buildWeatherLocationTup(citycountry):
        """
        Builds a weather name (owm.weather_from_place) from tuple of city/country

        IN:
            citycountry - tuple for city, country

        OUT:
            the player locaton (city/country code) in the weather_at_place() acceptable form
        """
        return awc_buildWeatherLocation(citycountry[0], citycountry[1])

    def awc_hasPlayerCoords():
        """
        Checks if we have player coords

        OUT:
            True if we have both latitude and longditude of the player
            False otherwise
        """
        lat = store.persistent._awc_player_location.get("lat")
        lon = store.persistent._awc_player_location.get("lon")

        return lat is not None and lon is not None

    def awc_hasPlayerCityCountry():
        """
        Checks if we have player city and country
        """
        city = store.persistent._awc_player_location.get("city")
        country = store.persistent._awc_player_location.get("country")

        return city is not None and country is not None

    def awc_getPlayerCoords():
        """
        Gets the player's coords from the persist _awc_player_location dict as tuple

        OUT:
            player co-ords as a tuple

        NOTE: Assumes we've checked that we have player coords before using this
        """
        return (store.persistent._awc_player_location["lat"], store.persistent._awc_player_location["lon"])

    def awc_getPlayerCityCountry():
        """
        Gets the player's city and country from the persist _awc_player_location dict as tuple

        OUT:
            player city, country as tuple

        NOTE: Assumes we've checked that we have player city/country before this
        """
        return (store.persistent._awc_player_location["city"], store.persistent._awc_player_location["country"])

    def awc_weathByCityCountryTup(citycountry):
        """
        Gets the weather for the location by citycountry tuple

        IN:
            citycountry - tuple of city and country

        OUT:
            observation of the weather at the given city/country
        """
        if not citycountry:
            citycountry = awc_getPlayerCityCountry()

        return store.awc_globals.owm.weather_at_place(awc_buildWeatherLocationTup(citycountry))

    def awc_weathByCoords(coords):
        """
        Gets the weather for the location by coords

        IN:
            coords - tuple, (lat,lon)

        OUT:
            observation of weather for the given coords
        """
        if not coords:
            coords = awc_getPlayerCoords()

        return store.awc_globals.owm.weather_at_coords(coords[0], coords[1])

    def awc_buildCityLookupDict():
        """
        Builds the lookup dict for city lookups
        """
        loc_data_dict = dict()
        lookup_file = renpy.config.gamedir.replace("\\", '/') + "/Submods/Auto Weather Change/Utilities/awc_citylookup.txt"

        with renpy.file(lookup_file) as loc_dat:
            for line in loc_dat:
                line = line.strip()

                if line == '' or line[0] == '#': continue

                x = line.split(',')

                #If no entry for this yet, then we make it
                if not loc_data_dict.get(x[0]):
                    loc_data_dict[x[0]] = list()

                loc_data_dict[x[0]].append((
                    x[1], #Country code
                    float(x[2]), #Lat
                    float(x[3]), #Lon
                    x[4]  #Province/State
                    )
                )

        store.awc_utils.city_lookup = loc_data_dict.copy()

    def awc_canGetAPIWeath():
        """
        Checks if we can get weather from api by checking if we have player location and a valid api key

        OUT:
            True if we can get api weather
            False otherwise
        """
        return (
            (awc_hasPlayerCityCountry() or awc_hasPlayerCoords())
            and not awc_isInvalidAPIKey(store.persistent._awc_API_key)
        )

    def awc_offlineTimerCheck():
        """
        Checks whether we should start or reset the offline timer and whether we timed out

        OUT:
            False if we have connection or if we have not timed out
            True if we have timed out

        NOTE: safe bet is to call this from a function called asynchronously
        """
        #If false then we have no connection
        if not awc_testConnection():
            _now = datetime.datetime.now()

            #If false start the timer and return false to pass
            if not store.awc_globals.weather_offline_timeout:
                store.awc_globals.weather_offline_timeout = _now + datetime.timedelta(0,1800)
                return False

            #Else if the timer started and we have not timed out return false to pass
            elif store.awc_globals.weather_offline_timeout and store.awc_globals.weather_offline_timeout > _now:
                return False

            #Else you shall not pass if we have timed out
            else:
                return True

        else:
            #Else we have connection and if the timer has started then reset it
            if store.awc_globals.weather_offline_timeout:
                store.awc_globals.weather_offline_timeout = None
            return False

    def awc_getObservation():
        """
        Gets the weather observation by player coords (if we have) or city/country (if we have)

        OUT:
            weather observation for player location (if we have it) or None if we don't
        """
        #What's preferred?
        pref_locator = store.persistent._awc_player_location["loc_pref"]

        if pref_locator == "latlon":
            #We have player co-ords? Use that
            if awc_hasPlayerCoords():
                return awc_weathByCoords(awc_getPlayerCoords())

        elif pref_locator == "citycountry":
            #We have player city and country? use that
            if awc_hasPlayerCityCountry():
                return awc_weathByCityCountryTup(awc_getPlayerCityCountry())

        return None

    def awc_weathFromAPI():
        """
        Gets weather based off the api results

        OUT:
            returns the weather to show based on current

        NOTE: Assumes that we have a form of location
        """
        observation = awc_getObservation()

        if awc_isThunderWeather(observation):
            return store.mas_weather_thunder

        elif awc_isRainWeather(observation):
            return store.mas_weather_rain

        elif awc_isSnowWeather(observation):
            return store.mas_weather_snow

        elif awc_isOvercastWeather(observation):
            return store.mas_weather_overcast

        else:
            return store.mas_weather_def

    def awc_isSunWeather(observation=None):
        """
        Checks if current weather description or detailed description is in the sun keywords list

        IN:
            observation - The weather observation to use to check
            NOTE: if not provided, it is acquired via the api

        OUT:
            True if weather is in sun keywords, False otherwise
        """
        if not observation:
            observation = awc_getObservation()

        weather_desc = observation.get_weather().get_status().lower()
        detailed_weather_desc = observation.get_weather().get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.SUN_KW
            or detailed_weather_desc in store.awc_globals.SUN_KW
        )

    def awc_isOvercastWeather(observation=None):
        """
        Checks if current cloud level is > 75%

        IN:
            observation - The weather observation to use to check
            NOTE: if not provided, it is acquired via the api

        OUT:
            True if cloud level is > 75%
        """
        if not observation:
            observation = awc_getObservation()

        return observation.get_weather().get_clouds() > store.awc_globals.OVERCAST_CLOUD_THRESH

    def awc_isRainWeather(observation=None):
        """
        Checks if hourly rain rate >= 3 millimeters/hour

        IN:
            observation - The weather observation to use to check
            NOTE: if not provided, it is acquired via the api

        OUT:
            True if the hourly rain rate (mm/hour) is >= 3. False otherwise
        """
        if not observation:
            observation = awc_getObservation()

        rain_dict = observation.get_weather().get_rain()

        #First, let's see if there's anthing in the dict.
        #If not, we just return False as that means no rain
        if len(rain_dict) == 0:
            return False

        #Now let's see if there's a 3 hr
        three_hour_rain = rain_dict.get("3h")

        if three_hour_rain:
            #Now we need to do a little bit of math and convert this to a per hour rate
            hour_rate = three_hour_rain/3.0

        #There's no 3 hour rain? Must be one hour instead then
        else:
            hour_rate = rain_dict.get("1h")

        #If the hourly rate is >= 3, we consider this to be rain
        return hour_rate >= store.awc_globals.RAIN_RATE_THRESH

    def awc_isThunderWeather(observation=None):
        """
        Checks if current weather description or detailed description is in the thunder keywords list

        IN:
            observation - The weather observation to use to check
            NOTE: if not provided, it is acquired via the api

        OUT:
            True if weather is in thunder keywords, False otherwise
        """
        if not observation:
            observation = awc_getObservation()

        weather_desc = observation.get_weather().get_status().lower()
        detailed_weather_desc = observation.get_weather().get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.THUNDER_KW
            or detailed_weather_desc in store.awc_globals.THUNDER_KW
        )

    def awc_isSnowWeather(observation=None):
        """
        Checks if current weather description or detailed description is in the snow keywords list

        IN:
            observation - The weather observation to use to check
            NOTE: if not provided, it is acquired via the api

        OUT:
            True if weather is in snow keywords, False otherwise
        """
        if not observation:
            observation = awc_getObservation()

        weather_desc = observation.get_weather().get_status().lower()
        detailed_weather_desc = observation.get_weather().get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.SNOW_KW
            or detailed_weather_desc in store.awc_globals.SNOW_KW
        )

    def awc_getTemperature(observation=None, temp="temp"):
        """
        Checks the temperature at the player's location

        IN:
            observation - The weather observation to use to check
            NOTE: if not provided, it is acquired via the api
            temp - The temperature we want to check. Accepts the following values
                1) "temp_min": Min current temperature in the city
                2) "temp": Current temperature
                3) "temp_max": Max current temperature in the city
            (Default: "temp")

            NOTE: "temp_min" and "temp_max" are optional parameters.
            Mean the min / max temperature in the city at the current moment to see deviation from current
            temp just for your reference.

        OUT:
            The temperature depending on the provided temp value
        """

        if not observation:
            observation = awc_getObservation()

        if not temp:
            temp = "temp"

        return observation.get_weather().get_temperature(unit='celsius')[temp]

    def awc_weatherProgress():
        """
        Asyncronous weather progress container.

        NOTE: This should be called asyncronously

        See weatherProgress for details.
        """
        #If the player forced weather or we're not in a background that supports weather, we do nothing
        if store.mas_weather.force_weather or store.mas_current_background.disable_progressive:
            return False

        #Otherwise we do stuff

        #Set a time for startup
        if not store.awc_globals.weather_check_time:
            store.awc_globals.weather_check_time = datetime.datetime.now() + datetime.timedelta(0,300)

        elif store.awc_globals.weather_check_time < datetime.datetime.now():
            #Need to set a new check time
            store.awc_globals.weather_check_time = datetime.datetime.now() + datetime.timedelta(0,300)

            if (
                store.persistent._awc_enabled
                and (
                    (awc_testConnection() and store.awc_canGetAPIWeath())
                    or (not awc_testConnection() and store.awc_canGetAPIWeath() and not awc_offlineTimerCheck())
                )
            ):
                if awc_testConnection():
                    #We have connection and a valid url. Get weath from api
                    new_weather = store.awc_weathFromAPI()

                    #Reset timeout if need be
                    if store.awc_globals.weather_offline_timeout:
                        store.awc_globals.weather_offline_timeout = None

                else:
                    #No connection, keep current weather
                    new_weather = store.mas_current_weather
                    return False

                #Do we need to change weather?
                if new_weather != store.mas_current_weather:
                    #Let's see if we need to scene change
                    store.mas_weather.should_scene_change = store.mas_current_background.isChangingRoom(
                        store.mas_current_weather,
                        new_weather
                    )

                    #Now we change weather
                    store.mas_changeWeather(new_weather)

                    #Play the rumble in the back to indicate thunder
                    if new_weather == store.mas_weather_thunder:
                        renpy.play("mod_assets/sounds/amb/thunder_1.wav",channel="backsound")
                    return True

            else:
                #Set a time for startup
                if not store.mas_weather.weather_change_time:
                    store.mas_weather.weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))

                elif store.mas_weather.weather_change_time < datetime.datetime.now():
                    #Need to set a new check time
                    store.mas_weather.weather_change_time = datetime.datetime.now() + datetime.timedelta(0,random.randint(1800,5400))

                    #Change weather
                    new_weather = store.mas_shouldRain()

                    if new_weather is not None and new_weather != store.mas_current_weather:
                        #Let's see if we need to scene change
                        store.mas_weather.should_scene_change = store.mas_current_background.isChangingRoom(
                            store.mas_current_weather,
                            new_weather
                        )

                        #Now we change weather
                        store.mas_changeWeather(new_weather)

                        #Play the rumble in the back to indicate thunder
                        if new_weather == store.mas_weather_thunder:
                            renpy.play("mod_assets/sounds/amb/thunder_1.wav",channel="backsound")
                        return True

                    elif store.mas_current_weather != store.mas_weather_def:
                        #Let's see if we need to scene change
                        store.mas_weather.should_scene_change = store.mas_current_background.isChangingRoom(
                            store.mas_current_weather,
                            store.mas_weather_def
                        )

                        store.mas_changeWeather(store.mas_weather_def)
                        return True

        return False