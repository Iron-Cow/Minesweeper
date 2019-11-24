import pygame


class RectField(object):
    def __init__(self, x: float, y: float, width: float, height: float, color: tuple):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self._color, [self._x, self._y, self._width, self._height])

    def get_w(self):
        return self._width


class EventManager(object):
    def check_events(self) -> bool:
        for event in pygame.event.get():  # key mapping of the game
            # print(event)
            if event.type == pygame.QUIT:
                return False
            #
            # if event.type == pygame.KEYDOWN:
            #     try:
            #         if event.key == pygame.K_RIGHT:
            #             print(111)
            #     except:
            #         1
            #         elif event.key == pygame.K_LEFT:
            #             figure.move_left()
            #
            #         elif event.key == pygame.K_DOWN:
            #             figure.fall()
            #
            #         elif event.key == pygame.K_SPACE:
            #             figure.set_config(figure.rotated_figure())

                # except IndexError:
                #     pass
        return True


class Cell(RectField):
    """Bomb or empty"""
    def __init__(self, x, y, w, color = (255, 0, 0), bomb: bool = False):
        super().__init__(x, y, w, w, color)
        self.__bomb = bomb

    def is_bomb(self) -> bool:
        return self.__bomb

    def set_bomb(self):
        self.__bomb = True

    def draw(self, surface):
        if self.__bomb:
            pygame.draw.rect(surface, self._color, [self._x+1, self._y+1, self._width-1, self._height-1],)


class FieldCoordinates(object):
    def __init__(self, nx: int, ny: int, exapmle_cell: Cell):
        self.__nx = nx
        self.__ny = ny
        self.__field = [[Cell(x=x*exapmle_cell.get_w(),
                              y=y*exapmle_cell.get_w(),
                              w=exapmle_cell.get_w(), ) for x in range(self.__nx)] for y in range(self.__ny)]

    def get_field(self):
        return self.__field


class GameField(RectField):
    """Minefield for the game"""
    def __init__(self, color, grid_color: tuple, game_cell: Cell, field: list):
        super().__init__(x=0, y=0,
                         width=len(field[0])*game_cell.get_w(),
                         height=len(field)*game_cell.get_w(),
                         color=color)
        self.__grid_color = grid_color
        self.__game_cell = game_cell
        self.__field = field

    def draw_grid(self, surface):
        # surface.fill(self._color)
        for x, _ in enumerate(self.__field[0]):  # Vertical lines
            pygame.draw.line(surface,
                             self.__grid_color,
                             (x * self.__game_cell.get_w(), 0),
                             (x * self.__game_cell.get_w(), self._height),
                             width=1
                             )

        for y, _ in enumerate(self.__field):  # Horizontal lines
            pygame.draw.line(surface,
                             self.__grid_color,
                             (0, y * self.__game_cell.get_w()),
                             (self._width, y * self.__game_cell.get_w()),
                             width=1
                             )

        pygame.draw.line(surface,
                         self.__grid_color,
                         (self._width, 0),
                         (self._width, self._height),
                         width=1
                             )

        pygame.draw.line(surface,
                         self.__grid_color,
                         (0, self._height),
                         (self._width, self._height,),
                         width=1
                         )

    def draw_cells(self, surface):
        for row in self.__field:
            for cell in row:
                cell.draw(surface)



