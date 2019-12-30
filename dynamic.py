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

# This is the full parameter for logging in.
# stdNo, pwd is essential, the others are unknown.

VAR_USER_ID = ''
VAR_USER_PW = ''

VAR_DRIVER_CHECK = False
VAR_USER_OK = False

VAR_SETTINGS_OK = False

# Act
VAR_HEADLESS = False

VAR_DELAY = 0.3
VAR_CURRENT_DRIVER = None

VAR_USER = {
    'task' : 'f_CourUserLogin',
    'ltYy' : '2019',
    'ltShtm' : 'B01012',
    'campFg' : '1',
    'stdNo' : '',
    'pwd' : '',
    'idPassGubun' : '1'
}

VAR_COURSE = [] # Empty first.
