def is_check(white_turn, positions):
    king_pos = None
    king_color = 'WHITE' if white_turn else 'BLACK'

    # Şahın pozisyonunu bulalım
    for pos, piece in positions.items():
        if piece and ((piece == 'KING' and white_turn and piece.isupper()) or (piece == 'king' and not white_turn and piece.islower())):
            king_pos = pos
            break

    if not king_pos:
        return False

    opponent_color = 'BLACK' if white_turn else 'WHITE'
    # Karşı takımın tüm taşlarını kontrol edelim
    for pos, piece in positions.items():
        if piece and ((piece.isupper() and not white_turn) or (piece.islower() and white_turn)):  # Karşı takımın taşı
            if is_valid_move(piece, pos, king_pos, positions):
                return True

    return False

def is_checkmate(king_color, positions):
    # Mat durumu kontrolü
    for pos, current_piece in positions.items():
        if current_piece and ((king_color == 'WHITE' and current_piece.isupper()) or (king_color == 'BLACK' and current_piece.islower())):
            for new_pos in positions.keys():
                if is_valid_move(current_piece, pos, new_pos, positions):
                    old_piece = positions[new_pos]
                    positions[new_pos] = current_piece
                    positions[pos] = None
                    if not is_check(king_color == 'WHITE', positions):
                        positions[new_pos] = old_piece
                        positions[pos] = current_piece
                        return False
                    positions[new_pos] = old_piece
                    positions[pos] = current_piece
    print("checkmate")
    return True

def is_starting_move(piece, start_pos, end_pos, positions):
    start_col, start_row = ord(start_pos[0]), int(start_pos[1])
    end_col, end_row = ord(end_pos[0]), int(end_pos[1])
    
    if piece.isupper():
        # Beyaz piyonlar
        if start_row == 2 and end_row == 4 and positions.get(chr(start_col) + '3') is None and positions.get(end_pos) is None:
            return True
        elif start_row + 1 == end_row and positions.get(end_pos) is None:
            return True
    else:
        # Siyah piyonlar
        if start_row == 7 and end_row == 5 and positions.get(chr(start_col) + '6') is None and positions.get(end_pos) is None:
            return True
        elif start_row - 1 == end_row and positions.get(end_pos) is None:
            return True
    
    return False

def is_valid_move(piece, start_pos, end_pos, positions):
    if start_pos == end_pos:
        return False

    start_col, start_row = ord(start_pos[0]), int(start_pos[1])
    end_col, end_row = ord(end_pos[0]), int(end_pos[1])
    if piece.upper() == 'W_PAWN':
        direction = 1
        # Piyonun düz hareketi
        if start_col == end_col and end_row - start_row == direction and positions.get(end_pos) is None:
            return True
        # Piyonun başlangıç hareketi
        if start_col == end_col and end_row - start_row == 2 * direction and (start_row == 2 or start_row == 7) and positions.get(end_pos) is None:
            return is_starting_move(piece, start_pos, end_pos, positions)
        # Piyonun çapraz yeme hareketi
        if abs(start_col - end_col) == 1 and end_row - start_row == direction and positions.get(end_pos) is not None:
            return True

    elif piece.lower() == 'pawn':
        direction = -1
        # Piyonun düz hareketi
        if start_col == end_col and end_row - start_row == direction and positions.get(end_pos) is None:
            return True
        # Piyonun başlangıç hareketi
        if start_col == end_col and end_row - start_row == 2 * direction and (start_row == 2 or start_row == 7) and positions.get(end_pos) is None:
            return is_starting_move(piece, start_pos, end_pos, positions)
        # Piyonun çapraz yeme hareketi
        if abs(start_col - end_col) == 1 and end_row - start_row == direction and positions.get(end_pos) is not None:
            return True
    elif piece.lower() == 'rook' or piece.upper() == 'W_ROOK':
        if start_col == end_col or start_row == end_row:
            if is_path_clear(start_pos, end_pos, positions):
                return True
    elif piece.lower() == 'knight' or piece.upper() == 'W_KNIGHT':
        if (abs(start_col - end_col), abs(start_row - end_row)) in [(1, 2), (2, 1)]:
            return True
    elif piece.lower() == 'bishop' or piece.upper() == 'W_BISHOP':
        if abs(start_col - end_col) == abs(start_row - end_row):
            if is_path_clear(start_pos, end_pos, positions):
                return True
    elif piece.lower() == 'queen' or piece.upper() == 'W_QUEEN':
        if start_col == end_col or start_row == end_row or abs(start_col - end_col) == abs(start_row - end_row):
            if is_path_clear(start_pos, end_pos, positions):
                return True
    elif piece.lower() == 'king' or piece.upper() == 'W_KING':
        if max(abs(start_col - end_col), abs(start_row - end_row)) == 1:
            return True

    return False

def is_path_clear(start_pos, end_pos, positions):
    start_col, start_row = ord(start_pos[0]), int(start_pos[1])
    end_col, end_row = ord(end_pos[0]), int(end_pos[1])

    step_col = 0 if start_col == end_col else 1 if end_col > start_col else -1
    step_row = 0 if start_row == end_row else 1 if end_row > start_row else -1

    col, row = start_col + step_col, start_row + step_row
    while col != end_col or row != end_row:
        if positions.get(chr(col) + str(row)) is not None:
            return False
        col += step_col
        row += step_row

    return True
