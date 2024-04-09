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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement # For intelisense

class autoInfiniteCraftClass:
    """This class contains all functions used by autoinfinitecraft.py"""
    def __init__(self):
        # Initalize Class
        # Load driver for infinite craft
        self.driver = webdriver.Firefox()
        self.driver.get("https://neal.fun/infinite-craft/")

        # Initalise action builder
        self.builder = ActionChains(self.driver)

        # Find item list and get array of item elements
        self.itemList = self.driver.find_elements(By.CLASS_NAME, "items-inner")[0].find_elements(By.CLASS_NAME, "item")
    
    def dragElementToOtherElement(self, element: WebElement, target: WebElement):
        """Drag `element: WebElement` to `target: WebElement`"""
        # Setup click and drag action
        self.builder.click_and_hold(element) \
            .move_to_element(target) \
            .release(target) \
            .perform() # Start action
