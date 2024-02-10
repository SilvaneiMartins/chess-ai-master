import pygame
import sys

from const import *


class Main:
    def __init__(self):
        # inicializa o pygame
        pygame.init()

        # cria a janela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Xadrez Ai Master - by: Silvanei Martins')

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
