from enum import Enum
import random
import copy


player_quit = False


class Tiles(Enum):
    EMPTY = '.'
    X = 'X'
    O = 'O'


class EndStates(Enum):
    X_wins = 'X'
    O_wins = 'O'
    In_progress = 'In_progress'
    Tie = 'Tie'


winner = EndStates.In_progress


def create_board():

    size_of_row = 3
    size_of_column = 3

    board = []

    for row in range(size_of_row):

        new_row = []

        for column in range(size_of_column):
            new_row.append(Tiles.EMPTY)

        board.append(new_row)

    return board


def print_board(board):

    for tile in board:
        print(tile[0].value + ' ' + tile[1].value + ' ' + tile[2].value)

    print('')


def check_invalid_input(player_input, board):

    error_message = 'Error invalid input. '
    incorrect_format_message = 'Incorrect Format. '
    try_again_message = 'Please Try Again.'
    valid = False

    if len(player_input) != 3:
        print(error_message+incorrect_format_message+try_again_message)
        return False

    if not str.isdigit(player_input[0]) or player_input[1]!= ' ' or not str.isdigit(player_input[2]):
        valid = False
        print(error_message+incorrect_format_message+try_again_message)
        return False

    if 1 <= int(player_input[0]) <= 3 and 1 <= int(player_input[2]) <= 3:
        valid = True
        if not check_valid_move(int(player_input[0]), int(player_input[2]), board):
            print(error_message + 'Please pick an empty spot. ' + try_again_message)
            valid = False
    else:
        print(error_message+'Row and column must be between 1 and 3. ' + try_again_message)
        valid = False

    if not valid:
        return False

    else:
        return True


def check_valid_move(row, col, board):

    if board[row-1][col-1] != Tiles.EMPTY:
        return False
    else:
        return True


def place_o(row, col, board):

    board[row - 1][col - 1] = Tiles.O
    print_board(board)


def AI_place_o(row, col, board):

    board[row - 1][col - 1] = Tiles.O


def place_x(row, col, board):

    board[row-1][col-1] = Tiles.X
    print_board(board)


def AI_place_x(row, col, board):

    board[row-1][col-1] = Tiles.X


def get_x_move(board):

    global winner

    prompt = 'X\'s turn. Enter your move'
    player_move = input(prompt)

    while not check_invalid_input(player_move, board):
        player_move = input(prompt)

    row = int(player_move[0])
    col = int(player_move[2])
    place_x(row, col, board)
    winner = check_if_game_over(board)


def get_o_move(board):

    global winner
    prompt = 'O\'s turn. Enter your move'
    player_move = input(prompt)

    while not check_invalid_input(player_move, board):
        player_move = input(prompt)

    row = int(player_move[0])
    col = int(player_move[2])
    place_o(row, col, board)
    winner = check_if_game_over(board)


def check_if_game_over(board):

    current_game_winner = EndStates.In_progress

    if check_if_x_won(board):
        current_game_winner = EndStates.X_wins

    elif check_if_o_won(board):
        current_game_winner = EndStates.O_wins

    elif check_tie(board):
        current_game_winner = EndStates.Tie

    return current_game_winner


def check_if_x_won(board):
    tile = Tiles.X

    if check_rows_(board, tile) or check_columns(board, tile) or check_diagonals(board, tile):
        return True
    else:
        return False


def check_if_o_won(board):
    tile = Tiles.O

    if check_rows_(board, tile) or check_columns(board, tile) or check_diagonals(board, tile):
        return True
    else:
        return False


def check_tie(board):

    for row in board:

        if Tiles.EMPTY in row:
            return False

    return True


def check_rows_(board, tile):

    for row in board:

        if row[0] == tile and row[1] == tile and row[2] == tile:
            return True

    return False


def check_columns(board, tile):

    length_board = 3
    for num in range(length_board):

        if board[0][num] == tile and board[1][num] == tile and board[2][num] == tile:
            return True

    return False


