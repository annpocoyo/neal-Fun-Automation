"""
autopasswordgame.py - Automate the Password Game by Neal Agarwal at neal.fun
Author: annpocoyo
Credits:
Chess - Chess library
Requests - HTTP library
Stockfish - Best Chess Move Finder
Selenium - Browser automation library
"""

# Import Modules
import os # For URL Handling and custom modules
import sys # For custom modules
import json # For geoguesser
import time # For waiting
import chess # For analyzing chess board from displayed svg
import shutil # For finding if stockfish is in path
import datetime # For Wordle
import requests # For API requests
from stockfish import Stockfish # Used to find ideal chess move
import xml.etree.ElementTree as ET # Obtaining chess board from displayed svg
from selenium.webdriver.common.by import By # For browser control

# Add custom modules to path
sys.path.append(f"""{
        os.path.dirname(
            os.path.abspath(sys.argv[0])
        )
    }/Library""")

# Is stockfish in path,
if shutil.which("stockfish"):
    # Yes, get the path
    stockfishPath = shutil.which("stockfish")
else:
    # No, ask for the path
    stockfishPath = input("Please enter the full path to stockfish:") \
        .strip('\"') \
        .strip("\'") # Strip out quotes from the path just in case

# Load custom librarys
from autoPasswordLibrary import autoPasswordClass
autoPasswordGame = autoPasswordClass()

# Get today's date
date = datetime.date.today()

# Setup XML processing
xml = {'xml': 'http://www.w3.org/2000/svg'}

