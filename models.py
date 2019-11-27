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


class Cell(RectField):
    """Bomb or empty"""
    def __init__(self, x, y, w, color = (255, 0, 0), bomb: bool = False, label: str = ""):
        super().__init__(x, y, w, w, color)
        self.__bomb = bomb
        self.__label = label

    def is_bomb(self) -> bool:
        return self.__bomb

    def set_bomb(self):
        self.__bomb = True

    def draw(self, surface):
        if self.get_label() != "flag":
            font = pygame.font.Font("freesansbold.ttf", 14)
            nearby_bombs = font.render(str(self.__label), True, (0, 255, 0))
            surface.blit(nearby_bombs, (self._x + self._width * 0.43, (self._y + self._width * 0.43)))

        if self.__bomb:
            pygame.draw.rect(surface, self._color, [self._x+1, self._y+1, self._width-1, self._height-1],)

        elif self.__label == " ":
            pygame.draw.rect(surface, (100, 100, 100), [self._x + 1, self._y + 1, self._width - 1, self._height - 1], )

        elif self.__label == "flag":
            pygame.draw.line(surface, (255, 255, 255),
                             (self._x + 0.25 * self._width, self._y + 0.25 * self._height),
                             (self._x + 0.25 * self._width, self._y + 0.75 * self._height),
                             2
                             )
            pygame.draw.rect(surface, (255, 0, 0),
                             [self._x + 0.25 * self._width,
                              self._y + 0.25 * self._height,
                              self._width / 2,
                              self._height / 4])

    def get_label(self):
        return self.__label

    def set_label(self, label) -> None:
        self.__label = label


class EventManager(object):
    def __init__(self, example_cell: Cell, field: list):
        self.__example_cell = example_cell
        self.__field = field

    def get_click_cell(self, event) -> tuple:  # x, y   (2, 4)
        return event.pos[0]//self.__example_cell.get_w(), event.pos[1] //\
               self.__example_cell.get_w()

    def game_over(self, window):
        run = True
        while run:
            window.fill((255, 0, 0))
            font = pygame.font.Font("freesansbold.ttf", 55)
            gameover = font.render("GAME OVER", True, (0, 255, 0))
            for event in pygame.event.get():  # key mapping of the game
                # print(event)
                if event.type == pygame.QUIT:
                    run = False
            window.blit(gameover,
                        (len(self.__field[0]) * self.__example_cell.get_w() // 3, len(self.__field) * self.__example_cell.get_w() // 2))
            pygame.display.update()
        return False

    def get_surround_bombs(self, x, y) -> int:
        surround_cells = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        s = 0
        for cell in surround_cells:
            try:
                try_cell = list(map(sum, list(zip((x, y), cell))))  # surrounding cell around clicked cell
                if -1 in try_cell:
                    raise IndexError
                if self.__field[try_cell[1]][try_cell[0]].is_bomb():
                    s += 1
            except IndexError:
                continue
        return s

    def open_cell(self, window, xx, yy):
        x = xx
        y = yy
        cells_to_check = [(x, y)]
        while True:
            cells_to_check.pop(cells_to_check.index((x, y)))
            # print(f"x - {x}, y - {y}")
            if not self.__field[y][x].is_bomb():  # if not bomb
                # print(self.get_surround_bombs(x, y))
                if self.get_surround_bombs(x, y):  # if there are bombs around ...
                    self.__field[y][x].set_label(self.get_surround_bombs(x, y))

                else:  # case without bombs
                    self.__field[y][x].set_label(" ")  # current cell change label
                    surround_cells = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
                    for cell in surround_cells:
                        try:
                            try_cell = tuple(map(sum, list(zip((x, y), cell))))  # [3, 1] example
                            if -1 in try_cell:  # index should be positive
                                raise IndexError
                            # print(try_cell)

                            if self.__field[try_cell[1]][try_cell[0]].get_label() == "":
                                # print(self.__field[try_cell[1]][try_cell[0]].get_label())
                                if try_cell not in cells_to_check:
                                    cells_to_check.append(try_cell)

                        except IndexError:
                            continue
            else:
                return self.game_over(window)
            if cells_to_check:
                x, y = cells_to_check[0]
            else:
                break
        return True

    def check_events(self, window) -> bool:
        for event in pygame.event.get():  # key mapping of the game
            # print(event)
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = self.get_click_cell(event)
                if event.button == 1:
                    return self.open_cell(window, x, y)
                elif event.button == 3:
                    if self.__field[y][x].get_label() == "":
                        self.__field[y][x].set_label("flag")
                    elif self.__field[y][x].get_label() == "flag":
                        self.__field[y][x].set_label("")
        return True


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



