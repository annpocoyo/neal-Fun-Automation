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
