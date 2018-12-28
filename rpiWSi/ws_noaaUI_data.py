#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ws_globals
from ws_globals import *
import sys
import gc
import random
import string
import urllib2
import json
# TNev
#import rpiWSi
from pprint import pprint
import traceback


from globals import *

icons={
"chanceflurries":("12.png"),
"chancerain":("9.png"),
"chancesleet":("8.png"),
"chancesnow":("35.png"),
"chancetstorms":("1.png"),
"clear":("32c.png"),
"cloudy":("26.png"),
"flurries":("12.png"),
"fog":("19.png"),
"hazy":("19.png"),
"mostlycloudy":("28.png"),
"mostlysunny":("34.png"),
"partlycloudy":("30.png"),
"partlysunny":("28.png"),
"rain":("9.png"),
"sleet":("8.png","17.png"),
"snow":("35.png"),
"sunny":("36c.png"),
"tstorms":("1.png"),

"nt_chanceflurries":("12.png"),
"nt_chancerain":("9.png"),
"nt_chancesleet":("8.png"),
"nt_chancesnow":("35.png"),
"nt_chancetstorms":("1.png"),
"nt_clear":("31c.png"),
"nt_cloudy":("26.png"),
"nt_flurries":("12.png"),
"nt_fog":("22.png"),
"nt_hazy":("22.png"),
"nt_mostlycloudy":("27.png"),
"nt_mostlysunny":("33.png"),
"nt_partlycloudy":("29.png"),
"nt_partlysunny":("27.png"),
"nt_rain":("9.png"),
"nt_sleet":("8.png","17.png"),
"nt_snow":("35.png"),
"nt_sunny":("31c.png"),
"nt_tstorms":("47.png"),
"na":("na.png")
}

def get_value(value):
    if value is None:
        return -99
    else:
        return value

def get_wu_data(wu_api_key,wu_gps_coordinates,wu_language='EN',wu_icon_set='k'):
    w,wu_data={},{}
    try:
        if debug:
            wu_json_string1=''
            wu_json_string2=''
            wu_parsed_json1={u''}
            wu_parsed_json2={u''}

        else:
            # Re-write to use the stupid UI - https://forecast.weather.gov/MapClick.php?&lat=40.06690578175116&lon=-85.90853691101074&FcstType=json
            data_request = urllib2.urlopen("https://forecast.weather.gov/MapClick.php?&lat=%s&lon=%s&FcstType=json" % tuple(wu_gps_coordinates.split(',')))
            data = json.loads(data_request.read())

            observations = data['currentobservation']

            forecast_time = data['time']['startPeriodName']
            forecast_data = data['data']

        # This is not displayed.. so no need to find it.
        feels_like=-99


        if temperature_inits=="celsius":
            wu_data["temp_now"]=(float(get_value(observations['Temp']))-32)*(float(5)/float(9))
            wu_data["temp_now_feels_like"]=int(feels_like)-32*(5/9)
        else:
            wu_data["temp_now"]=(float(get_value(observations['Temp'])))
            wu_data["temp_now_feels_like"]=feels_like

        wu_data["wind_mph"]=unicode(int(get_value(observations['Winds'])))
        wu_data["wind_kph"]=unicode(int(get_value(observations['Winds']))*1.609)
        wu_data["image_0"]="https://forecast.weather.gov/newimages/large/%s" % observations['Weatherimage']

        if temperature_inits=="celsius":
            wu_data["local_temp_out"]=(float(get_value(observations['Temp']))-32)*(float(5)/float(9))
        else:
            wu_data["local_temp_out"]=(float(get_value(observations['Temp'])))

        wu_data["local_hum_out"]=get_value(observations["Relh"])
        #wu_data["local_pressure"]=unicode(int(float(wu_parsed_json1['current_observation']["pressure_mb"])*750.06/1000.0))
        #wu_data["local_pressure_pa"]=unicode("%2.1f"%(float(get_value(observations['barometricPressure']['value']))))
        wu_data["local_pressure"]=unicode("%2.1f"%(float(get_value(observations['SLP']))))


        wu_data["time_0"]=forecast_time[0]
        wu_data["temp_fore_0_min"]=forecast_data['temperature'][0]
        wu_data["temp_fore_0_max"]=forecast_data['temperature'][1]
        wu_data["conditions_0"]=observations['Weather']

        wu_data["time_1"]=forecast_time[1]
        wu_data["temp_fore_1_min"]=forecast_data['temperature'][2]
        wu_data["temp_fore_1_max"]=forecast_data['temperature'][3]
        wu_data["conditions_1"]=forecast_data['weather'][1]

        wu_data["time_2"]=forecast_time[2]
        wu_data["temp_fore_2_min"]=forecast_data['temperature'][4]
        wu_data["temp_fore_2_max"]=forecast_data['temperature'][5]
        wu_data["conditions_2"]=forecast_data['weather'][2]

        wu_data["time_3"]=forecast_time[3]
        wu_data["temp_fore_3_min"]=forecast_data['temperature'][6]
        wu_data["temp_fore_3_max"]=forecast_data['temperature'][7]
        wu_data["conditions_3"]=forecast_data['weather'][3]

        wu_data['image_1']=forecast_data['iconLink'][1]
        wu_data['image_2']=forecast_data['iconLink'][2]
        wu_data['image_3']=forecast_data['iconLink'][3]

    except:
        print("\n\n")
        pprint(wu_data)
        print("\n\n")
        print "\nUnexpected error:", sys.exc_info()[0]
        pprint(sys.exc_info())
        traceback.print_tb(sys.exc_info()[2])
        print "Giving up"
        return {}

    # Now go out and download the latest RADAR image to the cache.
    # https://radar.weather.gov/lite/N0R/%s_0.png
    radar_url = "https://radar.weather.gov/lite/N0R/%s_0.png" % data['location']['wfo']

    global app_dir
    file_name = os.path.realpath("{1}/cache/{0}".format('radar.png',app_dir))

    if not os.path.isfile(file_name):

        data_request = urllib2.urlopen(radar_url)
        image_data = data_request.read()

        with open(file_name, 'w') as OUTPUT:
            OUTPUT.write(image_data)
            OUTPUT.close()

    return wu_data

if __name__=="__main__":

    if os.uname()[0]=="Linux":
        rpiWSi.ws_start(90)
    else:
        rpiWSi.ws_start(0)
