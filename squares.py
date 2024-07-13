import pygame as pg
from rules import is_valid_move, is_check

class Squares:
    def __init__(self, root):
        self.root = root
        self.positions = {
            "a1": "W_ROOK", "a2": "W_PAWN", "a3": None, "a4": None, "a5": None, "a6": None, "a7": "pawn", "a8": "rook",
            "b1": "W_KNIGHT", "b2": "W_PAWN", "b3": None, "b4": None, "b5": None, "b6": None, "b7": "pawn", "b8": "knight",
            "c1": "W_BISHOP", "c2": "W_PAWN", "c3": None, "c4": None, "c5": None, "c6": None, "c7": "pawn", "c8": "bishop",
            "d1": "W_QUEEN", "d2": "W_PAWN", "d3": None, "d4": None, "d5": None, "d6": None, "d7": "pawn", "d8": "queen",
            "e1": "W_KING", "e2": "W_PAWN", "e3": None, "e4": None, "e5": None, "e6": None, "e7": "pawn", "e8": "king",
            "f1": "W_BISHOP", "f2": "W_PAWN", "f3": None, "f4": None, "f5": None, "f6": None, "f7": "pawn", "f8": "bishop",
            "g1": "W_KNIGHT", "g2": "W_PAWN", "g3": None, "g4": None, "g5": None, "g6": None, "g7": "pawn", "g8": "knight",
            "h1": "W_ROOK", "h2": "W_PAWN", "h3": None, "h4": None, "h5": None, "h6": None, "h7": "pawn", "h8": "rook"
        }
        self.font = pg.font.Font(None, 36)
        self.selected_piece = None
        self.selected_piece_pos = None
        self.move_history = []
        self.turn = 'WHITE'  # Beyaz başlar

    def drawBoard(self):
        square_size = 100
        for row in range(8):
            for col in range(8):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                pg.draw.rect(self.root, color, (col * square_size, row * square_size, square_size, square_size))

                file = chr(col + ord('a'))
                rank = str(8 - row)
                position = file + rank
                piece = self.positions.get(position)
                if piece and (position != self.selected_piece_pos):
                    piece_color = (255, 0, 0) if piece.isupper() else (0, 0, 255)
                    png = pg.image.load(f'assets/{piece}.png')  # Taş resmi yükleniyor
                    png = pg.transform.scale(png, (100, 100))  # Resmi boyutlandırma
                    self.root.blit(png, (col * square_size, row * square_size))  # Taşı çizmek için resim yüzeyini ekrana kopyala

        if self.selected_piece:
            mouse_x, mouse_y = pg.mouse.get_pos()
            self.root.blit(pg.image.load(f'assets/{self.selected_piece}.png'), (mouse_x - 50, mouse_y - 50))  # Seçilen taşı fare konumuna göre çiz

    def selectPiece(self, x, y):
        file = chr(x // 100 + ord('a'))
        rank = str(8 - y // 100)
        self.selected_piece_pos = file + rank
        self.selected_piece = self.positions.get(self.selected_piece_pos)

        # Sadece geçerli oyuncunun taşını seçebilmesi için kontrol ekleyelim
        if self.selected_piece and (
                (self.turn == 'WHITE' and self.selected_piece.islower()) or
                (self.turn == 'BLACK' and self.selected_piece.isupper())):
            self.selected_piece = None
            self.selected_piece_pos = None

    def movePiece(self, x, y):
        if not self.selected_piece:
            return

        file = chr(x // 100 + ord('a'))
        rank = str(8 - y // 100)
        new_pos = file + rank

        if is_valid_move(self.selected_piece, self.selected_piece_pos, new_pos, self.positions):
            old_pos = self.selected_piece_pos
            old_piece = self.positions.get(new_pos)
            self.positions[new_pos] = self.selected_piece
            self.positions[self.selected_piece_pos] = None
            self.selected_piece = None
            self.selected_piece_pos = None

            if is_check(self.turn == 'WHITE', self.positions):
                # Şah kontrolü, hamleyi geri al
                self.positions[old_pos] = self.positions[new_pos]
                self.positions[new_pos] = old_piece
                print("Geçersiz hamle: Şah tehdit altında")
            else:
                self.move_history.append((old_pos, new_pos, old_piece))
                self.turn = 'BLACK' if self.turn == 'WHITE' else 'WHITE'
        else:
            self.selected_piece = None
            self.selected_piece_pos = None

    def undoMove(self):
        if not self.move_history:
            return

        last_move = self.move_history.pop()
        old_pos, new_pos, captured_piece = last_move

        self.positions[old_pos] = self.positions[new_pos]
        self.positions[new_pos] = captured_piece

        self.turn = 'BLACK' if self.turn == 'WHITE' else 'WHITE'
