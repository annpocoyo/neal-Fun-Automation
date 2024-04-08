"""
Auto Infinite Craft Library - All the external code used to automate Infinite Craft.

Inside this library:

autoInfiniteCraftClass - contains all functions used by autoinfinitecraft.py
"""
import os # For loading JSON
import sys #  ^
import json # |
from selenium import webdriver # For Browser Control
from selenium.webdriver.common.by import By

class autoInfiniteCraftClass:
    """This class contains all functions used by autoinfinitecraft.py"""
    def __init__(self):
        # Initalize Class
        # Load driver for infinite craft
        self.driver = webdriver.Firefox()
        self.driver.get("https://neal.fun/infinite-craft/")

        # Find item list and get array of item elements
        self._itemList = self.driver.find_elements(By.CLASS_NAME, "items-inner")[0].find_elements(By.CLASS_NAME, "item")

    def _getListOfItems(self):
        """Get parseable list of currently known items"""
        # Temp list used to store list of items:
        listToReturn: list = []

        # Loop through all items in item list.
        for item in self._itemList:
            # Add name of item to the list we are returning and the web element
            listToReturn.append([item.text, item])
        
        # Return list
        return listToReturn

    # Setup properties
    listOfItems = property(_getListOfItems) # Parseable list of items.