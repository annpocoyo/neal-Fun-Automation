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
from auto_infinite_craft_library import AutoInfiniteCraftClass
auto_infinite_craft = AutoInfiniteCraftClass()

def main():
    auto_infinite_craft.craft(auto_infinite_craft.item_list[0],
        auto_infinite_craft.item_list[1])

    while True:
        pass

if __name__ == '__main__':
    main()
