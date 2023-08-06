from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    """A class for login page locators. All login page locators should be
    added here.
    """
    USER_NAME_LOCATOR = (By.NAME, 'UserName')
    PASSWORD_LOCATOR = (By.NAME, "Password")
    SUBMIT_LOCATOR = (By.ID, "submitButton")

    CONFIRMATION_LOCATOR = (By.ID, "ctl00_LVUserMenu_LWelcome")

    NO_FILE_FOUND = (By.ID,"PDoesNotExist")
