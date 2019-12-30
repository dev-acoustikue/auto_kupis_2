# [Project AutoKupis2] Auto-sugang project GUI.
# 0.1.0va, 19.12.29. First launched.
# written by acoustikue(SukJoon Oh)
#                                 __  _ __            
#    ____ __________  __  _______/ /_(_) /____  _____ 
#   / __ `/ ___/ __ \/ / / / ___/ __/ / //_/ / / / _ \
#  / /_/ / /__/ /_/ / /_/ (__  ) /_/ / ,< / /_/ /  __/
#  \__,_/\___/\____/\__,_/____/\__/_/_/|_|\__,_/\___/ 
#                                                     
# Visual Studio Code
# 


import requests
import re

import os, sys

# for import from parent directory
sys.path.append( 
    os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))) )

from config import KUPIS_SERVER_URL


# added utility, 2019.08.19.
def kupisServerTime():

    date_from_header = requests.get(KUPIS_SERVER_URL).headers['Date'] 
    # If it is not in a special case, server always sends me the time in the header.
    # Refer to W3C docs.

    # What I need is a date, converted to Korean time, GMT +9.
    # or just use GMT 0.

    # for example, the output will be like, 
    # Sun, 18 Aug 2019 16:23:36 GMT  
    # regex will be like, /^(0[0-9]|1[0-9]|2[0-3])(:[0-5]\d)(:[0-5]\d)/

    exported_time = re.compile('\d\d:\d\d:\d\d').findall(date_from_header)[0]
    #exported_h = exported_time[0:2]
    #exported_m = exported_time[3:5]
    #exported_s = exported_time[6:]

    print('[console] Server time(GMT 0): ' + str(exported_time) + ' detected.')

    return exported_time


