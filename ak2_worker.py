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

# from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox

import os, sys
import time

# Selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.alert import Alert

from selenium.webdriver.firefox.options import Options # for headless option
from selenium.webdriver.common.keys import Keys

from config import *
import dynamic as dy



#
# Thread worker
# Setting tab ui update
class AutoKupis2_Tab1_UI_Update(QThread):

    def run(self):
        pass
    pass


class AutoKupis2_LoginTestHandler(QThread):

    _signal = pyqtSignal(dict)

    def run(self):
        
        # print('\tAutoKupis2_LoginTestHandler running...')

        if dy.VAR_USER_OK == False:
            self._signal.emit({'type': 'message_box', 'title': 'User information', 'body': 'User info unknown.'})
        
        elif dy.VAR_DRIVER_CHECK == False:
            self._signal.emit({'type': 'message_box', 'title': 'Driver status', 'body': 'Check the driver status.'})

        else:
            try:
                self._signal.emit({'type': 'status_bar', 'msg': 'Login test loading...'})

                driver = webdriver.Firefox(executable_path=FIREFOX_WEBDRIVER)
                driver.get(KUPIS_LOGIN_URL)

                driver.find_element_by_name('stdNo').send_keys(dy.VAR_USER_ID)
                driver.find_element_by_name('pwd').send_keys(dy.VAR_USER_PW)

                # executing script
                driver.execute_script('Login();')
                driver.execute_script('document.onkeydown = function() {};') # set an empty function

                # New tab
                body = driver.find_element_by_tag_name("body")
                body.send_keys(Keys.CONTROL + 't')

                self._signal.emit({'type': 'status_bar', 'msg': 'Login test done.'})

            except Exception as e:
                # self.statusBar().showMessage("Login test failed.")
                self._signal.emit({'type': 'message_box', \
                    'title': 'Test', 'body': 'Login test failed.'})
                pass

        # print('\tAutoKupis2_LoginTestHandler end')



class AutoKupis2_DriverCheckHandler(QThread):
    
    _signal = pyqtSignal(dict)

    #@pyqtSlot()
    def run(self):

        # Debug
        # print('\tAutoKupis2_DriverCheckHandler running...')
        
        # Check process just opens Firefox and closes it.
        # self._signal.emit({'type': 'message_box',\
        #          'title': 'Driver check', 'body': FIREFOX_WEBDRIVER})

        try:
            
            self._signal.emit({'type': 'status_bar', 'msg': 'Driver checking...'})
            self._signal.emit({'type': 'STAT__1', 'text': 'Browser status: checking...'})

            # Firefox headless option enable
            options = Options()
            options.headless = True

            driver = webdriver.Firefox(options=options, executable_path=FIREFOX_WEBDRIVER)
            driver.quit()

            # if ok
            dy.VAR_DRIVER_CHECK = True
            self._signal.emit({'type': 'message_box',\
                 'title': 'Driver check', 'body': 'Driver check finished.'})
            self._signal.emit({'type': 'status_bar', 'msg': 'Driver check done.'})
            

        except Exception as e:
            dy.VAR_DRIVER_CHECK = False
            # QMessageBox.warning(self, "Driver", "Driver error.")
            self._signal.emit({'type': 'message_box',\
                 'title': 'Driver check', 'body': e})

            # Display
        if dy.VAR_DRIVER_CHECK:
            #self.sig_numbers.emit("Browser status: Checked")
            self._signal.emit({'type': 'STAT_1', \
                'text': 'Browser status: Working'})
            
        else:
            self._signal.emit({'type': 'STAT_1', \
                'text': 'Browser status: Error'})
        #self.sig_numbers.emit("Driver check done.")

        # print('\tAutoKupis2_DriverCheckHandler end')



class AutoKupis2_RunRequestHandler(QThread):

    _signal = pyqtSignal(dict)

    def run(self):

        # Debug

        if dy.VAR_USER_OK == False:
            self._signal.emit({'type': 'message_box', 'title': 'User information', 'body': 'User info unknown.'})
            return

        elif dy.VAR_DRIVER_CHECK == False:
            self._signal.emit({'type': 'message_box', 'title': 'Driver status', 'body': 'Check the driver status.'})
            return

        try: # Loop up driver

            dy.VAR_CURRENT_DRIVER.set_page_load_timeout(dy.VAR_DELAY)

            while(1):
                for course in dy.VAR_COURSE:
                        
                    # dy.VAR_COURSE
                    query = "?strSaveCheck=Y&strSbjtId={code}&strKcuCount=0&CuriCdtWarnFg=3.0&MinCuriCnt=1&CuriCnt=1&CuriCdt=3.0&CuriMax=21&CuriAdd=0&PreSngj=4.11&Schdiv=1".format(code=course)

                    req_str = ''.join(KUPIS_SUGANG_REQ_URL)
                    req_str += query # This function send parameter by GET.

                    try:
                        dy.VAR_CURRENT_DRIVER.get(req_str)
                        # alert might raise exception, thus

                        self._signal.emit({'type': 'status_bar', 'msg': "Reqeust for [{}] sent.".format(course)})

                    except UnexpectedAlertPresentException as e: 
                        # self.statusBar().showMessage("UnexpectedAlertPresentException.")
                        continue
                    
                    except TimeoutException as e: 
                        # self.statusBar().showMessage("TimeoutException.")
                        continue
                    except Exception:
                        # self.statusBar().showMessage("Exception.")
                        self._signal.emit({'type': 'status_bar', 'msg': "Exception"})
                
        except Exception:
                QMessageBox.warning(self, "Driver status", "No browser handle.")
                # return


