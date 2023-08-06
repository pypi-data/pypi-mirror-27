import os
from time import sleep
from selenium import webdriver
from compliance_assist.locators import LoginPageLocators

# Import credentials, if available
try:
    from sensitive import USER_NAME, PASSWORD
except:
    # If sensisitve.py is not available
    USER_NAME = ""
    PASSWORD = ""


class Site(object):
    
    def __init__(self,download_destination="/Users/mattlewis/Development/python/ComplianceAssist/compliance_assist/data/tmp"):

        options = webdriver.ChromeOptions()
        profile = {"plugins.plugins_list": 
                [
                    {"enabled":False,"name":"Chrome PDF Viewer"}
                ],
                "download.default_directory" : download_destination}
        options.add_experimental_option("prefs",profile)
        self.DOWNLOAD_DEST = download_destination
        self.driver = webdriver.Chrome(options = options)
        self.driver.get("https://sanjac.compliance-assist.com/")
        self._login()
    
    def get_cookies(self):
        return self.driver.get_cookies()

    def _login(self):
        """
        Login to the Compliance Assist site using credentials imported from
        sensitive module (which is .gitignored).
        """
        # Fetch login fields and submit button
        username_field = self.driver.find_element(
            *LoginPageLocators.USER_NAME_LOCATOR)
        password_field = self.driver.find_element(
            *LoginPageLocators.PASSWORD_LOCATOR)
        submit_button = self.driver.find_element(
            *LoginPageLocators.SUBMIT_LOCATOR)
        # Send username and password to fields
        username_field.send_keys(USER_NAME)
        password_field.send_keys(PASSWORD)
        # Click
        submit_button.click()

    def goto(self,url):
        """
        Navigate to url.
        
        Note: this can be used to download files.
        """
        self.driver.get(url)

    def download(self, url):
        """
        Method to download files at supplied `url` from Compliance Assist and
        save file in local `destination`. 
        
        Note: this method utilizes chromes automatic downloading for files. 
        If the url points to a page chrome wants to load, it will load it.
        """
        download_error_indicator = None
        before = os.listdir(self.DOWNLOAD_DEST)
        self.goto(url)
        after = os.listdir(self.DOWNLOAD_DEST)
        change = set(after) - set(before)
        try:
            file_name = change.pop()
        except:
            raise ChangelessDirectoryError

        # Detects that file could not be found and throws a FileNotFoundError
        try:
            download_error_indicator = self.driver.find_element(*LoginPageLocators.NO_FILE_FOUND)
        except:
            pass
        if(download_error_indicator):
            raise FileNotFoundError
        
        while(('crdownload' in file_name) or ('.com' in file_name)):
                sleep(.5)
                before = after
                after = os.listdir(self.DOWNLOAD_DEST)
                change = set(after) - set(before)
                if(change):
                    file_name = change.pop()
                print(file_name)
        return file_name


    def _find_element(self,LOCATOR):
        """
        Exposes driver for the purpose of locating elements on site.
        """
        return self.driver.find_element(*LOCATOR)

    def close(self):
        self.driver.close()


class FileNotFound(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class ChangelessDirectoryError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)