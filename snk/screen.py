import time

import pygame

from snk.map import Map


class Screen:
    """Class to do all the visuals.

    """

    def __init__(self, bot_name: str, window_x: int, window_y: int):
        # set the speed of the snake
        self.bot_name = bot_name
        self.__snake_speed = 15
        # defining colors
        self.__black = pygame.Color(0, 0, 0)
        self.__white = pygame.Color(255, 255, 255)
        self.__red = pygame.Color(255, 0, 0)
        self.__green = pygame.Color(0, 255, 0)
        self.__blue = pygame.Color(0, 0, 255)
        self.__yellow = pygame.Color(255, 255, 0)
        self.__game_window = None

        # Initialise game window
        pygame.display.set_caption('SnAIke: ' + self.bot_name)
        self.__game_window = pygame.display.set_mode((window_x * 10, window_y * 10))

        # FPS (frames per second) controller
        self.clock = pygame.time.Clock()

    def reset_window(self) -> None:
        """Reset/clear the window.

        :return: None
        """
        self.__game_window.fill(self.__black)

    def draw_snake(self, super_segments: int, map: Map) -> None:
        """Draw all part of the snake onto the window.

        :param super_segments: Number of super segments of the snake
        :param map: The map object
        :return: None
        """
        if super_segments > 0:
            for index, pos in enumerate(map.snake_body):
                if index <= super_segments:
                    pygame.draw.rect(self.__game_window, self.__yellow,
                                     pygame.Rect(pos[0] * 10, pos[1] * 10, 10, 10))
                else:
                    pygame.draw.rect(self.__game_window, self.__green,
                                     pygame.Rect(pos[0] * 10, pos[1] * 10, 10, 10))
        else:
            for pos in map.snake_body:
                pygame.draw.rect(self.__game_window, self.__green,
                                 pygame.Rect(pos[0] * 10, pos[1] * 10, 10, 10))

    def draw_fruit(self, map) -> None:
        """Draw fruit onto the screen.

        :param map: The map object
        :return: None
        """
        pygame.draw.rect(self.__game_window, self.__white, pygame.Rect(
            map.white_fruit[0] * 10, map.white_fruit[1] * 10, 10, 10))

    def draw_yellow_fruit(self, map: Map) -> None:
        """Draw the super food.

        :param map: The map object.
        :return: None
        """
        if len(map.yellow_fruit) > 0:
            pygame.draw.rect(self.__game_window, self.__yellow, pygame.Rect(
                map.yellow_fruit[0] * 10, map.yellow_fruit[1] * 10, 10, 10))

    def draw_poison(self, map: Map) -> None:
        """Draw poison food.

        :param map: The map object
        :return: None
        """
        for item in map.red_fruits:
            pygame.draw.rect(self.__game_window, self.__red, pygame.Rect(
                item[0] * 10, item[1] * 10, 10, 10))

    def draw_paralyze(self, map: Map) -> None:
        """Draw poison food.

        :param map: The map object
        :return: None
        """
        for item in map.blue_fruits:
            pygame.draw.rect(self.__game_window, self.__blue, pygame.Rect(
                item[0] * 10, item[1] * 10, 10, 10))

    def draw_paralyzed_snake(self, map: Map, countdown: int):
        if countdown > 0:
            for index, pos in enumerate(map.snake_body):
                if index <= countdown:
                    pygame.draw.rect(self.__game_window, self.__blue,
                                     pygame.Rect(pos[0] * 10, pos[1] * 10, 10, 10))
                else:
                    pygame.draw.rect(self.__game_window, self.__green,
                                     pygame.Rect(pos[0] * 10, pos[1] * 10, 10, 10))
        else:
            for pos in map.snake_body:
                pygame.draw.rect(self.__game_window, self.__green,
                                 pygame.Rect(pos[0] * 10, pos[1] * 10, 10, 10))

    def show_score(self, score: int) -> None:
        """Show the score at the upper left corner of the window.

        :param score: The score to be shown
        :return: None
        """
        font = 'times new roman'
        size = 20
        color = self.__white
        # creating font object score_font
        score_font = pygame.font.SysFont(font, size)

        # create the display surface object
        # score_surface
        score_surface = score_font.render('Score : ' + str(score), True, color)

        # create a rectangular object for the text
        # surface object
        score_rect = score_surface.get_rect()

        # displaying text
        self.__game_window.blit(score_surface, score_rect)

    def game_over(self, score: int, window_x: int, window_y: int) -> None:
        """Show the game over screen and close the window after 2 seconds.

        :param score: The final score
        :param window_x: Size of the window in x
        :param window_y: Size of the window in y
        :return: None
        """
        # creating font object my_font
        my_font = pygame.font.SysFont('times new roman', 50)

        # creating a text surface on which text
        # will be drawn
        game_over_surface = my_font.render(
            'Your Score is : ' + str(score), True, self.__red)

        # create a rectangular object for the text
        # surface object
        game_over_rect = game_over_surface.get_rect()

        # setting position of the text
        game_over_rect.midtop = ((window_x / 2) * 10, (window_y / 4) * 10)

        # blit will draw the text on screen
        self.__game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        # after 2 seconds we will quit the program
        time.sleep(2)

        # deactivating pygame library
        pygame.quit()

        # quit the program
        quit()

    def update(self) -> None:
        """Update the display and tick the clock.

        :return: None
        """
        pygame.display.update()
        # Frame Per Second /Refresh Rate
        self.clock.tick(self.__snake_speed)
