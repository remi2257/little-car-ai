from src.Games.GameDraw import *
from src.const import *


def run_draw_map(**kwargs):
    # --- INIT Variable--- #

    stop = False

    # --- INIT PYGAME--- #

    game = GameDraw()

    # Boucle infinie
    while not stop:
        pygame.time.Clock().tick(240)

        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == pygame_const.QUIT or (
                    event.type == pygame_const.KEYDOWN and event.key in list_break):  # Si un de ces événements est de type QUIT
                stop = True  # On arrête la boucle
            if event.type == pygame_const.MOUSEBUTTONDOWN:
                game.is_holding_left = True
            if event.type == pygame_const.MOUSEBUTTONUP:
                game.is_holding_left = False
                game.last_x = -1
                game.last_y = -1
            # if pygame.mouse.get_pressed()[0]:  # See if the user has clicked or dragged their mouse
            if event.type == pygame_const.KEYDOWN:
                if event.key == pygame_const.K_s:  # See if the user has clicked or dragged their mouse
                    game.save_map()
                if event.key == pygame_const.K_f:  # See if the user has clicked or dragged their mouse
                    game.free_map()
                if event.key == pygame_const.K_c:  # See if the user has clicked or dragged their mouse
                    game.checkpoint_cmd()
        pos = pygame.mouse.get_pos()

        game.actualize(pos)


if __name__ == '__main__':
    run_draw_map()
