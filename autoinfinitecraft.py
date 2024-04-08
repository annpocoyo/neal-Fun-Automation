"""
autoinfinitecraft.py - Automate crafting in Infinite Craft by Neal Agarwal at neal.fun
Author: Ryan, also known as annpocoyo
Credits:
Selenium - Browser automation library
"""

# Import Modules
import os # For custom modules
import sys # For custom modules
from selenium.webdriver.common.by import By # For browser control

# Add custom modules to path
sys.path.append(f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/Library")

# Load custom librarys
from autoInfiniteCraftLibrary import autoInfiniteCraftClass
autoInfiniteCraftGame = autoInfiniteCraftClass()

def main():
    print(autoInfiniteCraftGame.listOfItems)

# Good practise to make programs that are runned from the terminal use a main function.
main()
