import os
from copy import deepcopy
from abc import ABC, abstractmethod

class ChessPiece(ABC):
    def __init__(self, is_white):
        self.is_white = is_white

    @abstractmethod
    def get_valid_moves(self, field, start_row, start_col):
        pass

    def __str__(self):
        name = self.__class__.__name__
        return name[0].upper() if self.is_white else name[0].lower()

class King(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = start_row + dr, start_col + dc
                if 0 <= r < 8 and 0 <= c < 8 and (field[r][c] == '.' or field[r][c].is_white != self.is_white):
                    moves.append((r, c))
        return moves

class Queen(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
    
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if field[r][c] == '.':
                    moves.append((r, c))
                elif field[r][c].is_white != self.is_white:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves

class Bishop(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if field[r][c] == '.':
                    moves.append((r, c))
                elif field[r][c].is_white != self.is_white:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves

class Knight(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        directions = [(-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1)]
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (field[r][c] == '.' or field[r][c].is_white != self.is_white):
                moves.append((r, c))
        return moves

class Rook(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if field[r][c] == '.':
                    moves.append((r, c))
                elif field[r][c].is_white != self.is_white:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        return moves

class Pawn(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.first_move = True
        self.last_move_double = False

    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        direction = 1 if self.is_white else -1
        r, c = start_row + direction, start_col
        
        if 0 <= r < 8 and field[r][c] == '.':
            moves.append((r, c))
            double_r = start_row + 2 * direction
            if self.first_move and 0 <= double_r < 8 and field[double_r][c] == '.':
                moves.append((double_r, c))
        
        for dc in [-1, 1]:
            r, c = start_row + direction, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8 and field[r][c] != '.' and field[r][c].is_white != self.is_white:
                moves.append((r, c))
        
        if (self.is_white and start_row == 4) or (not self.is_white and start_row == 3):
            for dc in [-1, 1]:
                c = start_col + dc
                if 0 <= c < 8 and isinstance(field[start_row][c], Pawn) and field[start_row][c].is_white != self.is_white and field[start_row][c].last_move_double:
                    moves.append((start_row + direction, c))
        
        return moves

    def move(self, field, start_row, start_col, end_row, end_col):
        if abs(end_row - start_row) == 2:
            self.last_move_double = True
        else:
            self.last_move_double = False
        self.first_move = False
        
        if (self.is_white and end_row == 7) or (not self.is_white and end_row == 0):
            choice = input("Выберите фигуру для превращения (Queen/Rook/Bishop/Knight): ").capitalize()
            return globals()[choice](self.is_white)
        return self

class Wizard(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.moves_since_teleport = 3

    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if field[r][c] == '.':
                    moves.append((r, c))
                elif field[r][c].is_white != self.is_white:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        
        if self.moves_since_teleport >= 3:
            for r in range(8):
                for c in range(8):
                    if field[r][c] == '.':
                        moves.append((r, c))
        return moves

    def move(self, field, start_row, start_col, end_row, end_col):
        if abs(end_row - start_row) > 2 or abs(end_col - start_col) > 2:
            self.moves_since_teleport = 0
        else:
            self.moves_since_teleport += 1
        return self

class Archer(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        king_directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dr, dc in king_directions:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8 and (field[r][c] == '.' or field[r][c].is_white != self.is_white):
                moves.append((r, c))
        
        attack_directions = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]
        for dr, dc in attack_directions:
            r, c = start_row + dr, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8 and field[r][c] != '.' and field[r][c].is_white != self.is_white:
                moves.append((r, c))
        return moves

    def move(self, field, start_row, start_col, end_row, end_col):
        distance_row = abs(end_row - start_row)
        distance_col = abs(end_col - start_col)
        if distance_row <= 1 and distance_col <= 1:
            return self
        else:
            field[end_row][end_col] = '.'
            return self

class Thunderer(ChessPiece):
    def __init__(self, is_white):
        super().__init__(is_white)
        self.moves_since_thunder = 4

    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            r, c = start_row + dr, start_col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if field[r][c] == '.':
                    moves.append((r, c))
                elif field[r][c].is_white != self.is_white:
                    moves.append((r, c))
                    break
                else:
                    break
                r, c = r + dr, c + dc
        
        if self.moves_since_thunder >= 4:
            thunder_directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            for dr, dc in thunder_directions:
                r, c = start_row + dr, start_col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    moves.append((r, c))
        return moves

    def move(self, field, start_row, start_col, end_row, end_col):
        if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1 and self.moves_since_thunder >= 4:
            thunder_directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            for dr, dc in thunder_directions:
                r, c = start_row + dr, start_col + dc
                if 0 <= r < 8 and 0 <= c < 8 and field[r][c] != '.' and field[r][c].is_white != self.is_white:
                    field[r][c] = '.'
            self.moves_since_thunder = 0
        else:
            self.moves_since_thunder += 1
        return self

class Checker(ChessPiece):
    def get_valid_moves(self, field, start_row, start_col):
        moves = []
        direction = 1 if self.is_white else -1
        for dc in [-1, 1]:
            r, c = start_row + direction, start_col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if field[r][c] == '.':
                    moves.append((r, c))
                elif field[r][c].is_white != self.is_white and 0 <= r + direction < 8 and 0 <= c + dc < 8 and field[r + direction][c + dc] == '.':
                    moves.append((r + direction, c + dc))
        return moves

start_field_classic = [
    [Rook(True), Knight(True), Bishop(True), Queen(True), King(True), Bishop(True), Knight(True), Rook(True)],
    [Pawn(True) for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    [Pawn(False) for _ in range(8)],
    [Rook(False), Knight(False), Bishop(False), Queen(False), King(False), Bishop(False), Knight(False), Rook(False)]
]

start_field_custom = [
    [Wizard(True), Archer(True), Bishop(True), Queen(True), King(True), Bishop(True), Thunderer(True), Rook(True)],
    [Pawn(True) for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    [Pawn(False) for _ in range(8)],
    [Wizard(False), Archer(False), Bishop(False), Queen(False), King(False), Bishop(False), Thunderer(False), Rook(False)]
]

start_field_checkers = [
    [Checker(True) if i % 2 == 1 else '.' for i in range(8)],
    ['.' if i % 2 == 1 else Checker(True) for i in range(8)],
    [Checker(True) if i % 2 == 1 else '.' for i in range(8)],
    ['.' for _ in range(8)],
    ['.' for _ in range(8)],
    ['.' if i % 2 == 1 else Checker(False) for i in range(8)],
    [Checker(False) if i % 2 == 1 else '.' for i in range(8)],
    ['.' if i % 2 == 1 else Checker(False) for i in range(8)],
]

def print_field(field, threatened=None):
    threatened = threatened or set()
    letters_coords = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    nums_coords = [i for i in range(1, 9)]
    print('    ', *letters_coords, sep=' ', end='\n\n')
    for i in range(len(field)):
        print(nums_coords[i], end='    ')
        for j in range(8):
            if (i, j) in threatened:
                print(f'[{field[i][j]}]', end=' ')
            else:
                print(f'{field[i][j]}', end=' ')
        print('  ', nums_coords[i])
    print('\n    ', *letters_coords, sep=' ')

def get_threatened_pieces(field, is_white_turn):
    threatened = set()
    king_pos = None
    for r in range(8):
        for c in range(8):
            if field[r][c] != '.' and field[r][c].is_white == is_white_turn:
                moves = field[r][c].get_valid_moves(field, r, c)
                for move_r, move_c in moves:
                    if field[move_r][move_c] != '.' and field[move_r][move_c].is_white != is_white_turn:
                        threatened.add((move_r, move_c))
                        if isinstance(field[move_r][move_c], King):
                            king_pos = (move_r, move_c)
                    elif isinstance(field[r][c], Checker) and abs(move_r - r) == 2 and abs(move_c - c) == 2:
                        mid_r = (r + move_r) // 2
                        mid_c = (c + move_c) // 2
                        if field[mid_r][mid_c] != '.' and field[mid_r][mid_c].is_white != is_white_turn:
                            threatened.add((mid_r, mid_c))
    return threatened, king_pos

def rollback_fun(rollback, field, start_field, file_name='step_notation.txt'):
    with open(file_name) as file:
        lines = file.readlines()
        if len(lines) <= rollback:
            return deepcopy(start_field)
        new_field = deepcopy(start_field)
        for line in lines[:-rollback]:
            pass
    return new_field

def main_game_loop(start_field):
    field = deepcopy(start_field)
    game_on = True
    step_player_white = True
    letter_to_num_dict = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    num_to_letter_dict = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    count_steps = 0
    step_notation = ''
    try:
        os.remove('step_notation.txt')
    except:
        pass

    print('Команды:')
    print('"откат" - откатить ходы')
    print('"нотация" - прочитать нотацию')
    print('"stop" - вернуться в меню')
    print('"угрозы" - показать угрожаемые фигуры')

    while game_on:
        threatened, king_pos = get_threatened_pieces(field, step_player_white)
        print_field(field)
        if king_pos:
            print("Ваш король под шахом!")

        with open('step_notation.txt', 'a') as file:
            if step_player_white and count_steps != 0:
                file.write(step_notation + '\n')
                step_notation = f'{count_steps + 1}. '
            elif not step_player_white:
                file.write(step_notation + ' ')

        step_coord_figure = input(f'\nВведите координату {"белой" if step_player_white else "черной"} фигуры: ')
        step_coord_figure = step_coord_figure.strip('"')
        if step_coord_figure == 'stop':
            return True
        if step_coord_figure == 'угрозы':
            threatened, king_pos = get_threatened_pieces(field, step_player_white)
            print_field(field, threatened)
            if threatened:
                threatened_coords = [f"{num_to_letter_dict[c]}{r + 1}" for r, c in threatened]
                print(f"Фигура под боем: {', '.join(threatened_coords)}")
            else:
                print("Нет фигур под боем.")
            continue
        if step_coord_figure == 'откат':
            rollback = int(input('На сколько ходов откатить? '))
            field = rollback_fun(rollback, field, start_field)
            count_steps -= rollback
            continue

        step_coord_figure_go = input('Введите координату хода: ')
        try:
            start_col = letter_to_num_dict[step_coord_figure[0].lower()] - 1
            start_row = int(step_coord_figure[1]) - 1
            end_col = letter_to_num_dict[step_coord_figure_go[0].lower()] - 1
            end_row = int(step_coord_figure_go[1]) - 1

            if field[start_row][start_col] == '.':
                print('Там нет фигуры!')
                continue
            if field[start_row][start_col].is_white != step_player_white:
                print('Это не ваша фигура!')
                continue
            
            moves = field[start_row][start_col].get_valid_moves(field, start_row, start_col)
            if (end_row, end_col) not in moves:
                print('Недопустимый ход!')
                continue

            if isinstance(field[start_row][start_col], Checker) and abs(end_row - start_row) == 2:
                mid_row = (start_row + end_row) // 2
                mid_col = (start_col + end_col) // 2
                field[mid_row][mid_col] = '.'
                field[end_row][end_col] = field[start_row][start_col]
                field[start_row][start_col] = '.'
            elif isinstance(field[start_row][start_col], Archer):
                field[start_row][start_col] = field[start_row][start_col].move(field, start_row, start_col, end_row, end_col)
                distance_row = abs(end_row - start_row)
                distance_col = abs(end_col - start_col)
                if distance_row <= 1 and distance_col <= 1:
                    field[end_row][end_col] = field[start_row][start_col]
                    field[start_row][start_col] = '.'
            elif isinstance(field[start_row][start_col], Thunderer):
                field[start_row][start_col] = field[start_row][start_col].move(field, start_row, start_col, end_row, end_col)
                if abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1:
                    continue
                else:
                    field[end_row][end_col] = field[start_row][start_col]
                    field[start_row][start_col] = '.'
            else:
                if isinstance(field[start_row][start_col], Pawn) and abs(start_col - end_col) == 1 and field[end_row][end_col] == '.':
                    field[start_row][end_col] = '.'
                piece = field[start_row][start_col].move(field, start_row, start_col, end_row, end_col) if hasattr(field[start_row][start_col], 'move') else field[start_row][start_col]
                field[end_row][end_col] = piece
                field[start_row][start_col] = '.'

            step_notation += f'{field[end_row][end_col]}{step_coord_figure}-{step_coord_figure_go}'
            step_player_white = not step_player_white
            count_steps += 1 if step_player_white else 0

            if isinstance(field[end_row][end_col], King):
                print_field(field)
                print(f'{"Белые" if not step_player_white else "Черные"} выиграли!')
                game_on = False

        except (KeyError, ValueError, IndexError):
            print('Некорректный ввод!')
            continue

    return False

while True:
    print("\nВыберите игру:")
    print("1 - Классические шахматы")
    print("2 - Шахматы с новыми фигурами")
    print("3 - Шашки")
    choice = input("Ваш выбор (1-3): ")
    
    if choice == '1':
        print("\nВы выбрали Классические шахматы.")
        print("Белые фигуры: R (ладья), N (конь), B (слон), Q (королева), K (король), P (пешка)")
        print("Черные фигуры: r (ладья), n (конь), b (слон), q (королева), k (король), p (пешка)")
        main_game_loop(start_field_classic)
    elif choice == '2':
        print("\nВы выбрали Шахматы с новыми фигурами.")
        print("Белые фигуры: W (волшебник), A (лучник), B (слон), Q (королева), K (король), T (громовержец), R (ладья), P (пешка)")
        print("Черные фигуры: w (волшебник), a (лучник), b (слон), q (королева), k (король), t (громовержец), r (ладья), p (пешка)")
        print("\nОписание новых фигур:")
        print("1. Волшебник (W/w):")
        print("   - Ходит как слон (по диагонали на любое расстояние), но раз в 3 хода может телепортироваться на любую свободную клетку.")
        print("   - После телепортации счетчик сбрасывается, после обычного хода увеличивается на 1.")
        print("   - Телепортация доступна, если счетчик >= 3.")
        print("2. Лучник (A/a):")
        print("   - Может перемещаться на 1 клетку в любом направлении, как король (вверх, вниз, влево, вправо и по диагоналям).")
        print("   - Также может атаковать фигуры противника на расстоянии 2 клеток в любом направлении (по прямой или диагонали), оставаясь на месте.")
        print("3. Громовержец (T/t):")
        print("   - Ходит как ладья (по горизонтали или вертикали на любое расстояние).")
        print("   - Раз в 4 хода может вызвать 'удар грома', атакуя все соседние клетки (8 клеток вокруг), уничтожая фигуры противника, но не перемещаясь.")
        print("   - После 'удара грома' счетчик сбрасывается, после обычного хода увеличивается на 1.")
        print("   - 'Удар грома' доступен, если счетчик >= 4.")
        main_game_loop(start_field_custom)
    elif choice == '3':
        print("\nВы выбрали Шашки.")
        print("Белые фигуры: C (шашка)")
        print("Черные фигуры: c (шашка)")
        main_game_loop(start_field_checkers)
    else:
        print("Неверный выбор!")