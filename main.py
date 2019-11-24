from models import *
import pygame
from random import randint

if __name__ == "__main__":
    run = True
    pygame.init()

    # rect = Cell(200, 200, 50, (255, 255, 0))
    game_cell = Cell(0, 0, 50, (255, 0, 0))  # example of the cell
    current_field = FieldCoordinates(nx=20, ny=10, exapmle_cell=game_cell).get_field()

    window = pygame.display.set_mode(size=(1+len(current_field[0])*game_cell.get_w(),
                                           1+len(current_field)*game_cell.get_w()))

    for _ in range(10):
        while True:
            x = randint(0, len(current_field[0])-1)
            y = randint(0, len(current_field)-1)
            if current_field[y][x].is_bomb():
                pass
            else:
                current_field[y][x].set_bomb()
                # print(x, y)
                break

    # For test
    # current_field[3][3].set_bomb()
    # print(current_field[3][3].is_bomb())

    event_manager = EventManager(game_cell, current_field)
    game_field = GameField(color=(0, 0, 0),
                           grid_color=(100, 255, 5),
                           game_cell=game_cell,
                           field=current_field)
    while run:
        # window.fill((0, 0, 0))
        game_field.draw_grid(window)
        game_field.draw_cells(window)

        run = event_manager.check_events()
        # rect.draw(window)

        pygame.display.update()
