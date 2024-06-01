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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement # For type definitions

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
        
        # Initalise action builder
        self.builder = ActionChains(self.driver)
    
    def drag_element_to_other_element(self, element: WebElement, target: WebElement):
        """Drag `element: WebElement` to `target: WebElement`"""
        # Setup click and drag action
        self.builder.click_and_hold(element) \
            .move_to_element(target) \
            .release(target) \
            .perform() # Start action
    
    def get_all_pairs_of_list(self, combination_list: list):
        """Get all possible Pairs of `list: list`"""
        # Setup list to return
        list_to_return: list[list] = []
        for x in combination_list:
            for y in combination_list:
                list_to_return.append([x,y]) # Add combination to returned list
        
        # Return list
        return list_to_return
