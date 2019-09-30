#Loc dict
default persistent._awc_player_location = {
    "city": None,
    "country": None,
    "lat": None,
    "lon": None,
    "loc_pref": None
}

default persistent._awc_API_key = None

init -18 python:
    #Initialize the lookup
    awc_buildCityLookupDict()

init -200 python in awc_globals:
    #Store base url in a global store
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


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
            True if successful, error code if not
        """
        try:
            urllib2.urlopen(url)
            return True
        except urllib2.HTTPError as e:
            return e.code

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

    # Weather status keywords
    SUN_KW = ['clear', 'sun']
    OVERCAST_KW = ['clouds', 'fog', 'haze', 'mist', 'light rain', 'broken clouds']
    RAIN_KW = ['rain', 'drizzle']
    THUNDER_KW = ['storm', 'hurricane', 'tornado', 'thunderstorm']
    SNOW_KW = ['snow', 'sleet']


#Helper methods
init -19 python:
    import store

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
                disp_text = city_name + ", " + place[3] + ". " + awc_getFriendlyCountry(place[0])
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
        if awc_isSunWeather():
            return store.mas_weather_def

        elif awc_isOvercastWeather():
            return store.mas_weather_overcast

        elif awc_isRainWeather():
            return store.mas_weather_rain

        elif awc_isThunderWeather():
            return store.mas_weather_thunder

        elif awc_isSnowWeather():
            return store.mas_weather_snow

    def awc_isSunWeather():
        """
        Checks if current weather description or detailed description is in the sun keywords list

        OUT:
            True if weather is in sun keywords, False otherwise
        """
        weath_observaton = awc_getObservation().get_weather()

        weather_desc = weath_observaton.get_status().lower()
        detailed_weather_desc = weath_observaton.get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.SUN_KW
            or detailed_weather_desc in store.awc_globals.SUN_KW
        )

    def awc_isOvercastWeather():
        """
        Checks if current weather description or detailed description is in the overcast keywords list

        OUT:
            True if weather is in overcast keywords, False otherwise
        """
        weath_observaton = awc_getObservation().get_weather()

        weather_desc = weath_observaton.get_status().lower()
        detailed_weather_desc = weath_observaton.get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.OVERCAST_KW
            or detailed_weather_desc in store.awc_globals.OVERCAST_KW
        )

    def awc_isRainWeather():
        """
        Checks if current weather description or detailed description is in the rain keywords list

        OUT:
            True if weather is in sun keywords, False otherwise
        """
        weath_observaton = awc_getObservation().get_weather()

        weather_desc = weath_observaton.get_status().lower()
        detailed_weather_desc = weath_observaton.get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.RAIN_KW
            or detailed_weather_desc in store.awc_globals.RAIN_KW
        )

    def awc_isThunderWeather():
        """
        Checks if current weather description or detailed description is in the thunder keywords list

        OUT:
            True if weather is in thunder keywords, False otherwise
        """
        weath_observaton = awc_getObservation().get_weather()

        weather_desc = weath_observaton.get_status().lower()
        detailed_weather_desc = weath_observaton.get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.THUNDER_KW
            or detailed_weather_desc in store.awc_globals.THUNDER_KW
        )

    def awc_isSnowWeather():
        """
        Checks if current weather description or detailed description is in the snow keywords list

        OUT:
            True if weather is in snow keywords, False otherwise
        """
        weath_observaton = awc_getObservation().get_weather()

        weather_desc = weath_observaton.get_status().lower()
        detailed_weather_desc = weath_observaton.get_detailed_status().lower()


        return (
            weather_desc in store.awc_globals.SNOW_KW
            or detailed_weather_desc in store.awc_globals.SNOW_KW
        )
