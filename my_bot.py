"""
Welcome to your first Snake bot!

This bot's name is DumbAI. It's purpose is simple (don't expect it to gain much points :) ):
1. Initialize game
2. Go until you reach the wall and turn to counter-clockwise direction
3. If you are at the right wall/go up look if the fruit is on the same line (have the same y coordinate as snake)
    3.a Fruit is on the same line -> turn left
    3.b Else -> do nothing
4. Go to step 2

Note: You need to import snk package at all time, because it contains the game engine.
"""

# Let's start by importing the Snake Starter Kit so we can interface with the Snake engine
import snk

# GAME START
# Here we define the bot's name as Settler and initialize the game, including communication with the Halite engine.
game = snk.Game('DumbAI')
while True:
    # TURN START
    # Get the current state of the map
    map_status = game.map_status()
    # Here we define our action to be sent to the Snake engine at the end of the turn
    action = None
    # Get individual information about the map
    heading = map_status.snake_direction
    snake_position = map_status.snake_position
    white_fruit = map_status.white_fruit
    min_x, max_x = 0, map_status.window_x
    min_y, max_y = 0, map_status.window_y

    # move into counter clockwise direction if we reach a wall
    # if direction is upwards, turn left
    if heading == 'UP':
        wall_distance = snake_position[1] - min_y
        if wall_distance < 1:
            game.send_command('LEFT')
            continue

    # if direction is downwards, turn up
    elif heading == 'DOWN':
        wall_distance = max_y - snake_position[1]
        if wall_distance < 2:
            game.send_command('RIGHT')
            continue

    # if direction is right, turn down
    elif heading == 'RIGHT':
        wall_distance = max_x - snake_position[0]
        if wall_distance < 2:
            game.send_command('UP')
            continue

    # if direction is left, turn down
    else:
        wall_distance = snake_position[0] - min_x
        if wall_distance < 1:
            game.send_command('DOWN')
            continue

    # if we are at the right wall/if direction is upwards
    if heading == 'UP':
        # if we are at the same y coordinate/line with fruit, turn left
        if snake_position[1] == white_fruit[1]:
            game.send_command('LEFT')
            continue

    # send action to game engine
    game.send_command(action)
