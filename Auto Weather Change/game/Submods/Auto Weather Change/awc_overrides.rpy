init 1 python:

    def mas_shouldRain():
        """
        Tries to get weather from API. If not possible, then we use normal rand Chances

        OUT:
            weather to use, or None if we dont want to change weather
        """

        # If the key and the location are valid we use the weather from the api
        if (
            mas_isMoniNormal(higher=True)
            and (store.awc_canGetAPIWeath() and awc_testConnection())
            and store.persistent._awc_enabled
        ):
            return store.awc_weathFromAPI()

        else:
            #All paths roll
            chance = random.randint(1,100)
            if mas_isMoniNormal(higher=True):
                #NOTE: Chances are as follows:
                #Spring:
                #   - Rain: 40%
                #   - Thunder: 15% (37.5% of that 40%)
                #   - Overcast: 15% (if rain has failed)
                #   - Sunny: 45%
                #
                #Summer:
                #   - Rain: 10%
                #   - Thunder: 6% (60% of that 10%)
                #   - Overcast: 5% (if rain has failed)
                #   - Sunny: 85%
                #
                #Fall:
                #   - Rain: 30%
                #   - Thunder: 12% (40% of that 50%)
                #   - Overcast: 15%
                #   - Sunny: 55%
                #
                #Winter:
                #   - Snow: 50%
                #   - Overcast: 20%
                #   - Sunny: 30%
                if mas_isSpring():
                    return mas_weather._determineCloudyWeather(
                        40,
                        15,
                        15,
                        rolled_chance=chance
                    )

                elif mas_isSummer():
                    return mas_weather._determineCloudyWeather(
                        10,
                        6,
                        5,
                        rolled_chance=chance
                    )

                elif mas_isFall():
                    return mas_weather._determineCloudyWeather(
                        30,
                        12,
                        15,
                        rolled_chance=chance
                    )

                else:
                    #Chance of snow
                    if chance <= 50:
                        return mas_weather_snow
                    elif chance <= 70:
                        return mas_weather_overcast

            #Otherwise rain based on how Moni's feeling
            elif mas_isMoniUpset() and chance <= MAS_RAIN_UPSET:
                return mas_weather_overcast
            elif mas_isMoniDis() and chance <= MAS_RAIN_DIS:
                return mas_weather_rain
            elif mas_isMoniBroken() and chance <= MAS_RAIN_BROKEN:
                return mas_weather_thunder
        return None


init -19 python in mas_weather:
    import random
    import datetime
    import store

    def weatherProgress():
        """
        Runs a roll on mas_shouldRain() to pick a new weather to change to after a time between half an hour - one and a half hour

        RETURNS:
            - True or false on whether or not to call spaceroom
        """
        #First, see if we have a value to get
        ret_val = store.await_weatherProgress.get()

        #If ret val is none, then we're either not running, or not done
        #In the latter case, a new thread won't start until this finishes
        if ret_val is None:
            store.await_weatherProgress.start()

        #We have a value, let's return it
        else:
            return ret_val
