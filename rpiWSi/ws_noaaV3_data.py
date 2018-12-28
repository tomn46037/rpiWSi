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
            # First step - get the GridPoint from Lat/Long
            gridpoint_request = urllib2.urlopen("https://api.weather.gov/points/%s" % wu_gps_coordinates)
            gridpoint = json.loads(gridpoint_request.read())

            #pprint(gridpoint)

            forecast_url = gridpoint['properties']['forecast']
            forecast_request = urllib2.urlopen(forecast_url)
            forecast = json.loads(forecast_request.read())['properties']

            #print "Forecast URL: %s" % forecast_url

            # Then get the current observations data - this must come from a station.  (Airport.)
            nws_station_request = urllib2.urlopen("https://api.weather.gov/points/%s/stations" % wu_gps_coordinates)
            nws_station_url = json.loads(nws_station_request.read())['features'][0]['id']+'/observations/current'

            observations_request = urllib2.Request(nws_station_url, headers={ 'User-Agent': 'test Mozilla/5.0' })
            observations_string = urllib2.urlopen(observations_request).read()
            observations = json.loads(observations_string)['properties']

            #print("\n\n\n\n\n\nHere: %s" % observations_string)
            #pprint(observations)

        feels_like=-99
        try:
            feels_like = float(get_value(observations['windChill']['value']))
        except:
            pass
        try:
            feels_like = float(get_value(observations['heatIndex']['value']))
        except:
            pass

        if temperature_inits=="celsius":
            wu_data["temp_now"]=int(float(get_value(observations['temperature']['value'])))
            wu_data["temp_now_feels_like"]=int(feels_like)
        else:
            wu_data["temp_now"]=(float(get_value(observations['temperature']['value']))*(9/5))+32
            wu_data["temp_now_feels_like"]=(feels_like*(9/5))+32

        wu_data["wind_mph"]=unicode(int(get_value(observations['windSpeed']['value']))/1.609)
        wu_data["wind_kph"]=unicode(int(get_value(observations['windSpeed']['value'])))
        wu_data["icon_0"]=observations['icon']

        if temperature_inits=="celsius":
            wu_data["loacl_temp_out"]=float(get_value(observations['temperature']['value']))
        else:
            wu_data["local_temp_out"]=(float(get_value(observations['temperature']['value']))*(9/5))+32

        wu_data["local_hum_out"]=get_value(observations["relativeHumidity"]['value'])
        #wu_data["local_pressure"]=unicode(int(float(wu_parsed_json1['current_observation']["pressure_mb"])*750.06/1000.0))
        wu_data["local_pressure_pa"]=unicode("%2.1f"%(float(get_value(observations['barometricPressure']['value']))))
        wu_data["local_pressure"]=unicode("%2.1f"%(float(get_value(observations['barometricPressure']['value']))/3386.389))

        #if icons.has_key(wu_data["icon_0"]):wu_data["image_0"]=icons[wu_data["icon_0"]]
        #else:wu_data["image_0"]=icons[wu_data["na"]]

        if debug: wu_data["wind_kph"]=unicode(random.randint(7,15))
        #xxx=12/0


        wu_data["temp_fore_0_min"]=forecast['periods'][3]['temperature']
        wu_data["temp_fore_0_max"]=forecast['periods'][3]['temperature']
        wu_data["conditions_0"]=forecast['periods'][3]['shortForecast']

        wu_data["temp_fore_1_min"]=forecast['periods'][4]['temperature']
        wu_data["temp_fore_1_max"]=forecast['periods'][4]['temperature']
        wu_data["conditions_1"]=forecast['periods'][4]['shortForecast']

        wu_data["temp_fore_2_min"]=forecast['periods'][5]['temperature']
        wu_data["temp_fore_2_max"]=forecast['periods'][5]['temperature']
        wu_data["conditions_2"]=forecast['periods'][5]['shortForecast']

        wu_data["temp_fore_3_min"]=forecast['periods'][6]['temperature']
        wu_data["temp_fore_3_max"]=forecast['periods'][6]['temperature']
        wu_data["conditions_3"]=forecast['periods'][6]['shortForecast']

        wu_data['image_1']=forecast['periods'][3]['icon']
        wu_data['image_2']=forecast['periods'][4]['icon']
        wu_data['image_3']=forecast['periods'][5]['icon']

        #print wu_data

    except:
        print "\nUnexpected error:", sys.exc_info()[0]
        pprint(sys.exc_info())
        traceback.print_tb(sys.exc_info()[2])
        print "Giving up"
        return {}

    return wu_data

if __name__=="__main__":

    if os.uname()[0]=="Linux":
        rpiWSi.ws_start(90)
    else:
        rpiWSi.ws_start(0)
