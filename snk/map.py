import random


class Map:
    """A class for the map. Contains all attributes which are needed for the bot.

    """

    def __init__(self, ):
        # Window size
        self.__window_x = 72
        self.__window_y = 48
        # defining snake default position
        self.__snake_position = [10, 5]
        # defining first 4 blocks of snake body
        self.__snake_body = [[10, 5],
                             [9, 5],
                             [8, 5],
                             [7, 5]]
        self.__paralyzed_segments = 0
        self.__super_segments = 0
        # set a seed for the generator
        random.seed(8)
        # fruit position
        self.__fruit_position = [random.randrange(1, self.__window_x),
                                 random.randrange(1, self.__window_y)]

        self.__poison_position = [[random.randrange(1, self.__window_x),
                                   random.randrange(1, self.__window_y)]]

        self.__paralyze_position = [[random.randrange(1, self.__window_x),
                                     random.randrange(1, self.__window_y)]]

        self.__super_food = []

        self.__fruit_spawn = True

        # setting default snake direction towards right
        self.__snake_direction = 'RIGHT'

    @property
    def window_x(self) -> int:
        """ Maximum size of the map in x dimension.

        :return: Maximum x value
        :rtype: int
        """
        return self.__window_x

    @property
    def window_y(self) -> int:
        """Maximum size of the map in y dimension.

        :return: Maximum y value
        :rtype: int
        """
        return self.__window_y

    @property
    def snake_position(self) -> list:
        """Position of the head of the snake.

        :return: x and y coordinates [x,y]
        :rtype: list
        """
        return self.__snake_position

    @snake_position.setter
    def snake_position(self, snake_position: list) -> list:
        self.__snake_position = snake_position

    @property
    def snake_body(self) -> [list]:
        """Coordinates of all parts of the snake body

        :return: x and y coordinates of all body parts
        :rtype: [list]
        """
        return self.__snake_body

    @snake_body.setter
    def snake_body(self, snake_body: list) -> list:
        self.__snake_body = snake_body

    @property
    def fruit_position(self) -> list:
        """Coordinates of the fruit

        :return: x and y coordinates of the fruit
        :rtype: list
        """
        return self.__fruit_position

    @fruit_position.setter
    def fruit_position(self, fruit_position: list):
        self.__fruit_position = fruit_position

    @property
    def poison_position(self) -> [list]:
        """Coordinates of the poison food

        :return: x and y of the poison food
        :rtype: [list]
        """
        return self.__poison_position

    @poison_position.setter
    def poison_position(self, poison_position: list):
        self.__poison_position = poison_position

    @property
    def paralyze_position(self):
        return self.__paralyze_position

    @paralyze_position.setter
    def paralyze_position(self, paralyze_position: list):
        self.__paralyze_position = paralyze_position

    @property
    def super_food(self) -> list:
        """Coordinates of super food.

        :return: x and y of super food
        :rtype: list
        """
        return self.__super_food

    @super_food.setter
    def super_food(self, super_food: list):
        self.__super_food = super_food

    @property
    def fruit_spawn(self) -> bool:
        return self.__fruit_spawn

    @fruit_spawn.setter
    def fruit_spawn(self, fruit_spawn: bool):
        self.__fruit_spawn = fruit_spawn

    @property
    def snake_direction(self) -> str:
        """The direction in which the snake is currently heading.

        :return: Directions can be: UP|DOWN|LEFT|RIGHT
        :rtype: str
        """
        return self.__snake_direction

    @property
    def paralyzed_segments(self) -> int:
        return self.__paralyzed_segments

    @paralyzed_segments.setter
    def paralyzed_segments(self, num: int):
        self.__paralyzed_segments = num

    @property
    def super_segments(self) -> int:
        return self.__super_segments

    @super_segments.setter
    def super_segments(self, num: int):
        self.__super_segments = num

    @snake_direction.setter
    def snake_direction(self, snake_direction: bool):
        self.__snake_direction = snake_direction

    def spawn_new_fruit(self):
        self.__fruit_position = [random.randrange(1, self.__window_x),
                                 random.randrange(1, self.__window_y)]
        if self.__fruit_position in self.__paralyze_position or self.__fruit_position in self.__poison_position:
            self.spawn_new_fruit()
        elif self.__fruit_position in self.__super_food:
            self.spawn_new_fruit()

    def spawn_new_poison(self):
        poison_position = [random.randrange(1, self.__window_x),
                           random.randrange(1, self.__window_y)]
        if poison_position in self.__paralyze_position or poison_position in self.__fruit_position:
            self.spawn_new_poison()
        elif poison_position in self.__super_food:
            self.spawn_new_poison()
        else:
            self.__poison_position.append(poison_position)

    def spawn_new_paralyze_food(self):
        paralyzed_food = [random.randrange(1, self.__window_x),
                          random.randrange(1, self.__window_y)]

        if paralyzed_food in self.__poison_position or paralyzed_food in self.__fruit_position:
            self.spawn_new_paralyze_food()
        elif paralyzed_food in self.__super_food:
            self.spawn_new_paralyze_food()
        else:
            self.__paralyze_position.append(paralyzed_food)

    def spawn_new_super_food(self):
        self.__super_food = [random.randrange(1, self.__window_x),
                             random.randrange(1, self.__window_y)]

        if self.__super_food in self.__poison_position or self.__super_food in self.__fruit_position:
            self.spawn_new_super_food()
        elif self.__super_food in self.__paralyze_position:
            self.spawn_new_super_food()
