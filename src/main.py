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
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_bg(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # click do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    # se clicou no quadrado ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                
                # mouse em movimento
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)
                
                # solta o click do mouse
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()
                
                # fechar a janela
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