def main():
    # Type in static string to solve static questions
    autoPasswordGame.passwordContents += \
        "0!XXXV113june00:00pepsi🌑🌒🌓🌔🌕🌖🌗🌘🏋️‍♂️🏋️‍♂️🏋️‍♂️iamloved"
    autoPasswordGame.updateBox()
    
    # Find CAPTCHA
    captcha_code_source = \
        autoPasswordGame.driver.find_elements(By.CLASS_NAME, "captcha-img")[0] \
            .get_attribute("src")
    captcha = os.path.splitext(os.path.basename(captcha_code_source))[0]

    # Type CAPTCHA
    autoPasswordGame.passwordContents += captcha
    autoPasswordGame.updateBox()

    # Fix Number Conflicts
    autoPasswordGame.fixNumberConflicts()

    # Get the answer to today's Wordle
    # Make API request and get today's Wordle from it
    wordle = \
        requests.get(f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json") \
            .json()['solution']

    # Type today's Wordle
    autoPasswordGame.passwordContents += wordle
    autoPasswordGame.updateBox()

    # Solve geoguesser
    # Load json file for geoguesser which was pulled STRAIGHT from the game files
    mapsFile = \
        open(f"""{
            os.path.dirname(
                os.path.abspath(sys.argv[0])
            )
        }/Library/passwordGame/maps.json""")
    mapsMatchs = json.load(mapsFile)

    # Find embed url for geoguesser
    geoGuesserEmbed = autoPasswordGame.driver \
        .find_elements(By.XPATH, "//iframe[@class=\"geo\"]")[0] \
        .get_attribute("src")

    # Search for match with url in mapMatchs
    for i in mapsMatchs:
        if (i['embed'] == geoGuesserEmbed):
            # Match found
            # Set variable geoGuesserCountry to matching country
            geoGuesserCountry = i['title'].lower()

    # Close json file
    mapsFile.close()

    # Type country
    autoPasswordGame.passwordContents += geoGuesserCountry
    autoPasswordGame.updateBox()

    # Solve chess
    # Find chess svg URL
    chessSVGURL = \
        autoPasswordGame.driver.find_elements(By.CLASS_NAME, "chess-img")[0]\
        .get_attribute("src")

    # Who's turn is it? [TRUE = White, FALSE = Black]
    while autoPasswordGame.driver.find_elements(By.CLASS_NAME, "move")[0].text == "":
        continue # Wait until loading finished
    chessTurn = (
        autoPasswordGame.driver.find_elements(By.CLASS_NAME, "move")[0]
            .text == "White to move"
    )

    # Obtain SVG as text
    chessSVGText = requests.get(chessSVGURL).text

    # Load SVG
    chessSVG: ET.Element = ET.fromstring(chessSVGText)

    # Find chess matrix as text from SVG
    chessMatrixText = chessSVG.find(".//xml:pre", xml).text

    # Convert chess matrix to nested list
    chessMatrix = [[], [], [], [], [], [], [], []]
    for i in range(len(chessMatrixText.split("\n"))):
        chessMatrix[i] = chessMatrixText.split("\n")[i].split(" ")
    
    # Convert chess matrix into Chess.Board object
    chessBoard = chess.Board().empty()
    # Loop through chess matrix
    for i in range(len(chessMatrix)):
        # Get current item
        x: list = list(reversed(chessMatrix))[i]

        for j in range(len(x)):
            # Get current item
            y: str = x[j]

            # Is this a blank square, if yes, do nothing
            if not (y == '.'):
                # This is not a blank square:
                # Add matching square to chess board object
                square = j + (i * 8) # Which square are we placing in?
                color = y.isupper() # What color is this square?

                # Which piece are we?
                match y.upper():
                    case "R":
                        piece = chess.ROOK
                    case "N":
                        piece = chess.KNIGHT
                    case "B":
                        piece = chess.BISHOP
                    case "Q":
                        piece = chess.QUEEN
                    case "K":
                        piece = chess.KING
                    case "P":
                        piece = chess.PAWN

                # Fill in square
                chessBoard.set_piece_at(square, chess.Piece(piece, color))

    # Specify who's turn it is in the Chess.Board object
    chessBoard.turn = chessTurn

    # Find best move and send to password game
    # Initalise stockfish
    SF = Stockfish(path=stockfishPath, depth=25, parameters={"Threads": 2})
    
    # Supply analyzed chess board's FEN
    SF.set_fen_position(chessBoard.fen())

    # Find best chess move in UCI (Universal Chess Interface)
    bestMoveUCI = SF.get_best_move()

    # Convert best move to SAN (Standard Algebraic Notation)
    bestMoveSAN = chessBoard.san(chessBoard.parse_uci(bestMoveUCI))

    # Type best chess move in SAN
    autoPasswordGame.passwordContents += bestMoveSAN
    autoPasswordGame.updateBox()

    # Fix Number Conflicts
    autoPasswordGame.fixNumberConflicts()

    # PAUL IS LIFE (Add Paul to the password)
    autoPasswordGame.password_box.send_keys("🥚")
    autoPasswordGame.paulInOurPassword = True

    # Fix Element Conflicts
    autoPasswordGame.fixElementConflicts()

    # Wait for bold button to appear
    time.sleep(2)

    # Bold all vowels
    autoPasswordGame.boldVowels()

    # Paul has hatched now, so start feeding
    autoPasswordGame.startFeedingPaul()

    # Wait for rule about feeding to finish
    time.sleep(1)

    # Get YouTube video of specified length
    # Get YouTube rule words
    youtubeRuleWords = \
        autoPasswordGame.driver.find_elements(By.CLASS_NAME, "youtube")[0] \
        .find_elements(By.XPATH, ".//*[contains(text(), 'YouTube video')]")[0] \
        .text.split(" ")

    # Get YouTube video length
    # Get minutes
    youtubeMinutes = int(youtubeRuleWords[youtubeRuleWords.index("minute") - 1])
    
    # Get seconds
    # Is there a second in the rule
    if "second" in " ".join(youtubeRuleWords):
        # Yes, so get the seconds
        youtubeSeconds = \
            int(youtubeRuleWords[youtubeRuleWords.index("second") - 1])
    else:
        # No, so 0 seconds
        youtubeSeconds = 0

    # Load JSON file of YouTube videos
    youtubeVideosFile = \
        open(f"""{
            os.path.dirname(os.path.abspath(sys.argv[0]))
        }/Library/passwordGame/youtubeVideos.json""")
    youtubeVideoMatchs = json.load(youtubeVideosFile)

    # Get youtube video url
    youtubeVideo = "youtu.be/" \
    + youtubeVideoMatchs[str(youtubeMinutes)][youtubeSeconds]

    # Close JSON file
    youtubeVideosFile.close()

    # Add YouTube video to password
    autoPasswordGame.passwordContents += youtubeVideo
    autoPasswordGame.updateBox()

    # Fix any element conflicts
    autoPasswordGame.fixElementConflicts()

    # Wait
    time.sleep(0.50)

    # Fix any number conflicts
    autoPasswordGame.fixNumberConflicts()

    # Wait
    time.sleep(0.50)

    # Rebold vowels
    autoPasswordGame.boldVowels()

    # Wait for rules to load
    time.sleep(1)

    # Sacrifice letters
    autoPasswordGame.sacrificeTheWorthless()

    # Wait for italic button to appear
    time.sleep(2)

    # Italic everything
    autoPasswordGame.italicEverything()

    # Wait for font picker to appear
    time.sleep(2)

    # Load font dropdown
    autoPasswordGame.loadFontDropdown()

    # WingDing everything
    autoPasswordGame.wingdingEverything()

    # Wait for rules to load
    time.sleep(1)

    # Initalise variables to not break syntax
    hexColor: str = "0"

    # Get color display
    colorDisplay = \
        autoPasswordGame.driver.find_elements(By.CLASS_NAME, "rand-color")[0]

    # Get refresh button
    colorRefresh = \
        colorDisplay.find_elements(By.CLASS_NAME, "refresh")[0]

    # Tell everything password is being modified
    autoPasswordGame._isPasswordBeingModified = True

    # Loop until optimal hex with no numbers found
    while any(char.isdigit() for char in hexColor):
        # Refresh color
        colorRefresh.click()

        # Get rgb value of color as tuple
        RGBColor: tuple = \
            tuple(map(
                int, colorDisplay.value_of_css_property("background") \
                    .replace("rgb(", "") \
                    .replace(")", "") \
                    .replace(",", "") \
                    .split(" ")
            ))

        # Convert rgb to hex
        hexColor = autoPasswordGame.RGBToHex(*RGBColor)

    # Add hex code to password
    autoPasswordGame.passwordContents += hexColor
    autoPasswordGame.updateBox()

    # Tell everything we finished
    autoPasswordGame._isPasswordBeingModified = False

    # Wait
    time.sleep(0.50)

    # Rebold all vowels, again
    autoPasswordGame.boldVowels()

    # Wait for Times New Roman button to appear
    time.sleep(1)

    # Set the font to Times New Roman for all roman numerals
    autoPasswordGame.timesNewRomanNumerals()

    # Wait for font dropdown to appear
    time.sleep(1)

    # Add padding for password box length
    autoPasswordGame.fixPasswordLength()

    # Set font size correctly
    autoPasswordGame.fontSizeFix()

    # WAIT FOR THE USER TO CLICK YES
    # Get password divs
    passwordDiv = \
        autoPasswordGame.driver \
            .find_elements(By.CLASS_NAME, "password-wrapper")[0]

    # Initalise variable
    textElement: list = []
    
    # Wait
    while len(textElement) == 0:
        # Check if div contains text
        textElement: list = \
            passwordDiv.find_elements(By.XPATH,
                ".//*[contains(text(), 'Please re-type your password')]"
            )
        continue # Wait

    autoPasswordGame.finalSteps()

    while True:
        continue

if __name__ == '__main__':
    main()
