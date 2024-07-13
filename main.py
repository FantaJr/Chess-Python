import pygame as pg
from squares import Squares

def main():
    pg.init()
    screen = pg.display.set_mode((800, 800))
    pg.display.set_caption("Chess")

    clock = pg.time.Clock()
    squares = Squares(screen)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tuş
                    if squares.selected_piece:
                        squares.movePiece(event.pos[0], event.pos[1])
                    else:
                        squares.selectPiece(event.pos[0], event.pos[1])
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_u:  # Geri alma tuşu
                    squares.undoMove()

        screen.fill((0, 0, 0))
        squares.drawBoard()
        pg.display.flip()
        clock.tick(144)

    pg.quit()

if __name__ == "__main__":
    main()
