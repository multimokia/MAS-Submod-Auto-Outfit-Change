init -10 python:
    if store.awc_canGetAPIWeath() and awc_testConnection():
        store.persistent._mas_sunrise = awc_dtToMASTime(awc_getSunriseDT())
        store.persistent._mas_sunset = awc_dtToMASTime(awc_getSunsetDT())