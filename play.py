"""
Welcome to the Snake game!

This file only serves for you as a human player. You can use it to play the game by yourself or to test different
strategies before implementing them in your bot. Have fun!

Note: You need to import snk package at all time, because it contains the game engine.
"""

import snk

game = snk.Game('AI4fun')
while True:
    game.play()
