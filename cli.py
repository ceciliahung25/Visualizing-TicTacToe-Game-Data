# cli.py

import csv
import os
from logic import Board, RandomBot

def print_board(board):
    for i, row in enumerate(board.grid):
        print(f"{i} | {' | '.join(cell if cell is not None else ' ' for cell in row)} |")
    print("   0   1   2")

def choose_player_type():
    while True:
        choice = input("Choose player type (1 for Human, 2 for RandomBot): ")
        if choice == '1':
            return 'X'
        elif choice == '2':
            return 'O'
        else:
            print("Invalid choice. Please enter 1 or 2.")

def main():
    board = Board()
    player = choose_player_type()

    while True:
        print_board(board)
        print(f"Player {player}'s turn.")

        if player == 'X':
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
        else:
            bot = RandomBot(player)
            move = bot.get_move(board)
            row, col = move

        if 0 <= row < 3 and 0 <= col < 3:
            if board.grid[row][col] is not None:
                print("That cell is already occupied! Try again.")
                continue

            board.grid[row][col] = player
            winner = board.get_winner()
            if winner:
                print_board(board)
                print(f"Player {winner} wins!")

                # Record winner in log file
                record_winner(winner)
                break
            elif all(cell is not None for row in board.grid for cell in row):
                print_board(board)
                print("It's a draw!")
                break
            else:
                player = board.other_player(player)
        else:
            print("Invalid input! Row and column must be 0, 1, or 2.")

def record_winner(player):
    log_file_path = 'logs/game_log.csv'
    log_exists = os.path.exists(log_file_path)

    with open(log_file_path, 'a', newline='') as csvfile:
        fieldnames = ['Player', 'Result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the log file doesn't exist, write the header
        if not log_exists:
            writer.writeheader()

        # Write winner data to the log file
        writer.writerow({'Player': player, 'Result': 'Win'})

if __name__ == '__main__':
    main()
