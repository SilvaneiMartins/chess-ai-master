import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move


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
            # mostra o metodo
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            # se estiver arrastando
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
                        # pedra valida (Color)?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # mostra o metodo
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                # mouse em movimento
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        # mostra o metodo
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                # solta o click do mouse
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # cria possiveis movimentos
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        # valida o movimento
                        if board.valid_move(dragger.piece, move):
                            # captura normal
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)

                            # som
                            game.play_sound(captured)

                            # mostra o metodo
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)

                            # muda o jogador
                            game.next_turn()

                    dragger.undrag_piece()

                # tecla pressionada
                elif event.type == pygame.KEYDOWN:
                    
                    # troca o tema
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # reinicia o jogo
                    if event.key == pygame.K_r:
                        game.reset()

                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                
                # fechar a janela
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


main = Main()
main.mainloop()
