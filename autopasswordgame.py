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
    stockfish_path = shutil.which("stockfish")
else:
    # No, ask for the path
    stockfish_path = input("Please enter the full path to stockfish:") \
        .strip('\"') \
        .strip("\'") # Strip out quotes from the path just in case

# Load custom librarys
from auto_password_library import AutoPasswordClass
auto_password_game = AutoPasswordClass()

# Get today's date
date = datetime.date.today()

# Setup XML processing
xml = {'xml': 'http://www.w3.org/2000/svg'}

def main():
    # Type in static string to solve static questions
    auto_password_game.password_contents += \
        "0!XXXV113june00:00pepsi🌑🌒🌓🌔🌕🌖🌗🌘🏋️‍♂️🏋️‍♂️🏋️‍♂️iamloved"
    auto_password_game.update_box()
    
    # Find CAPTCHA
    captcha_code_source = \
        auto_password_game.driver.find_elements(By.CLASS_NAME, "captcha-img")[0] \
            .get_attribute("src")
    captcha = os.path.splitext(os.path.basename(captcha_code_source))[0]

    # Type CAPTCHA
    auto_password_game.password_contents += captcha
    auto_password_game.update_box()

    # Fix Number Conflicts
    auto_password_game.fix_number_conflicts()

    # Get the answer to today's Wordle
    # Make API request and get today's Wordle from it
    wordle = \
        requests.get(f"https://www.nytimes.com/svc/wordle/v2/{date:%Y-%m-%d}.json") \
            .json()['solution']

    # Type today's Wordle
    auto_password_game.password_contents += wordle
    auto_password_game.update_box()

    # Solve geoguesser
    # Load json file for geoguesser which was pulled STRAIGHT from the game files
    maps_file = \
        open(f"""{
            os.path.dirname(
                os.path.abspath(sys.argv[0])
            )
        }/Library/passwordGame/maps.json""")
    maps_matches = json.load(maps_file)

    # Find embed url for geoguesser
    geo_guesser_embed = auto_password_game.driver \
        .find_elements(By.XPATH, "//iframe[@class=\"geo\"]")[0] \
        .get_attribute("src")

    # Search for match with url in map matches
    for i in maps_matches:
        if (i['embed'] == geo_guesser_embed):
            # Match found
            # Set variable geo_guesser_country to matching country
            geo_guesser_country = i['title'].lower()

    # Close json file
    maps_file.close()

    # Type country
    auto_password_game.password_contents += geo_guesser_country
    auto_password_game.update_box()

    # Solve chess
    # Find chess svg URL
    chess_svg_url = \
        auto_password_game.driver.find_elements(By.CLASS_NAME, "chess-img")[0]\
        .get_attribute("src")

    # Who's turn is it? [TRUE = White, FALSE = Black]
    while auto_password_game.driver.find_elements(By.CLASS_NAME, "move")[0].text == "":
        continue # Wait until loading finished
    chess_turn = (
        auto_password_game.driver.find_elements(By.CLASS_NAME, "move")[0]
            .text == "White to move"
    )

    # Obtain SVG as text
    chess_svg_text = requests.get(chess_svg_url).text

    # Load SVG
    chess_svg: ET.Element = ET.fromstring(chess_svg_text)

    # Find chess matrix as text from SVG
    chess_matrix_text = chess_svg.find(".//xml:pre", xml).text

    # Convert chess matrix to nested list
    chess_matrix = [[], [], [], [], [], [], [], []]
    for i in range(len(chess_matrix_text.split("\n"))):
        chess_matrix[i] = chess_matrix_text.split("\n")[i].split(" ")
    
    # Convert chess matrix into Chess.Board object
    chess_board = chess.Board().empty()
    # Loop through chess matrix
    for i in range(len(chess_matrix)):
        # Get current item
        x: list = list(reversed(chess_matrix))[i]

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
                chess_board.set_piece_at(square, chess.Piece(piece, color))

    # Specify who's turn it is in the Chess.Board object
    chess_board.turn = chess_turn

    # Find best move and send to password game
    # Initalise stockfish
    SF = Stockfish(path=stockfish_path, depth=25, parameters={"Threads": 2})
    
    # Supply analyzed chess board's FEN
    SF.set_fen_position(chess_board.fen())

    # Find best chess move in UCI (Universal Chess Interface)
    best_move_uci = SF.get_best_move()

    # Convert best move to SAN (Standard Algebraic Notation)
    best_move_san = chess_board.san(chess_board.parse_uci(best_move_uci))

    # Type best chess move in SAN
    auto_password_game.password_contents += best_move_san
    auto_password_game.update_box()

    # Fix Number Conflicts
    auto_password_game.fix_number_conflicts()

    # PAUL IS LIFE (Add Paul to the password)
    auto_password_game.password_box.send_keys("🥚")
    auto_password_game.paul_in_our_password = True

    # Fix Element Conflicts
    auto_password_game.fix_element_conflicts()

    # Wait for bold button to appear
    time.sleep(2)

    # Bold all vowels
    auto_password_game.bold_vowels()

    # Paul has hatched now, so start feeding
    auto_password_game.start_feeding_paul()

    # Wait for rule about feeding to finish
    time.sleep(1)

    # Get YouTube video of specified length
    # Get YouTube rule words
    youtube_rule_words = \
        auto_password_game.driver.find_elements(By.CLASS_NAME, "youtube")[0] \
        .find_elements(By.XPATH, ".//*[contains(text(), 'YouTube video')]")[0] \
        .text.split(" ")

    # Get YouTube video length
    # Get minutes
    youtube_minutes = int(youtube_rule_words[youtube_rule_words.index("minute") - 1])
    
    # Get seconds
    # Is there a second in the rule
    if "second" in " ".join(youtube_rule_words):
        # Yes, so get the seconds
        youtube_seconds = \
            int(youtube_rule_words[youtube_rule_words.index("second") - 1])
    else:
        # No, so 0 seconds
        youtube_seconds = 0

    # Load JSON file of YouTube videos
    youtube_videos_file = \
        open(f"""{
            os.path.dirname(os.path.abspath(sys.argv[0]))
        }/Library/passwordGame/youtubeVideos.json""")
    youtube_video_matches = json.load(youtube_videos_file)

    # Get youtube video url
    youtube_video = "youtu.be/" \
    + youtube_video_matches[str(youtube_minutes)][youtube_seconds]

    # Close JSON file
    youtube_videos_file.close()

    # Add YouTube video to password
    auto_password_game.password_contents += youtube_video
    auto_password_game.update_box()

    # Fix any element conflicts
    auto_password_game.fix_element_conflicts()

    # Wait
    time.sleep(0.50)

    # Fix any number conflicts
    auto_password_game.fix_number_conflicts()

    # Wait
    time.sleep(0.50)

    # Rebold vowels
    auto_password_game.bold_vowels()

    # Wait for rules to load
    time.sleep(1)

    # Sacrifice letters
    auto_password_game.sacrifice_the_worthless()

    # Wait for italic button to appear
    time.sleep(2)

    # Italic everything
    auto_password_game.italic_everything()

    # Wait for font picker to appear
    time.sleep(2)

    # Load font dropdown
    auto_password_game.load_font_dropdown()

    # WingDing everything
    auto_password_game.wingding_everything()

    # Wait for rules to load
    time.sleep(1)

    # Initalise variables to not break syntax
    hex_color: str = "0"

    # Get color display
    color_display = \
        auto_password_game.driver.find_elements(By.CLASS_NAME, "rand-color")[0]

    # Get refresh button
    color_refresh = \
        color_display.find_elements(By.CLASS_NAME, "refresh")[0]

    # Tell everything password is being modified
    auto_password_game._is_password_being_modified = True

    # Loop until optimal hex with no numbers found
    while any(char.isdigit() for char in hex_color):
        # Refresh color
        color_refresh.click()

        # Get rgb value of color as tuple
        rgb_color: tuple = \
            tuple(map(
                int, color_display.value_of_css_property("background") \
                    .replace("rgb(", "") \
                    .replace(")", "") \
                    .replace(",", "") \
                    .split(" ")
            ))

        # Convert rgb to hex
        hex_color = auto_password_game.rgb_to_hex(*rgb_color)

    # Add hex code to password
    auto_password_game.password_contents += hex_color
    auto_password_game.update_box()

    # Tell everything we finished
    auto_password_game._is_password_being_modified = False

    # Wait
    time.sleep(0.50)

    # Rebold all vowels, again
    auto_password_game.bold_vowels()

    # Wait for Times New Roman button to appear
    time.sleep(1)

    # Set the font to Times New Roman for all roman numerals
    auto_password_game.times_new_roman_numerals()

    # Wait for font dropdown to appear
    time.sleep(1)

    # Add padding for password box length
    auto_password_game.fix_password_length()

    # Set font size correctly
    auto_password_game.font_size_fix()

    # WAIT FOR THE USER TO CLICK YES
    # Get password divs
    password_div = \
        auto_password_game.driver \
            .find_elements(By.CLASS_NAME, "password-wrapper")[0]

    # Initalise variable
    text_element: list = []
    
    # Wait
    while len(text_element) == 0:
        # Check if div contains text
        text_element: list = \
            password_div.find_elements(By.XPATH,
                ".//*[contains(text(), 'Please re-type your password')]"
            )
        continue # Wait

    auto_password_game.final_steps()

    while True:
        continue

if __name__ == '__main__':
    main()
