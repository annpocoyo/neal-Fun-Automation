"""
Auto Password Library - All the external code used to automate the password game.

Inside this library:

autoPasswordClass - contains all functions used by autopasswordgame.py
"""
import os # For loading JSON
import sys #  ^
import json # |
import string # Cleaner way of getting the alphabet
import threading # For feeding Paul in the background
from selenium import webdriver # For Browser Control
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class autoPasswordClass:
    """This class contains all functions used by autopasswordgame.py"""
    # Initalize Variables
    # Contents of password
    passwordContents: str = ""

    # Vowels
    vowels: list[str] = ["a", "e", "i", "o", "u", "y"]

    # Roman Numerals
    romanNumerals: list[str] = ["I", "V", "X", "L", "C", "D", "M"]
    
    # Digits used to add to 25
    digitsThatAddTo25: str = "992"

    # Elements with atomic numbers that add up to 200
    elementsThatAddTo200: list[str] = ["Fm"]

    # Is Paul in our password?
    paulInOurPassword: bool = False

    # Has paul hatched?
    paulHatched: bool = False

    # Font size state storage
    currentFontSize: list[int] = []

    # Internal variable, is password being modified
    _isPasswordBeingModified: bool = False

    # Internal Variable, is first time bolding?
    _isFirstTimeBolding: bool = True

    # Internal Variable, is ENDGAME?
    _isEndgame: bool = False

    def __init__(self):
        # Initalize Class
        # Load driver for password game
        self.driver = webdriver.Firefox()
        self.driver.get("https://neal.fun/password-game/")

        # Find password box
        self.password_box = self.driver.find_elements(By.CLASS_NAME, "ProseMirror")[0]

        # Find password length counter
        self.password_length_counter = self.driver.find_elements(By.CLASS_NAME, "password-length")[0]

        # Load JSON file for the ENTIRE FRICKING PERIODIC TABLE
        elementsFile = open(f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/Library/passwordGame/elements.json")
        self.elements = json.load(elementsFile)

        # Overwrite Window.Date to fix impossible question
        self.driver.execute_script("""
            oldDate = window.Date;

            window.Date = function () {
                // Apply the original constructor on this object
                oldDate.apply(this, arguments);

                this.now = function () {
                  return "00:00";
                };

                this.toLocaleString = function (locale, x) {
                  return "00:00 PM";
                };
            }
            
            window.Date.prototype = oldDate
            
            window.Date.now = function () {
                return "10:00";
            };
        """)

        # Close json file
        elementsFile.close()

    def updateBox(self):
        """Refresh the Password Box"""
        self._isPasswordBeingModified = True # Tell everything password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver.execute_script("arguments[0].style='white-space: nowrap !important'", self.password_box)

        # Refresh password box
        self.password_box.send_keys(Keys.COMMAND + "a")
        # If Paul exists:
        if self.paulInOurPassword:
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_LEFT) # WE MUST PROTECT PAUL, PAUL IS EVERYTHING, PAUL IS LIFE
        # Protect the worms food
        if self.paulHatched:
            # Run as many times as there are worms in the password
            for i in range(self.password_box.text.count("🐛")):
                self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_LEFT) # Protect each worm
        self.password_box.send_keys(Keys.BACKSPACE)
        self.password_box.send_keys(str(self.digitsThatAddTo25) + "".join(self.elementsThatAddTo200) + self.passwordContents)
        
        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        # Wait for password box to update
        while self.password_box.text.replace("🥚", "").replace("🐔", "").replace("🐛", "") != str(self.digitsThatAddTo25) + "".join(self.elementsThatAddTo200) + self.passwordContents:
            continue # Wait

        self._isPasswordBeingModified = False # Tell everything we finished

    def findDigitsThatAddUpTo(self, number: int):
        """Find 3 digits that add up to `number: int`"""
        # Loop through all combinations of digits
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    # Do they add up to the number
                    if (i + j + k == number):
                        # Yes, return digits
                        return str(i) + str(j) + str(k)

    def fixNumberConflicts(self):
        """Fix any number conflicts"""
        # Initialize local variables
        numberToSubtractFrom25 = 0
        digitsAddedByOtherStuff = []

        # Get all digits added by other things and add them together
        digitsAddedByOtherStuff = [int(i) for i in self.passwordContents if i.isdigit()]
        numberToSubtractFrom25 = sum(digitsAddedByOtherStuff)

        # Find digits to replace previous ones to fix number conflicts.
        self.digitsThatAddTo25 = self.findDigitsThatAddUpTo(25 - numberToSubtractFrom25)
        self.updateBox()

    def findElementsThatAddUpTo(self, number: int):
        """Find elements that add up to `number: int`"""
        # Initalise Variables
        elements: list[str] = []

        # Do we only need one element?
        if number <= 118:
            # Append element
            elements.append(self.elements[number - 1]["safeSymbol"])
        else:
            # No: add base 199 numbered element and continue with the remainder
            elements.append(self.elements[117]["safeSymbol"])
            elements.append(self.elements[number - 119]["safeSymbol"])
        
        # Return elements
        return elements

    def fixElementConflicts(self):
        """Fix any element conflicts"""
        # Initialize local variables
        numberToSubtractFrom200 = 0
        elementsAddedByOtherStuff = []

        # Get all elements added by other things
        for i in self.elements:
            for j in range(len(self.passwordContents)):
                x = self.passwordContents[j]

                # Check if single character element symbol exists in string
                if (x == i["symbol"]) and ((len(self.passwordContents) - 1 == j) or (not any(ext["symbol"] == x + self.passwordContents[j + 1] for ext in self.elements))):
                    # Yes: add it in
                    elementsAddedByOtherStuff.append(i)
                # Check if double character element symbol exists in string
                elif (len(self.passwordContents) - 1 != j) and (x + self.passwordContents[j + 1] == i["symbol"]):
                    # Yes: add it in
                    elementsAddedByOtherStuff.append(i)

        # Add all the element's numbers together
        numberToSubtractFrom200 = sum(i["number"] for i in elementsAddedByOtherStuff)

        # Find elements to replace previous ones to fix element conflicts.
        self.elementsThatAddTo200 = self.findElementsThatAddUpTo(200 - numberToSubtractFrom200)
        self.updateBox()
    
    def boldVowels(self):
        """Bold all vowels"""
        # Initalise Variables
        # Postions of Vowels
        postionsOfVowels: list[int] = []

        # Previous postion of cursor
        previousCursor: int = 0

        # Find bold button
        boldButton = self.driver.find_elements(By.CLASS_NAME, "toolbar")[0].find_elements(By.XPATH, ".//*[contains(text(), 'Bold')]")[0]

        # Unbold entire password
        self._isPasswordBeingModified = True # Tell everything password is being modified
        self.password_box.send_keys(Keys.COMMAND + "a") # Select entire password

        # Is the entire password not bold already?
        if not "<strong>" + self.password_box.text + "</strong>" in self.password_box.get_attribute("innerHTML"):
            boldButton.click() # Bold everything

        if self._isFirstTimeBolding:
            # First time bolding, there is a fire now
            self.updateBox() # Put out fire

            # It isn't our first time bolding now
            self._isFirstTimeBolding = False

        self.password_box.send_keys(Keys.COMMAND + "a") # Select entire password again
        boldButton.click() # Unbold everything
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Deselect password
        self._isPasswordBeingModified = False # Tell everything we finished

        # Get contents of password box including EVERYTHING but replace incompatible emojis with placeholders
        truePasswordBoxContents = self.password_box.text.replace("🏋️‍♂️", "0")

        # Get all locations of vowels
        # Loop through vowels
        for i in self.vowels:
            # Loop through password
            for j in range(len(truePasswordBoxContents)):
                x = truePasswordBoxContents[j]
                # If current character is vowel
                if i.casefold() == x.casefold():
                    # Record postion of character
                    postionsOfVowels.append(j)
        
        # Sort postions of vowels in ascending order
        postionsOfVowels.sort()
        
        # Loop through vowel postions
        self._isPasswordBeingModified = True # Tell everything password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver.execute_script("arguments[0].style='white-space: nowrap !important'", self.password_box)

        # Move cursor to left side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_LEFT) # Go to the left side of the box

        # Begin loop
        for i in postionsOfVowels:            
            # Move cursor to postion of vowel
            for j in range(i - previousCursor):
                self.password_box.send_keys(Keys.ARROW_RIGHT) # Move cursor to the right by one
            
            # Select vowel
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_RIGHT)

            # Bold vowel
            boldButton.click()

            # Set old cursor for efficent moving of cursor
            previousCursor = i
        
        # Move cursor to right side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Go to the right side of the box

        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        self._isPasswordBeingModified = False # Tell everything we finished

    def getUnusedLetters(self, text : str):
        """Get all unused letters in `text: str`"""
        # Initalise variables
        unusedLetters: list[str] = []

        # Get the alphabet minus hex code characters
        alphabet: list[str] = list(string.ascii_lowercase)
        alphabet.remove("a")
        alphabet.remove("b")
        alphabet.remove("c")
        alphabet.remove("d")
        alphabet.remove("e")
        alphabet.remove("f")

        # Loop through characters in text
        for letter in alphabet:
                # Check if letter not in text
                if not letter in text.casefold():
                    # It isn't, add to unused letters
                    unusedLetters.append(letter)

        # Return result
        return unusedLetters
    
    def sacrificeTheWorthless(self):
        """Self explanatory"""
        # Get 2 unused characters
        unusedCharacters: list[str] = self.getUnusedLetters(self.password_box.text)[:2]

        # Sacrifice characters
        # Press buttons
        button1 = self.driver.find_elements(By.CLASS_NAME, "letters")[0].find_elements(By.XPATH, ".//*[contains(text(), '" + unusedCharacters[0].upper() + "')]")[0].click()
        button2 = self.driver.find_elements(By.CLASS_NAME, "letters")[0].find_elements(By.XPATH, ".//*[contains(text(), '" + unusedCharacters[1].upper() + "')]")[0].click()

        # Commit the very legal act of SACRIFICE
        sacrificeButton = self.driver.find_elements(By.CLASS_NAME, "sacrafice-btn")[0].click()

    def italicEverything(self):
        """Italic everything to statify rule 26"""
        # Find bold button
        italicButton = self.driver.find_elements(By.CLASS_NAME, "toolbar")[0].find_elements(By.XPATH, ".//*[contains(text(), 'Italic')]")[0]

        # Italic entire password
        self._isPasswordBeingModified = True # Tell everything password is being modified
        self.password_box.send_keys(Keys.COMMAND + "a") # Select entire password
        italicButton.click()
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Deselect entire password
        self._isPasswordBeingModified = False # Tell everything we finished

    def loadFontDropdown(self):
        """Find and load the font dropdown - Must be run before any font changing functions"""
        self.fontDropdown = self.driver.find_elements(By.CLASS_NAME, "toolbar")[0].find_elements(By.XPATH, ".//*[contains(text(), 'Wingdings')]")[0].find_element(By.XPATH, "./..")

    def wingdingEverything(self):
        """Turn everything into the WingDings font because computers can understand symbols"""
        # Get wingdings button
        wingDingsButton = self.fontDropdown.find_element(By.XPATH, ".//*[contains(text(), 'Wingdings')]")

        # Wingdings entire password
        self._isPasswordBeingModified = True # Tell everything password is being modified
        self.password_box.send_keys(Keys.COMMAND + "a") # Select entire password
        self.fontDropdown.click() # Open dropdown
        wingDingsButton.click() # Wingdings it
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Deselect entire password
        self._isPasswordBeingModified = False # Tell everything we finished

    def timesNewRomanNumerals(self):
        """Set the font to Times New Roman for all roman numerals"""
        # Initalise Variables
        # Postions of Roman Numerals
        postionsOfRomanNumerals: list[int] = []

        # Previous postion of cursor
        previousCursor: int = 0

        # Find Times New Roman button
        TimesNewRomanButton = self.fontDropdown.find_elements(By.XPATH, ".//*[contains(text(), 'Times New Roman')]")[0]

        # Get contents of password box including EVERYTHING but replace incompatible emojis with placeholders
        truePasswordBoxContents = self.password_box.text.replace("🏋️‍♂️", "0")

        # Get all locations of roman numerals
        # Loop through roman numerals
        for i in self.romanNumerals:
            # Loop through password
            for j in range(len(truePasswordBoxContents)):
                x = truePasswordBoxContents[j]
                # If current character is roman numeral
                if i == x:
                    # Record postion of character
                    postionsOfRomanNumerals.append(j)

        # Sort postions of Roman Numerals in ascending order
        postionsOfRomanNumerals.sort()
        
        # Loop through roman numeral postions
        self._isPasswordBeingModified = True # Tell everything password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver.execute_script("arguments[0].style='white-space: nowrap !important'", self.password_box)

        # Move cursor to left side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_LEFT) # Go to the left side of the box

        # Begin loop
        for i in postionsOfRomanNumerals:
            # Move cursor to postion of Roman Numeral
            for j in range(i - previousCursor):
                self.password_box.send_keys(Keys.ARROW_RIGHT) # Move cursor to the right by one
            
            # Select roman numeral
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_RIGHT)

            # Set font to Times New Roman
            self.fontDropdown.click()
            TimesNewRomanButton.click()

            # Set old cursor for efficent moving of cursor
            previousCursor = i
        
        # Move cursor to right side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Go to the right side of the box

        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        self._isPasswordBeingModified = False # Tell everything we finished

    def fontSizeFix(self):
        """Set font size correctly for numbers and letters"""
        # Initalise variables
        # Occurences of letters
        letterOccurences: dict = dict.fromkeys(list(string.ascii_lowercase), 0)

        # Allowed font sizes
        allowedFontSizes: list[int] = [0, 1, 4, 9, 12, 16, 25, 28, 32, 36, 42, 49, 64, 81]

        # Previous postion of cursor
        previousCursor: int = 0

        # Find Font Size Dropdown
        fontSizeDropdown = self.driver.find_elements(By.CLASS_NAME, "toolbar")[0].find_elements(By.XPATH, ".//*[contains(text(), '1px')]")[0].find_element(By.XPATH, "./..")

        # Get contents of password box including EVERYTHING but replace incompatible emojis with placeholders
        truePasswordBoxContents = self.password_box.text.replace("🏋️‍♂️", "=")
        
        # Loop through characters positions
        self._isPasswordBeingModified = True # Tell everything password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver.execute_script("arguments[0].style='white-space: nowrap !important'", self.password_box)

        # Move cursor to left side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_LEFT) # Go to the left side of the box

        # Begin loop
        for index in range(len(truePasswordBoxContents)):
            # Get character
            character = truePasswordBoxContents[index]

            # Check type of character and get font size
            if character.isdigit():
                # Set font size to character squared
                fontSize = int(character) ** 2
            elif character.isalpha():
                # How many times have we hit this letter
                letterHits = letterOccurences[character.lower()]

                # Increase the letter occurences by one
                letterOccurences[character.lower()] += 1

                # What font size to use
                fontSize = allowedFontSizes[letterHits]
            elif character == "|":
                # Override for retyping password
                fontSize = allowedFontSizes[1]
            else:
                continue # Font size doesn't matter

            # Move cursor to position of character
            for j in range(index - previousCursor):
                self.password_box.send_keys(Keys.ARROW_RIGHT) # Move cursor to the right by one
            
            # Select position of character
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_RIGHT)

            # Set font size to correct font size
            # Open up font size dropdown
            fontSizeDropdown.click()

            # Set font
            fontSizeDropdown.find_elements(By.XPATH, ".//*[contains(text(), '" + str(fontSize) + "px')]")[0].click()

            # Set old cursor for efficent moving of cursor
            previousCursor = index
        
        # Move cursor to right side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Go to the right side of the box

        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        self._isPasswordBeingModified = False # Tell everything we finished

    def fixPasswordLength(self):
        """Fix password length by making it a prime number and putting the length in the password"""
        # Get current length of password
        lengthOfPassword = int(self.password_length_counter.text)

        # How much padding do we need
        paddingRequired = 113 - lengthOfPassword

        # Tell everything the password is being modified
        self._isPasswordBeingModified = True

        # Move cursor to right side of text
        self.password_box.send_keys(Keys.COMMAND + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Go to the right side of the box

        # If Paul exists:
        if self.paulInOurPassword:
            self.password_box.send_keys(Keys.ARROW_LEFT) # WE MUST PROTECT PAUL, PAUL IS EVERYTHING, PAUL IS LIFE

        # Protect the worms food
        if self.paulHatched:
            # Run as many times as there are worms in the password
            for i in range(self.password_box.text.count("🐛")):
                self.password_box.send_keys(Keys.ARROW_LEFT) # Protect each worm

        # Type padding
        for i in range(paddingRequired):
            self.password_box.send_keys("|")

        # Tell everything that we finished
        self._isPasswordBeingModified = False

    def finalSteps(self):
        """EVERYTHING HAS BEEN LEADING UP TO THIS MOMENT, EVERYTHING"""
        # Get final password box text
        finalPasswordBox = self.driver.find_elements(By.CLASS_NAME, "password-final")[0].text

        # Stop feeding Paul and tell everything we are in the endgame
        self._isEndgame = True
        
        # Wait for Paul feeding to stop
        while self.feedPaulThread.is_alive():
            continue # Wait

        # Select all
        self.password_box.send_keys(Keys.COMMAND + "a")

        # Paste in old password
        self.password_box.send_keys(finalPasswordBox)

        # FORMATTING
        # Bold all vowels
        self.boldVowels()

        # Italic password
        self.italicEverything()

        # Reload font dropdown
        self.loadFontDropdown()

        # Wingding everything
        self.wingdingEverything()

        # Times New Roman Numerals
        self.timesNewRomanNumerals()

        # Font size
        self.fontSizeFix()

    def startFeedingPaul(self):
        """
        Start feeding Paul because PAUL IS LIFE

        Notice - This function runs in the background and will return instantly
        """
        if self.paulHatched:
            # SHOULDN'T BE CALLED, RAISE A TYPEERROR
            raise TypeError("Paul already hatched, function shouldn't be called")
        
        # Paul has hatched, so tell the rest of the class
        self.paulHatched = True

        # Start feeding Paul in the background
        self.feedPaulThread = threading.Thread(target=self._paulFeedThread, name="Paul Feeding Thread")
        self.feedPaulThread.start()
    
    def _paulFeedThread(self):
        """Internal function to feed Paul - DO NOT CALL DIRECTLY - WILL NEVER RETURN"""
        while True:
            # Wait for password to not be actively edited
            while self._isPasswordBeingModified:
                continue # Wait

            # If we are in the endgame, STOP
            if self._isEndgame:
                break

            # Move cursor to right side of text
            self.password_box.send_keys(Keys.COMMAND + "a") # Select all
            self.password_box.send_keys(Keys.ARROW_RIGHT) # Go to the right side of the box

            # Feed Paul
            self.password_box.send_keys("🐛")

            # Wait for Paul to eat his worm
            while self.password_box.text.count("🐛") >= 7:
                continue # Wait

    def RGBToHex(self, r: int, g: int, b: int):
        """Convert RGB color code to hex color code"""
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)