"""
Auto Infinite Craft Library - All the external code used to automate Infinite Craft.

Inside this library:

autoInfiniteCraftClass - contains all functions used by autoinfinitecraft.py
"""
from _autoBrowserBase import autoBrowserBase # Base for automatic browser control
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement # For intelisense

class autoInfiniteCraftClass(autoBrowserBase):
    """This class contains all functions used by autoinfinitecraft.py"""
    def __init__(self):
        # Initalize Class
        # First we need to contact our parent's constructer
        super().__init__(url = "https://neal.fun/infinite-craft/")

        # Find item list and get array of item elements
        self.itemList = self.driver.find_elements(By.CLASS_NAME, "items-inner")[0].find_elements(By.CLASS_NAME, "item")

        # Get neal.fun logo to be used as TARGET where items will be dragged and dropped
        self.craftingTarget = self.driver.find_elements(By.CLASS_NAME, "site-title")[0]

        # Get clear button to use for clearing the crafting area
        self.clearButton = self.driver.find_elements(By.CLASS_NAME, "clear")[0]
    
    def craft(self, item1: WebElement, item2: WebElement):
        """Craft 2 items together"""
        # Clean up the crafting area to avoid conflicts
        self.clearButton.click()

        # Drag item 1 to crafting target
        super().dragElementToOtherElement(item1, self.craftingTarget)

        # Drag item 2 to crafting target to combine them
        super().dragElementToOtherElement(item2, self.craftingTarget)
