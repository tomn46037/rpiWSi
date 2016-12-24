#==============================================================
#interface language. uncomment one of them. you can create you own language file and use it here
#from lang_ru import *
from lang_en import *

#weather underground api key NEED TO CHANGE
wu_api_key = 'XXXXXXXXXXXXXXXX'

#gps coordinates NEED TO CHANGE
wu_gps_coordinates = '20.93838,-24.3838182'
#weather underground api language. Must be exactly as declared in WeatherUnderground API
#wu_language = 'RU'
wu_language = 'EN'

#do not change!
wu_icon_set = 'k'

#choose you temperature units (C/F)
#temperature_inits="celsius"
temperature_inits="fahrenheit"

#enable demo data without internet connection
debug=False
#debug=True

#web server port
#After successfull setup you can get current screenshot from raspberry using browser:
#http://raspberry_ip:8080
web_server_port=8080

#screen resolution
screen_width,screen_height = 240,320
#if you want to change resolution you need to completely rewrite function 
#draw_data(screen,page,data,angle) in file ws_drawing.py
#==============================================================
