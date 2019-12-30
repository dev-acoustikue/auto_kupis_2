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


import os, sys
import platform
# import copy

# for import from parent directory
sys.path.append( 
    os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))) )


# Here the module's base directory will be set to folder where it is located.
# Every config files and other saved files must be in folder below the base directory.

PROJECT_CODE = 'auto_kupis_2'
PROJECT_OS = 'Windows'
PROJECT_SYS = ''
PROJECT_VERSION = '0.1.0va'

CURRENT_CODE = 'auto_kupis_2_w'
CURRENT_OS = str(platform.system())
CURRENT_SYS = CURRENT_OS + ' ' + str(platform.release()) + ' ' + str(platform.version())


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEBDRIVER_DIR = ''
# WEBDRIVER_DIR_R 
LOG_DIR = ''

WEBDRIVER_DIR = BASE_DIR + '\\webdriver\\'
LOG_DIR = BASE_DIR + '\\log\\'

FIREFOX_WEBDRIVER = WEBDRIVER_DIR + 'geckodriver.exe'



# First!!
# Make directory if there is no db folder
if not(os.path.isdir(LOG_DIR)): os.makedirs(os.path.join(LOG_DIR))

PROJECT_BANNER = '[auto_kupis_2] ' + PROJECT_CODE + ', ' + PROJECT_VERSION
PROJECT_BANNER += (', ' + CURRENT_SYS + '\n\tCopyright (C) 2019 SukJoon Oh')



# Scripts
# platform

# Make sure to print just necessary information, for simple logs.

# URL info
KUPIS_SERVER_URL = 'https://kupis.konkuk.ac.kr/sugang/'

# Sugang login page, first step
KUPIS_LOGIN_URL = 'https://kupis.konkuk.ac.kr/sugang/login/loginTop.jsp'

# Controller
KUPIS_LOGIN_REQ_URL = 'https://kupis.konkuk.ac.kr/sugang/login/loginBtm.jsp'

# without iframe
KUPIS_SUGANG_URL = 'https://kupis.konkuk.ac.kr/sugang/acd/cour/aply/courLessinApplyReg.jsp'
KUPIS_SUGANG_REQ_URL = KUPIS_SUGANG_URL



# PyQt Configuration
# 

QT_UI_DIR = BASE_DIR + '\\ui\\'
QT_UI_MAIN = QT_UI_DIR + 'auto_kupis_main.ui'
QT_UI_LIST = QT_UI_DIR + 'auto_kupis_list.ui'
QT_UI_ICON = QT_UI_DIR + 'auto_kupis_2.ico'


# 
# Parameter: -
# Returns: -
# Author: acoustikue
def showConfig():

    #if KENS_ENABLE is True:
    #    print('\tKENS_ENABLE(1). KENS module will be loaded.')

    print('Script config:')

    print('\tPROJECT_CODE    \t' + PROJECT_CODE)
    print('\tPROJECT_OS      \t' + PROJECT_OS)
    print('\tPROJECT_SYS     \t' + PROJECT_SYS)
    print('\tPROJECT_VERSION \t' + PROJECT_VERSION)

    print('\tCURRENT_CODE    \t' + CURRENT_CODE)
    print('\tCURRENT_OS      \t' + CURRENT_OS)
    print('\tCURRENT_SYS     \t' + CURRENT_SYS)

    print('\tBASE_DIR        \t' + BASE_DIR)





# Executing this script?
if __name__ == '__main__':

    # First print banner
    print(PROJECT_BANNER)
    print('\tExecuting KnsfConfig script. Running in debug mode.\n')

    # Show configuration variables
    showConfig()



