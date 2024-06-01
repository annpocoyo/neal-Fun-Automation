# Neal.fun Automation

A collection of scripts automating various aspects of the website: <https://neal.fun>!

## Compatiblilty

These scripts currently have been tested to be compatible with **macOS** and **Windows** using Python **3.12.2**!

## Dependiences

Automating the password game requires the following modules:

* Chess - for getting the chess game data
* Stockfish - for getting the best chess move
* Requests - for getting today's Wordle
* Selenium - for automating and controlling the browser

Alongside these modules you also need the programs **Firefox and GeckoDriver** to be installed. (Chrome has some **bugs** with emojis that make it **impossible** to use!)

## What do the scripts do?

| Script Name: | Script Purpose: |
| ------------ | --------------- |
| `autopasswordgame.py` | Automate completing the password game! **Doesn't** have 100% success rate. |
| `autoinfinitecraft.py` (**Work in Progress**) | **Automate crafting things** in Infinite Craft and automatically **find and store recipes** for certain things. |
