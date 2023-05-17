# importing libraries
import pygame
import random

from snk.map import Map
from snk.screen import Screen


class Game:
    """
    Class for the snake game. Must be initialized to start a game.
    """
    def __init__(self, bot_name: str = ''):
        # Set the name of the bot
        self.bot_name = bot_name
        # Initializing the map
        self.__map = Map()
        # Initializing the screen to get visuals
        self.__screen = Screen(self.bot_name, self.__map.window_x, self.__map.window_y)
        # Set the initial values for the game
        self.__score = 0
        self.__turn = 1
        self.__yellow_segments = self.__map.yellow_segments
        self.__paralyzed = None
        self.__blue_segments = self.__map.blue_segments
        self.change_to = self.__map.snake_direction
        # Initialising pygame
        pygame.init()

    def send_command(self, action: str = None) -> None:
        """Method to send the action to the game engine and simulate the next step.

        :param action: The action which has to be executed in the next time step.
        :return: None
        """
        # check if game has been interrupted
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()
                break

        self.change_to = action
        # check if snake is paralyzed
        if self.__paralyzed is not None:
            self.__paralyzed += 1
            if self.__paralyzed % 50 == 0:
                if self.__map.snake_direction == 'UP':
                    self.change_to = random.choice(['UP', 'LEFT', 'RIGHT'])
                elif self.__map.snake_direction == 'DOWN':
                    self.change_to = random.choice(['DOWN', 'LEFT', 'RIGHT'])
                elif self.__map.snake_direction == 'LEFT':
                    self.change_to = random.choice(['DOWN', 'LEFT', 'UP'])
                else:
                    self.change_to = random.choice(['DOWN', 'RIGHT', 'UP'])
                self.__blue_segments -= 1

            elif self.__blue_segments == 0:
                self.__paralyzed = None

        # Compute the new direction of the snake

        if self.change_to == 'UP' and self.__map.snake_direction != 'DOWN':
            self.__map.snake_direction = 'UP'
        if self.change_to == 'DOWN' and self.__map.snake_direction != 'UP':
            self.__map.snake_direction = 'DOWN'
        if self.change_to == 'LEFT' and self.__map.snake_direction != 'RIGHT':
            self.__map.snake_direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.__map.snake_direction != 'LEFT':
            self.__map.snake_direction = 'RIGHT'

        # Moving the snake
        if self.__map.snake_direction == 'UP':
            self.__map.snake_position[1] -= 1
        if self.__map.snake_direction == 'DOWN':
            self.__map.snake_position[1] += 1
        if self.__map.snake_direction == 'LEFT':
            self.__map.snake_position[0] -= 1
        if self.__map.snake_direction == 'RIGHT':
            self.__map.snake_position[0] += 1

        # Snake body growing mechanism
        # if fruits and snakes collide then score will be incremented by 10
        self.__map.snake_body.insert(0, list(self.__map.snake_position))
        if self.__map.snake_position[0] == self.__map.white_fruit[0] and self.__map.snake_position[1] == \
                self.__map.white_fruit[1]:
            # If we have super segments then score will be incremented by 20
            if self.__yellow_segments > 0:
                self.__score += 50
                self.__yellow_segments -= 1
            else:
                self.__score += 10
            self.__turn += 1
            self.__map.fruit_spawn = False
            # Every 5 turns we will spawn new super food, which give the snake 3 super segments
            if self.__turn % 5 == 0:
                self.__map.spawn_new_yellow_fruit()
            else:
                self.__map.yellow_fruit = []
        else:
            self.__map.snake_body.pop()

        # check if snake eats super food
        if len(self.__map.yellow_fruit) > 0:
            if self.__map.snake_position[0] == self.__map.yellow_fruit[0] and self.__map.snake_position[1] == \
                    self.__map.yellow_fruit[1]:
                self.__yellow_segments = 3
                self.__map.yellow_fruit = []

        # check if snake eats paralyze food
        for index, item in enumerate(self.__map.blue_fruits):
            if self.__map.snake_position[0] == item[0] and self.__map.snake_position[1] == item[1]:
                if self.__yellow_segments > 0:
                    self.__map.blue_fruits = []
                    self.__yellow_segments = 0
                    self.__score -= 50
                else:
                    self.__paralyzed = 0
                    self.__blue_segments = 3
                    self.__map.blue_fruits.pop(index)
                    self.__score -= 10

        # Spawn new fruit and poison
        if not self.__map.fruit_spawn:
            self.__map.spawn_new_fruit()
            self.__map.spawn_new_poison()
            self.__map.spawn_new_paralyze_food()
        self.__map.fruit_spawn = True

        # visuals
        self.__screen.reset_window()
        if self.__paralyzed is None:
            self.__screen.draw_snake(self.__yellow_segments, self.__map)
        else:
            self.__screen.draw_paralyzed_snake(self.__map, self.__blue_segments)
        self.__screen.draw_fruit(self.__map)
        self.__screen.draw_yellow_fruit(self.__map)
        self.__screen.draw_poison(self.__map)
        self.__screen.draw_paralyze(self.__map)

        # Game Over conditions: run into wall
        if self.__map.snake_position[0] < 0 or self.__map.snake_position[0] > self.__map.window_x - 1:
            self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)
        if self.__map.snake_position[1] < 0 or self.__map.snake_position[1] > self.__map.window_y - 1:
            self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)

        # Game over conditions
        if self.__yellow_segments == 0:
            # Eat poison food
            for item in self.__map.red_fruits:
                if self.__map.snake_position[0] == item[0] and self.__map.snake_position[1] == item[1]:
                    self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)

            # Touching the snake body
            for block in self.__map.snake_body[1:]:
                if self.__map.snake_position[0] == block[0] and self.__map.snake_position[1] == block[1]:
                    self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)

        # Decrease number of super segments if snake eats poison or touches snake body
        else:
            # Eat poison food
            for index, item in enumerate(self.__map.red_fruits):
                if self.__map.snake_position[0] == item[0] and self.__map.snake_position[1] == item[1]:
                    self.__yellow_segments = 0
                    self.__score -= 50
                    self.__map.red_fruits.pop(index)
                    num_poison = len(self.__map.red_fruits) // 2
                    del self.__map.red_fruits[-num_poison:]

            # Touching the snake body
            for index, block in enumerate(self.__map.snake_body[1:]):
                if self.__map.snake_position[0] == block[0] and self.__map.snake_position[1] == block[1]:
                    self.__yellow_segments -= 1
                    num = len(self.__map.snake_body) - index
                    del self.__map.snake_body[-num:]

        # displaying score continuously
        self.__screen.show_score(self.__score)

        # Refresh game screen
        self.__screen.update()

    def play(self):
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'

        # check if snake is paralyzed
        if self.__paralyzed is not None:
            self.__paralyzed += 1
            if self.__paralyzed % 50 == 0:
                if self.__map.snake_direction == 'UP':
                    self.change_to = random.choice(['UP', 'LEFT', 'RIGHT'])
                elif self.__map.snake_direction == 'DOWN':
                    self.change_to = random.choice(['DOWN', 'LEFT', 'RIGHT'])
                elif self.__map.snake_direction == 'LEFT':
                    self.change_to = random.choice(['DOWN', 'LEFT', 'UP'])
                else:
                    self.change_to = random.choice(['DOWN', 'RIGHT', 'UP'])
                self.__blue_segments -= 1

            elif self.__blue_segments == 0:
                self.__paralyzed = None

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if self.change_to == 'UP' and self.__map.snake_direction != 'DOWN':
            self.__map.snake_direction = 'UP'
        if self.change_to == 'DOWN' and self.__map.snake_direction != 'UP':
            self.__map.snake_direction = 'DOWN'
        if self.change_to == 'LEFT' and self.__map.snake_direction != 'RIGHT':
            self.__map.snake_direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.__map.snake_direction != 'LEFT':
            self.__map.snake_direction = 'RIGHT'

        # Moving the snake
        if self.__map.snake_direction == 'UP':
            self.__map.snake_position[1] -= 1
        if self.__map.snake_direction == 'DOWN':
            self.__map.snake_position[1] += 1
        if self.__map.snake_direction == 'LEFT':
            self.__map.snake_position[0] -= 1
        if self.__map.snake_direction == 'RIGHT':
            self.__map.snake_position[0] += 1

        # Snake body growing mechanism
        # if fruits and snakes collide then score will be incremented by 10
        self.__map.snake_body.insert(0, list(self.__map.snake_position))
        if self.__map.snake_position[0] == self.__map.white_fruit[0] and self.__map.snake_position[1] == \
                self.__map.white_fruit[1]:
            # If we have super segments then score will be incremented by 20
            if self.__yellow_segments > 0:
                self.__score += 50
                self.__yellow_segments -= 1
            else:
                self.__score += 10
            self.__turn += 1
            self.__map.fruit_spawn = False
            # Every 5 turns we will spawn new super food, which give the snake 3 super segments
            if self.__turn % 5 == 0:
                self.__map.spawn_new_yellow_fruit()
            else:
                self.__map.yellow_fruit = []
        else:
            self.__map.snake_body.pop()

        # check if snake eats super food
        if len(self.__map.yellow_fruit) > 0:
            if self.__map.snake_position[0] == self.__map.yellow_fruit[0] and self.__map.snake_position[1] == \
                    self.__map.yellow_fruit[1]:
                self.__yellow_segments = 3
                self.__map.yellow_fruit = []

        # check if snake eats paralyze food
        for index, item in enumerate(self.__map.blue_fruits):
            if self.__map.snake_position[0] == item[0] and self.__map.snake_position[1] == item[1]:
                if self.__yellow_segments > 0:
                    self.__map.blue_fruits = []
                    self.__yellow_segments = 0
                    self.__score -= 50
                else:
                    self.__paralyzed = 0
                    self.__blue_segments = 3
                    self.__map.blue_fruits.pop(index)
                    self.__score -= 10

        # Spawn new fruit and poison
        if not self.__map.fruit_spawn:
            self.__map.spawn_new_fruit()
            self.__map.spawn_new_poison()
            self.__map.spawn_new_paralyze_food()
        self.__map.fruit_spawn = True

        # visuals
        self.__screen.reset_window()
        if self.__paralyzed is None:
            self.__screen.draw_snake(self.__yellow_segments, self.__map)
        else:
            self.__screen.draw_paralyzed_snake(self.__map, self.__blue_segments)
        self.__screen.draw_fruit(self.__map)
        self.__screen.draw_yellow_fruit(self.__map)
        self.__screen.draw_poison(self.__map)
        self.__screen.draw_paralyze(self.__map)

        # Game Over conditions: run into wall
        if self.__map.snake_position[0] < 0 or self.__map.snake_position[0] > self.__map.window_x - 1:
            self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)
        if self.__map.snake_position[1] < 0 or self.__map.snake_position[1] > self.__map.window_y - 1:
            self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)

        # Game over conditions
        if self.__yellow_segments == 0:
            # Eat poison food
            for item in self.__map.red_fruits:
                if self.__map.snake_position[0] == item[0] and self.__map.snake_position[1] == item[1]:
                    self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)

            # Touching the snake body
            for block in self.__map.snake_body[1:]:
                if self.__map.snake_position[0] == block[0] and self.__map.snake_position[1] == block[1]:
                    self.__screen.game_over(self.__score, self.__map.window_x, self.__map.window_y)

        # Decrease number of super segments if snake eats poison or touches snake body
        else:
            # Eat poison food
            for index, item in enumerate(self.__map.red_fruits):
                if self.__map.snake_position[0] == item[0] and self.__map.snake_position[1] == item[1]:
                    self.__yellow_segments = 0
                    self.__score -= 50
                    self.__map.red_fruits.pop(index)
                    num_poison = len(self.__map.red_fruits)//2
                    del self.__map.red_fruits[-num_poison:]

            # Touching the snake body
            for index, block in enumerate(self.__map.snake_body[1:]):
                if self.__map.snake_position[0] == block[0] and self.__map.snake_position[1] == block[1]:
                    self.__yellow_segments -= 1
                    num = len(self.__map.snake_body) - index
                    del self.__map.snake_body[-num:]

        # displaying score continuously
        self.__screen.show_score(self.__score)

        # Refresh game screen
        self.__screen.update()

    def map_status(self):
        """Method to get the status of the map.

        :return: A map object, which has the following attrubutes:
            snake_position = Position of the snake head as a list: [x,y]
            snake_body = Position of all body parts of the snake as a list of lists: [[x1,y1],...,[xn, yn]]
            white_fruit = x and y coordinates of the food as a list: [x,y]
            red_fruits = x and y coordinates of poison food as a list of lists: [[x1,y1],...,[xn, yn]]
            yellow_fruit = x and y coordinates of super food as a list: [x,y] (gives snake 3 super segments)
            snake_direction = The direction in which the snake is heading as a string: UP|DOWN|RIGHT|LEFT
            window_x = Maximum size of map in x dimension
            window_y = Maximum size of map in y dimension
        """
        return self.__map