def check_diagonals(board, tile):

    length_board = 3
    top_left_to_bottom_right = True
    top_right_to_bottom_left = True
    for num in range(length_board):

        if board[num][num] != tile:
            top_left_to_bottom_right = False

    for num in range(length_board):

        if board[num][2-num] != tile:
            top_right_to_bottom_left = False

    if top_right_to_bottom_left or top_left_to_bottom_right:
        return True
    else:
        return False


def get_random_move(board):
    possible_moves = get_possible_moves(board)
    random_move = random.choice(possible_moves)

    return random_move


def play_out_a_game(board, move):

    temp_board = copy.deepcopy(board)
    AI_place_o(move[0], move[1], temp_board)
    temp_winner = check_if_game_over(temp_board)

    while temp_winner == EndStates.In_progress:
        random_x_move = get_random_move(temp_board)
        AI_place_x(random_x_move[0], random_x_move[1], temp_board)
        temp_winner = check_if_game_over(temp_board)

        if temp_winner == EndStates.In_progress:

            random_o_move = get_random_move(temp_board)
            AI_place_o(random_o_move[0], random_o_move[1], temp_board)
            temp_winner = check_if_game_over(temp_board)

    if temp_winner == EndStates.O_wins or temp_winner == EndStates.Tie:
        return True
    else:
        return False


def pure_monte_carlo_AI(board, play_outs):
    global winner
    temp_board = copy.deepcopy(board)
    possible_moves = get_possible_moves(temp_board)
    num_play_outs = play_outs

    wins_or_ties = []

    for move in possible_moves:
        num_wins_or_ties = 0

        for play_out in range(num_play_outs):

            if play_out_a_game(temp_board, move):
                num_wins_or_ties += 1

        wins_or_ties.append(num_wins_or_ties)

    AI_move = possible_moves[wins_or_ties.index((max(wins_or_ties)))]

    row = AI_move[0]
    col = AI_move[1]

    print('O\'s turn. Computer placed O at ' + str(row) + ' ' + str(col))

    place_o(row, col, board)
    winner = check_if_game_over(board)


def get_moves(board):

    num_play_outs = 45
    if winner == EndStates.In_progress:
        pure_monte_carlo_AI(board, num_play_outs)

    if winner == EndStates.In_progress:

        get_x_move(board)


def print_game_over():

    global winner

    print('Game Over!')
    if winner == EndStates.X_wins:
        print('X Wins!')
    elif winner == EndStates.O_wins:
        print('O Wins!')
    elif winner == EndStates.Tie:
        print('Tie!')


def ask_if_player_wants_to_play_again():
    global player_quit
    global winner
    valid_input = False
    prompt = 'Do you want to play again? (y/n)'
    error_message = 'Invalid input, please enter y or n'

    while not valid_input:
        player_input = input(prompt)

        if player_input == 'n':
            player_quit = True
            valid_input = True

        elif player_input == 'y':
            player_quit = False
            valid_input = True
            winner = EndStates.In_progress
        else:
            print(error_message)


def get_possible_moves(board):

    possible__moves = []

    for i in range(len(board)):
        for j in range(len(board)):

            current_tile = board[i][j]
            current_index = [i+1, j+1]
            if current_tile == Tiles.EMPTY:
                possible__moves.append(current_index)

    return possible__moves


def display_intro():
    print('Welcome to the Monte Carlo Tic Tac Toe Game!')
    print('Choose a position on the board in the format of row# col#')
    print('For example if I wanted to place my tile at row 2 column 3, I would type in \'2 3\''
          ' (no spaces before or after)')
    print('Good luck!\n')


def play_game():

    global winner
    board = create_board()
    print_board(board)

    while winner == EndStates.In_progress:

        get_moves(board)

    print_game_over()
    ask_if_player_wants_to_play_again()


display_intro()

while not player_quit:
    play_game()

