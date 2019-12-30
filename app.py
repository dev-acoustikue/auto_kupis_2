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


# PyQt
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic

from PyQt5.QtWidgets import QMessageBox

import os, sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.alert import Alert

from selenium.webdriver.firefox.options import Options # for headless option
from selenium.webdriver.common.keys import Keys

import threading

# for import from parent directory
sys.path.append( 
    os.path.dirname(
        os.path.abspath(os.path.dirname(__file__))) )

from config import *
import dynamic as dy

# UI file
AutoKupis2GUI_MainWndFile = QT_UI_MAIN


# File link
AutoKupis2GUI_MainWnd, QtBaseClass = uic.loadUiType(AutoKupis2GUI_MainWndFile)

class AutoKupis2GUI_LOGIN(QMainWindow, AutoKupis2GUI_MainWnd):
    
    def __init__(self):
        
        QMainWindow.__init__(self)
        
        self.setWindowIcon(QtGui.QIcon(QT_UI_ICON))

        self.setupUi(self)
        self.show()


        # First show user status
        self.statusBar().showMessage("No ID and password has been set.")
        

        # First tab
        # self.pushButton.clicked.connect(self.buttonWindow1_onClick)
        # self.ID_EDIT.returnPressed.connect(self.setID)
        self.LOGIN_TEST.clicked.connect(self.loginTest)

        self.SET_USER.clicked.connect(self.setUser)
        self.ID_EDIT.returnPressed.connect(self.setUser)
        self.PW_EDIT.returnPressed.connect(self.setUser)
        self.RESET_USER.clicked.connect(self.resetUser)

        self.DRIVER_CHECK.clicked.connect(self.driverCheck)

        # Second tab
        self.ADD_LIST.clicked.connect(self.addList)
        self.ADD_LIST_BOX.returnPressed.connect(self.addList)

        self.DELETE_LIST.clicked.connect(self.deleteList)
        self.RESET_LIST.clicked.connect(self.resetList)

        self.DELAY_BOX.valueChanged.connect(self.delaySet)

        # run
        self.RUN.clicked.connect(self.runRequest)

        self.HEADLESS_CHECK.clicked.connect(self.toggleHeadlessMode)

        self.OPEN_AND_WAIT.clicked.connect(self.openAndWait)
        self.QUIT.clicked.connect(self.quitBrowser)

    # Button Actions
    def setUser(self):

        dy.VAR_USER_ID = self.ID_EDIT.text()
        dy.VAR_USER_PW = self.PW_EDIT.text()

        if dy.VAR_USER_PW == '' or dy.VAR_USER_ID == '':
            
            # Alert
            QMessageBox.warning(self, "User information", "User information cannot be blank.")

            self.statusBar().showMessage("User information cannot be blank.")
            
            # Reset
            dy.VAR_USER_ID = dy.VAR_USER_PW = ''

            dy.VAR_USER_OK = False
        
        else:
            self.ID_EDIT.setText('')
            self.PW_EDIT.setText('')

            self.statusBar().showMessage("Login info set to ID({id}), PW({pw})".format(id=dy.VAR_USER_ID, pw=('*' * len(dy.VAR_USER_PW))))
            self.STAT_2.setText("User info: ID({id}), PW({pw})".format(id=dy.VAR_USER_ID, pw=('*' * len(dy.VAR_USER_PW))))

            dy.VAR_USER_OK = True
        


    def resetUser(self):
        
        # Reset
        dy.VAR_USER_ID = ''
        dy.VAR_USER_PW = ''

        dy.VAR_USER_OK = False

        # Display
        self.STAT_2.setText("User info: Unknown")
        self.statusBar().showMessage("User information has been successfully reset.")

        self.ID_EDIT.setText('')
        self.PW_EDIT.setText('')




    # Driver check
    def driverCheck(self):
        
        self.statusBar().showMessage("Driver checking...")

        def driverCheckThreadHandler():

            # Check process just opens Firefox and closes it.
            try:
                self.STAT_1.setText("Browser status: Checking...")

                # Firefox headless option enable
                options = Options()
                options.headless = True

                driver = webdriver.Firefox(options=options, executable_path=FIREFOX_WEBDRIVER)
                driver.quit()

                # if ok
                dy.VAR_DRIVER_CHECK = True
                
            except Exception as e:
                dy.VAR_DRIVER_CHECK = False

            except WebDriverException as e:

                dy.VAR_DRIVER_CHECK = False
                self.STAT_1.setText("Browser status: WebDriverException")

            # Display
            if dy.VAR_DRIVER_CHECK:
                self.STAT_1.setText("Browser status: Checked")
            
            else:
                self.STAT_1.setText("Browser status: Error")

            self.statusBar().showMessage("Driver check done.")

        # Make it daemon
        driver_test_thread = threading.Thread(target=driverCheckThreadHandler)
        driver_test_thread.daemon = True 
        driver_test_thread.start()




    def loginTest(self):
        
        if dy.VAR_USER_OK == False:
            self.statusBar().showMessage("User info unknown.")
            QMessageBox.warning(self, "User information", "User info unknown.")
        
        elif dy.VAR_DRIVER_CHECK == False:
            self.statusBar().showMessage("Check the driver status.")
            QMessageBox.warning(self, "Driver status", "Check the driver status.")

        else:
            try:

                def loginTestThreadHandler():

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

                # Make it daemon
                login_test_thread = threading.Thread(target=loginTestThreadHandler)
                login_test_thread.daemon = True 
                login_test_thread.start()

            except Exception as e:
                self.statusBar().showMessage("Login test failed.")

    #
    # Second tab
    def addList(self):

        lecture_code = self.ADD_LIST_BOX.text()

        if lecture_code.isdigit() == False:
            self.ADD_LIST_BOX.setText('')
            self.statusBar().showMessage("Only number can be added.")

        else:
            if len(lecture_code) is not 4:
                self.ADD_LIST_BOX.setText('')
                self.statusBar().showMessage("Lecture code is 4 digit number.")
                
            else:            
                # Add to dynamics
                dy.VAR_COURSE.append(lecture_code)
                self.TARGET_LIST.addItem(lecture_code)
                
                # Clear the box
                self.ADD_LIST_BOX.setText('')

                self.statusBar().showMessage("Added to the list.")

    def deleteList(self):

        try: 
            sel = self.TARGET_LIST.currentItem().text()
            sel_row = self.TARGET_LIST.currentRow()
            dy.VAR_COURSE.remove(sel) # Delete from the list

            self.TARGET_LIST.takeItem(sel_row)

            self.statusBar().showMessage("Selected item deleted.")

        except:
            self.statusBar().showMessage("Error.")


    def resetList(self):

        dy.VAR_COURSE = []

        # display
        self.TARGET_LIST.clear()
        self.statusBar().showMessage("List cleared.")

    # Act
    def toggleHeadlessMode(self):
        if self.HEADLESS_CHECK.isChecked(): 
            dy.VAR_HEADLESS = True
            self.statusBar().showMessage("Headless mode enabled.")

        else: 
            dy.VAR_HEADLESS = False
            self.statusBar().showMessage("Headless mode disabled.")

    def openAndWait(self):

        if dy.VAR_USER_OK == False:
            self.statusBar().showMessage("User info unknown.")
            QMessageBox.warning(self, "User information", "User info unknown.")
        
        elif dy.VAR_DRIVER_CHECK == False:
            self.statusBar().showMessage("Check the driver status.")
            QMessageBox.warning(self, "Driver status", "Check the driver status.")

        else:
            try:
                options = Options()
                options.headless = dy.VAR_HEADLESS

                dy.VAR_CURRENT_DRIVER = webdriver.Firefox(options=options, executable_path=FIREFOX_WEBDRIVER)
                dy.VAR_CURRENT_DRIVER.get(KUPIS_LOGIN_URL)

                dy.VAR_CURRENT_DRIVER.find_element_by_name('stdNo').send_keys(dy.VAR_USER_ID)
                dy.VAR_CURRENT_DRIVER.find_element_by_name('pwd').send_keys(dy.VAR_USER_PW)

                # executing script
                dy.VAR_CURRENT_DRIVER.execute_script('Login();')
                dy.VAR_CURRENT_DRIVER.execute_script('document.onkeydown = function() {};') # set an empty function

                # New tab
                # body = dy.VAR_CURRENT_DRIVER.find_element_by_tag_name("body")
                # body.send_keys(Keys.CONTROL + 't')
                dy.VAR_CURRENT_DRIVER.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')

                if dy.VAR_HEADLESS:
                    print('\tBrowser opened as headless')
                    print('\tWaiting...')

                

            except Exception as e:
                self.statusBar().showMessage("Browser open failed.")
    

    def quitBrowser(self):
        
        # Close browser
        try: dy.VAR_CURRENT_DRIVER.quit()
        except: self.statusBar().showMessage("Browser close failed.")
        finally:
            dy.VAR_CURRENT_DRIVER = None


    # self.DELAY_BOX.valueChanged.connect(self.delaySet)
    def delaySet(self):
        # b_hdle.set_page_load_timeout(0.25)
        dy.VAR_DELAY = self.DELAY_BOX.value()
        
        try:
            dy.VAR_CURRENT_DRIVER.set_page_load_timeout(dy.VAR_DELAY)
            self.statusBar().showMessage("Delay set to {0}".format(dy.VAR_DELAY))

        except:
            self.statusBar().showMessage("No browser handle loaded.")


    # Main opertion
    def runRequest(self):

        def runRequestThreadHandler():

            if dy.VAR_USER_OK == False:
                self.statusBar().showMessage("User info unknown.")
                QMessageBox.warning(self, "User information", "User info unknown.")
                return
            
            elif dy.VAR_DRIVER_CHECK == False:
                self.statusBar().showMessage("Check the driver status.")
                QMessageBox.warning(self, "Driver status", "Check the driver status.")
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
                            self.statusBar().showMessage("Reqeust for [{}] sent.".format(course))
                        
                        except UnexpectedAlertPresentException as e: 
                            self.statusBar().showMessage("UnexpectedAlertPresentException.")
                            continue
                    
                        except TimeoutException as e: 
                            self.statusBar().showMessage("TimeoutException.")
                            continue
                        except Exception:
                            self.statusBar().showMessage("Exception.")
                
            except Exception:
                QMessageBox.warning(self, "Driver status", "No browser handle.")
                # return

            

        # Make it daemon
        run_thread = threading.Thread(target=runRequestThreadHandler)
        run_thread.daemon = True 
        run_thread.start()

















# Test & Debug
if __name__ == "__main__":

    print(PROJECT_BANNER)
     
    app = QApplication(sys.argv)
    xwin = AutoKupis2GUI_LOGIN()
    app.exec()