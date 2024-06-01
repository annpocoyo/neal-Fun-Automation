"""
Auto Infinite Craft Library - All the external code used to automate Infinite Craft.

Inside this library:

AutoInfiniteCraftClass - contains all functions used by autoinfinitecraft.py
"""
from _auto_browser_base import AutoBrowserBase # Base for automatic browser control
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement # For intelisense

class AutoInfiniteCraftClass(AutoBrowserBase):
    """This class contains all functions used by autoinfinitecraft.py"""
    def __init__(self):
        # Initalize Class
        # First we need to contact our parent's constructer
        super().__init__(url = "https://neal.fun/infinite-craft/")

        # Get neal.fun logo to be used as TARGET where items will be dragged and dropped
        self.crafting_target = self.driver.find_elements(By.CLASS_NAME, "site-title")[0]

        # Get clear button to use for clearing the crafting area
        self.clear_button = self.driver.find_elements(By.CLASS_NAME, "clear")[0]
    
    def craft(self, item1: WebElement, item2: WebElement):
        """Craft 2 items together"""
        # Clean up the crafting area to avoid conflicts
        self.clear_button.click()

        # Drag item 1 to crafting target
        super().drag_element_to_other_element(item1, self.crafting_target)

        # Drag item 2 to crafting target to combine them
        super().drag_element_to_other_element(item2, self.crafting_target)

    def _get_item_list(self):
        """Find and return a array of crafted item elements"""
        return self.driver.find_elements(By.CLASS_NAME, "items-inner")[0] \
            .find_elements(By.CLASS_NAME, "item")

    # Setup item list and make sure it auto updates every time it is requested
    item_list = property(_get_item_list)