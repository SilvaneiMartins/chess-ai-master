import pygame
import sys

from const import *
from game import Game


# classe principal
class Main:
    def __init__(self):
        # inicializa o pygame
        pygame.init()

        # cria a janela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Xadrez Ai Master - by: Silvanei Martins')

        # cria o jogo
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game

        while True:
            game.show_log(screen)
            game.show_pieces(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
