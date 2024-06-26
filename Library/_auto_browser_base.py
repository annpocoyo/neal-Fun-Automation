"""
Auto Browser Base - All base code used to control the browser, you shouldn't need to import this direcly

Inside this library:

AutoBrowserBase - contains all functions used to control the browser
"""
import shutil # For finding if there is a geckodriver in path
import platform # To find out if we are on Mac or something else
from selenium import webdriver # For Browser Control
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service

class AutoBrowserBase:
    """This class contains all functions used to control the browser"""
    def __init__(self, gecko_driver_path = None, url: str = "https://google.com"):
        # Initalize Class
        # Has the creator of this object not passed a path to geckodriver?
        if gecko_driver_path == None:
            # No, we need to get one ourselves.
            # Is geckodriver in path?
            if shutil.which("geckodriver"):
                # Yes, get the path
                gecko_driver_path = shutil.which("geckodriver")
            else:
                # No, ask for the path
                gecko_driver_path = \
                    input("Please enter the full path to geckodriver:")\
                        .strip('\"') \
                        .strip("\'") # Strip out quotes from the path just incase

        # Setup service object for custom gecko driver path
        service = Service(executable_path = gecko_driver_path)

        # Load driver for website
        # Make sure custom geckoDriver is respected
        self.driver = webdriver.Firefox(service=service)

        # Load the website
        self.driver.get(url)

        # Are we on Mac or something else (This is to fix keybinds)?
        if platform.system() == "Darwin":
            # We are on Mac, for most keybinds macOS uses Command
            # instead of Ctrl so we will use that.
            self._action_key = Keys.COMMAND
        else:
            # We are on something else, assume the main key is Ctrl.
            self._action_key = Keys.CONTROL