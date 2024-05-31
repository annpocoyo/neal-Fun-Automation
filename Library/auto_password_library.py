"""
Auto Password Library - All the external code used to automate the password game.

Inside this library:

AutoPasswordClass - contains all functions used by autopasswordgame.py
"""
import os # For loading JSON
import sys #  ^
import json # |
import string # Cleaner way of getting the alphabet
import threading # For feeding Paul in the background
from _auto_browser_base import AutoBrowserBase # Automatic browser control base
from selenium.webdriver.common.by import By # For Browser Control
from selenium.webdriver.common.keys import Keys

class AutoPasswordClass(AutoBrowserBase):
    """This class contains all functions used by autopasswordgame.py"""
    # Initalize Variables
    # Contents of password
    password_contents: str = ""

    # Vowels
    vowels: list[str] = ["a", "e", "i", "o", "u", "y"]

    # Roman Numerals
    roman_numerals: list[str] = ["I", "V", "X", "L", "C", "D", "M"]
    
    # Digits used to add to 25
    digits_that_add_to_25: str = "992"

    # Elements with atomic numbers that add up to 200
    elements_that_add_to_200: list[str] = ["Fm"]

    # Is Paul in our password?
    paul_in_our_password: bool = False

    # Has paul hatched?
    paul_hatched: bool = False

    # Font size state storage
    current_font_size: list[int] = []

    # Internal variable, is password being modified
    _is_password_being_modified: bool = False

    # Internal Variable, is first time bolding?
    _is_first_time_bolding: bool = True

    # Internal Variable, is ENDGAME?
    _is_endgame: bool = False

    def __init__(self, gecko_driver_path = None):
        # Initalize Class
        # Contact parent costructor first
        super().__init__(gecko_driver_path, "https://neal.fun/password-game/")

        # Find password box
        self.password_box = \
            self.driver.find_elements(By.CLASS_NAME, "ProseMirror")[0]

        # Find password length counter
        self.password_length_counter = \
            self.driver.find_elements(By.CLASS_NAME, "password-length")[0]

        # Load JSON file for the ENTIRE FRICKING PERIODIC TABLE
        elements_file = open(f"""{
            os.path.dirname(os.path.abspath(sys.argv[0]))
        }/Library/passwordGame/elements.json""")
        self.elements = json.load(elements_file)

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
        elements_file.close()

    def update_box(self):
        """Refresh the Password Box"""
        # Broadcast the password is being modified
        self._is_password_being_modified = True

        # Disable password box wrapping as it messes up cursor postion
        self.driver \
            .execute_script(
                "arguments[0].style='white-space: nowrap !important'",
                self.password_box
            )

        # Refresh password box
        self.password_box.send_keys(self._action_key + "a")
        # If Paul exists:
        if self.paul_in_our_password:
             # WE MUST PROTECT PAUL, PAUL IS EVERYTHING, PAUL IS LIFE
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_LEFT)
        # Protect the worms food
        if self.paul_hatched:
            # Run as many times as there are worms in the password
            for i in range(self.password_box.text.count("🐛")):
                 # Protect each worm
                self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_LEFT)
        self.password_box.send_keys(Keys.BACKSPACE)
        self.password_box.send_keys(
            str(self.digits_that_add_to_25) \
            + "".join(self.elements_that_add_to_200) \
            + self.password_contents
        )
        
        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        # Wait for password box to update
        while self.password_box.text.replace("🥚", "") \
            .replace("🐔", "").replace("🐛", "") != str(self.digits_that_add_to_25) \
            + "".join(self.elements_that_add_to_200) + self.password_contents:
            continue # Wait

        self._is_password_being_modified = False # Tell everything we finished

    def find_digits_that_add_up_to(self, number: int):
        """Find 3 digits that add up to `number: int`"""
        # Loop through all combinations of digits
        for i in range(10):
            for j in range(10):
                for k in range(10):
                    # Do they add up to the number
                    if (i + j + k == number):
                        # Yes, return digits
                        return str(i) + str(j) + str(k)

    def fix_number_conflicts(self):
        """Fix any number conflicts"""
        # Initialize local variables
        number_to_subtract_from_25 = 0
        digits_added_by_other_stuff = []

        # Get all digits added by other things and add them together
        digits_added_by_other_stuff = \
            [int(i) for i in self.password_contents if i.isdigit()]
        number_to_subtract_from_25 = sum(digits_added_by_other_stuff)

        # Find digits to replace previous ones to fix number conflicts.
        self.digits_that_add_to_25 = \
            self.find_digits_that_add_up_to(25 - number_to_subtract_from_25)
        self.update_box()

    def find_elements_that_addup_to(self, number: int):
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

    def fix_element_conflicts(self):
        """Fix any element conflicts"""
        # Initialize local variables
        number_to_subtract_from_200 = 0
        elements_added_by_other_stuff = []

        # Get all elements added by other things
        for i in self.elements:
            for j in range(len(self.password_contents)):
                x = self.password_contents[j]

                # Check if single character element symbol exists in string
                if ((x == i["symbol"]) and (
                    (len(self.password_contents) - 1 == j) or (
                        not any(ext["symbol"] == 
                                x + self.password_contents[j + 1]
                                for ext in self.elements)
                ))):
                    # Yes: add it in
                    elements_added_by_other_stuff.append(i)
                # Check if double character element symbol exists in string
                elif ((len(self.password_contents) - 1 != j) and 
                      (x + self.password_contents[j + 1] == i["symbol"])):
                    # Yes: add it in
                    elements_added_by_other_stuff.append(i)

        # Add all the element's numbers together
        number_to_subtract_from_200 = \
            sum(i["number"] for i in elements_added_by_other_stuff)

        # Find elements to replace previous ones to fix element conflicts.
        self.elements_that_add_to_200 = \
            self.find_elements_that_addup_to(200 - number_to_subtract_from_200)
        self.update_box()
    
    def bold_vowels(self):
        """Bold all vowels"""
        # Initalise Variables
        # Postions of Vowels
        postions_of_vowels: list[int] = []

        # Previous postion of cursor
        previous_cursor: int = 0

        # Find bold button
        bold_button = self.driver.find_elements(By.CLASS_NAME, "toolbar")[0] \
            .find_elements(By.XPATH, ".//*[contains(text(), 'Bold')]")[0]

        # Unbold entire password
        self._is_password_being_modified = True # Broadcast the password is being modified
        self.password_box.send_keys(self._action_key + "a") # Select entire password

        # Is the entire password not bold already?
        if not ("<strong>" + self.password_box.text + "</strong>"
                in self.password_box.get_attribute("innerHTML")):
            bold_button.click() # Bold everything

        if self._is_first_time_bolding:
            # First time bolding, there is a fire now
            self.update_box() # Put out fire

            # It isn't our first time bolding now
            self._is_first_time_bolding = False

        self.password_box.send_keys(self._action_key + "a") # Select entire password again
        bold_button.click() # Unbold everything
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Deselect password
        self._is_password_being_modified = False # Tell everything we finished

        # Get contents of password box but strip out incompatible characters
        true_password_box_contents = self.password_box.text.replace("🏋️‍♂️", "0")

        # Get all locations of vowels
        # Loop through vowels
        for i in self.vowels:
            # Loop through password
            for j in range(len(true_password_box_contents)):
                x = true_password_box_contents[j]
                # If current character is vowel
                if i.casefold() == x.casefold():
                    # Record postion of character
                    postions_of_vowels.append(j)
        
        # Sort postions of vowels in ascending order
        postions_of_vowels.sort()
        
        # Loop through vowel postions
        self._is_password_being_modified = True # Broadcast the password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver.execute_script(
            "arguments[0].style='white-space: nowrap !important'",
            self.password_box)

        # Move cursor to left side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_LEFT) # Move to left of box

        # Begin loop
        for i in postions_of_vowels:            
            # Move cursor to postion of vowel
            for j in range(i - previous_cursor):
                self.password_box.send_keys(Keys.ARROW_RIGHT) # Move cursor right by one
            
            # Select vowel
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_RIGHT)

            # Bold vowel
            bold_button.click()

            # Set old cursor for efficent moving of cursor
            previous_cursor = i
        
        # Move cursor to right side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Move to right of box

        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        self._is_password_being_modified = False # Tell everything we finished

    def getUnusedLetters(self, text : str):
        """Get all unused letters in `text: str`"""
        # Initalise variables
        unused_letters: list[str] = []

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
                    unused_letters.append(letter)

        # Return result
        return unused_letters
    
    def sacrifice_the_worthless(self):
        """Self explanatory"""
        # Get 2 unused characters
        unused_characters: list[str] = \
            self.getUnusedLetters(self.password_box.text)[:2]

        # Sacrifice characters
        # Press buttons
        button1 = self.driver.find_elements(By.CLASS_NAME, "letters")[0] \
            .find_elements(By.XPATH, ".//*[contains(text(), '"
                           + unused_characters[0].upper() + "')]")[0].click()
        button2 = self.driver.find_elements(By.CLASS_NAME, "letters")[0] \
            .find_elements(By.XPATH, ".//*[contains(text(), '" \
                           + unused_characters[1].upper() + "')]")[0].click()

        # Commit the very legal act of SACRIFICE
        sacrifice_button = \
            self.driver.find_elements(By.CLASS_NAME, "sacrafice-btn")[0].click()

    def italic_everything(self):
        """Italic everything to statify rule 26"""
        # Find bold button
        italic_button = self.driver.find_elements(By.CLASS_NAME, "toolbar")[0] \
            .find_elements(By.XPATH, ".//*[contains(text(), 'Italic')]")[0]

        # Italic entire password
        self._is_password_being_modified = True # Broadcast the password is being modified
        self.password_box.send_keys(self._action_key + "a") # Select entire password
        italic_button.click()
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Deselect entire password
        self._is_password_being_modified = False # Tell everything we finished

    def load_font_dropdown(self):
        """Find and load the font dropdown - Must be run before any font changing functions"""
        self.font_dropdown = \
            self.driver.find_elements(By.CLASS_NAME, "toolbar")[0] \
                .find_elements(By.XPATH, ".//*[contains(text(), 'Wingdings')]")[0] \
                .find_element(By.XPATH, "./..")

    def wingding_everything(self):
        """Turn everything into the WingDings font because computers can understand symbols"""
        # Get wingdings button
        wingdings_button = \
            self.font_dropdown \
                .find_element(By.XPATH, ".//*[contains(text(), 'Wingdings')]")

        # Wingdings entire password
        self._is_password_being_modified = True # Broadcast the password is being modified
        self.password_box.send_keys(self._action_key + "a") # Select entire password
        self.font_dropdown.click() # Open dropdown
        wingdings_button.click() # Wingdings it
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Deselect entire password
        self._is_password_being_modified = False # Tell everything we finished

    def times_new_roman_numerals(self):
        """Set the font to Times New Roman for all roman numerals"""
        # Initalise Variables
        # Postions of Roman Numerals
        postions_of_roman_numerals: list[int] = []

        # Previous postion of cursor
        previous_cursor: int = 0

        # Find Times New Roman button
        times_new_roman_button = self.font_dropdown \
            .find_elements(By.XPATH, ".//*[contains(text(), 'Times New Roman')]")[0]

        # Get contents of password box but strip out incompatible characters
        true_password_box_contents = self.password_box.text.replace("🏋️‍♂️", "0")

        # Get all locations of roman numerals
        # Loop through roman numerals
        for i in self.roman_numerals:
            # Loop through password
            for j in range(len(true_password_box_contents)):
                x = true_password_box_contents[j]
                # If current character is roman numeral
                if i == x:
                    # Record postion of character
                    postions_of_roman_numerals.append(j)

        # Sort postions of Roman Numerals in ascending order
        postions_of_roman_numerals.sort()
        
        # Loop through roman numeral postions
        self._is_password_being_modified = True # Broadcast the password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver \
            .execute_script(
                "arguments[0].style='white-space: nowrap !important'",
                self.password_box
            )

        # Move cursor to left side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_LEFT) # Move to left of box

        # Begin loop
        for i in postions_of_roman_numerals:
            # Move cursor to postion of Roman Numeral
            for j in range(i - previous_cursor):
                self.password_box.send_keys(Keys.ARROW_RIGHT) # Move cursor right by one
            
            # Select roman numeral
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_RIGHT)

            # Set font to Times New Roman
            self.font_dropdown.click()
            times_new_roman_button.click()

            # Set old cursor for efficent moving of cursor
            previous_cursor = i
        
        # Move cursor to right side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Move to right of box

        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        self._is_password_being_modified = False # Tell everything we finished

    def font_size_fix(self):
        """Set font size correctly for numbers and letters"""
        # Initalise variables
        # Occurences of letters
        letter_occurences: dict = dict.fromkeys(list(string.ascii_lowercase), 0)

        # Allowed font sizes
        allowed_font_sizes: list[int] = \
            [0, 1, 4, 9, 12, 16, 25, 28, 32, 36, 42, 49, 64, 81]

        # Previous postion of cursor
        previous_cursor: int = 0

        # Find Font Size Dropdown
        font_size_dropdown = \
            self.driver.find_elements(By.CLASS_NAME, "toolbar")[0] \
                .find_elements(By.XPATH, ".//*[contains(text(), '1px')]")[0] \
                .find_element(By.XPATH, "./..")

        # Get contents of password box but strip out incompatible characters
        true_password_box_contents = self.password_box.text.replace("🏋️‍♂️", "=")
        
        # Loop through characters positions
        self._is_password_being_modified = True # Broadcast the password is being modified

        # Disable password box wrapping as it messes up cursor postion
        self.driver \
            .execute_script(
                "arguments[0].style='white-space: nowrap !important'",
                self.password_box
            )

        # Move cursor to left side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_LEFT) # Move to left of box

        # Begin loop
        for index in range(len(true_password_box_contents)):
            # Get character
            character = true_password_box_contents[index]

            # Check type of character and get font size
            if character.isdigit():
                # Set font size to character squared
                font_size = int(character) ** 2
            elif character.isalpha():
                # How many times have we hit this letter
                letter_hits = letter_occurences[character.lower()]

                # Increase the letter occurences by one
                letter_occurences[character.lower()] += 1

                # What font size to use
                font_size = allowed_font_sizes[letter_hits]
            elif character == "|":
                # Override for retyping password
                font_size = allowed_font_sizes[1]
            else:
                continue # Font size doesn't matter

            # Move cursor to position of character
            for j in range(index - previous_cursor):
                self.password_box.send_keys(Keys.ARROW_RIGHT) # Move cursor right by one
            
            # Select position of character
            self.password_box.send_keys(Keys.SHIFT + Keys.ARROW_RIGHT)

            # Set font size to correct font size
            # Open up font size dropdown
            font_size_dropdown.click()

            # Set font
            font_size_dropdown.find_elements(By.XPATH, ".//*[contains(text(), '" \
                                           + str(font_size) + "px')]")[0].click()

            # Set old cursor for efficent moving of cursor
            previous_cursor = index
        
        # Move cursor to right side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Move to right of box

        # Restore password box wrapping
        self.driver.execute_script("arguments[0].style=''", self.password_box)

        self._is_password_being_modified = False # Tell everything we finished

    def fix_password_length(self):
        """Fix password length by making it a prime number and putting 
           the length in the password"""
        # Get current length of password
        password_length = int(self.password_length_counter.text)

        # How much padding do we need
        padding_required = 113 - password_length

        # Tell everything the password is being modified
        self._is_password_being_modified = True

        # Move cursor to right side of text
        self.password_box.send_keys(self._action_key + "a") # Select all
        self.password_box.send_keys(Keys.ARROW_RIGHT) # Move to right of box

        # If Paul exists:
        if self.paul_in_our_password:
             # WE MUST PROTECT PAUL, PAUL IS EVERYTHING, PAUL IS LIFE
            self.password_box.send_keys(Keys.ARROW_LEFT)

        # Protect the worms food
        if self.paul_hatched:
            # Run as many times as there are worms in the password
            for i in range(self.password_box.text.count("🐛")):
                # Protect each worm
                self.password_box.send_keys(Keys.ARROW_LEFT)

        # Type padding
        for i in range(padding_required):
            self.password_box.send_keys("|")

        # Tell everything that we finished
        self._is_password_being_modified = False

    def final_steps(self):
        """EVERYTHING HAS BEEN LEADING UP TO THIS MOMENT, EVERYTHING"""
        # Get final password box text
        final_password_box = \
            self.driver.find_elements(By.CLASS_NAME, "password-final")[0].text

        # Stop feeding Paul and tell everything we are in the endgame
        self._is_endgame = True
        
        # Wait for Paul feeding to stop
        while self._feed_paul_thread.is_alive():
            continue # Wait

        # Select all
        self.password_box.send_keys(self._action_key + "a")

        # Paste in old password
        self.password_box.send_keys(final_password_box)

        # FORMATTING
        # Bold all vowels
        self.bold_vowels()

        # Italic password
        self.italic_everything()

        # Reload font dropdown
        self.load_font_dropdown()

        # Wingding everything
        self.wingding_everything()

        # Times New Roman Numerals
        self.times_new_roman_numerals()

        # Font size
        self.font_size_fix()

    def start_feeding_paul(self):
        """
        Start feeding Paul because PAUL IS LIFE

        Notice - This function runs in the background and will return instantly
        """
        if self.paul_hatched:
            # SHOULDN'T BE CALLED, RAISE A TYPEERROR
            raise TypeError("Paul already hatched, function shouldn't be called")
        
        # Paul has hatched, so tell the rest of the class
        self.paul_hatched = True

        # Start feeding Paul in the background
        self._feed_paul_thread = \
            threading.Thread(target=self._paul_feed_thread,
                             name="Paul Feeding Thread")
        self._feed_paul_thread.start()
    
    def _paul_feed_thread(self):
        """Internal function to feed Paul - DO NOT CALL DIRECTLY - WILL NEVER RETURN"""
        while True:
            # Wait for password to not be actively edited
            while self._is_password_being_modified:
                continue # Wait

            # If we are in the endgame, STOP
            if self._is_endgame:
                break

            # Move cursor to right side of text
            self.password_box.send_keys(self._action_key + "a") # Select all
            self.password_box.send_keys(Keys.ARROW_RIGHT) # Move to right of box

            # Feed Paul
            self.password_box.send_keys("🐛")

            # Wait for Paul to eat his worm
            while self.password_box.text.count("🐛") >= 7:
                continue # Wait

    def rgb_to_hex(self, r: int, g: int, b: int):
        """Convert RGB color code to hex color code"""
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)