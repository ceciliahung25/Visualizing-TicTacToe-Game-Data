# cli.py

import csv
import os
from datetime import datetime
from logic import Board, RandomBot

def print_board(board):
    for i, row in enumerate(board.grid):
        print(f"{i} | {' | '.join(cell if cell is not None else ' ' for cell in row)} |")
    print("   0   1   2")

def choose_player_type():
    while True:
        choice = input("Choose player type (1 for Human, 2 for RandomBot): ")
        if choice == '1':
            return 'X', 'Human'
        elif choice == '2':
            return 'O', 'RandomBot'
        else:
            print("Invalid choice. Please enter 1 or 2.")

# 新增的函数，用于写入游戏数据到 CSV 文件
def write_game_log(player_type, player_symbol, move_count, winner):
    log_file_path = 'logs/game_log.csv'

    # 如果文件不存在，创建文件并写入标题
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Player Type', 'Player Symbol', 'Move Count', 'Winner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # 将当前游戏数据写入文件
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 添加检查是否已经有了获胜者，避免重复写入
    if winner and winner != "Draw":
        with open(log_file_path, 'a', newline='') as csvfile:
            fieldnames = ['Timestamp', 'Player Type', 'Player Symbol', 'Move Count', 'Winner']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'Timestamp': timestamp,
                'Player Type': player_type,
                'Player Symbol': player_symbol,
                'Move Count': move_count,
                'Winner': winner
            })

def main():
    board = Board()
    player_symbol, player_type = choose_player_type()

    # 重置 move_count
    move_count = 0

    while True:
        print_board(board)
        print(f"{player_type} Player {player_symbol}'s turn.")

        if player_type == 'Human':
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
        else:
            bot = RandomBot(player_symbol)
            move = bot.get_move(board)
            row, col = move

        if 0 <= row < 3 and 0 <= col < 3:
            if board.grid[row][col] is not None:
                print("That cell is already occupied! Try again.")
                continue

            board.grid[row][col] = player_symbol
            move_count += 1
            winner = board.get_winner()
            if winner:
                print_board(board)
                print(f"{player_type} Player {player_symbol} wins!")

                # 仅在游戏开始时写入一次
                if move_count == 1:
                    write_game_log(player_type, player_symbol, move_count, player_symbol)
                break

            elif all(cell is not None for row in board.grid for cell in row):
                print_board(board)
                print("It's a draw!")

                # 仅在游戏开始时写入一次
                if move_count == 1:
                    write_game_log(player_type, player_symbol, move_count, "Draw")
                break

            else:
                player_symbol = board.other_player(player_symbol)

        else:
            print("Invalid input! Row and column must be 0, 1, or 2.")

if __name__ == '__main__':
    main()
