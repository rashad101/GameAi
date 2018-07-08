import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import time

GAMEARENAHEIGHT = 19 # Height of the Board
GAMEARENAWIDTH = 19 # Width of the Board

DEPTH = 3 # Depth value to search

# relate numbers (1, -1, 0) to symbols ('X', 'O', ' ')
symbols = {1:'X', -1:'O', 0:' '}

def main():

    histogram, statistics, histm = playgame()
    histm = histm[histm[:,0].argsort()]
    
    plothistogram(2, histogram, 'Random Games')
    plt.figure(3)
    sns.heatmap(statistics, linewidth=0.5, cmap = "plasma", annot = True,color = 'red')
    plt.figure(4)
    plt.bar(histm[:,0], histm[:,1],color='green')
    plt.xticks(histm[:,0])
    plt.yticks(histm[:,1])
    plt.show()

# Helper Function to make random moves.....
def playgame():
    histogram = np.zeros(3)
    win_1 = 0
    win_2 = 0
    tie = 0
    gameWins = np.zeros((GAMEARENAHEIGHT,GAMEARENAWIDTH), dtype=int)

    start_time = time.time()

    hist_move = np.empty((0,2), dtype = int)
    f= open("output.txt","w+")
    for i in range(1000):
        
        # initialize player number, move counter
        player = 1
        mvcntr = 1
        
        # initialize 6x7 connect4 board
        Board =  np.zeros((GAMEARENAHEIGHT,GAMEARENAWIDTH), dtype=int)
        
        # initialize flag that indicates win
        noWinnerYet = True

        while move_still_possible(Board) and noWinnerYet:
            
            if player == 1:
                # let player move at random
                row, col = move_at_random(Board, player)                
            else:
                bm = np.empty((0, 2), dtype = int)
                won = False
                for col in range(GAMEARENAWIDTH):
                    row = getLowestEmptySpace(Board, col)
                    if row >= 0:
                        tempBoard = Board.copy()
                        tempBoard[row, col] = player
                        if move_was_winning_move(tempBoard, player, row, col):
                            won = True
                            break
                        else:                    
                            _, val = backtrack(Board.copy(), col, player, 0)
                            if val == None:
                                continue
                            else:
                                bm = np.append(bm, np.array([[col,val]]), axis = 0)
                if won == False:
                    min_val = np.amin(bm, axis = 0)[1]
                    bm = bm[bm[:,1] == min_val]
                    col = np.random.choice(bm[:,0])
                    row = getLowestEmptySpace(Board, col)

                Board[row, col] = player

            # print current game state
            # print_game_state(Board)
            # print('============================================')
            
            # evaluate game state
            if move_was_winning_move(Board, player, row, col):
                f.write("%d %s %d\n" % ((i+1),symbols[player],mvcntr))
                print ('Game No %d ::: player %s wins after %d moves \n' % (i+1, symbols[player], mvcntr))
                print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                noWinnerYet = False
                Board[Board != player] = 0
                Board *= player
                gameWins += Board
                if player == 1:
                    win_1 += 1
                else:
                    win_2 += 1
            elif move_still_possible(Board):
                # switch player and increase move counter
                player *= -1
                mvcntr +=  1

        if noWinnerYet:
            print ('Game no %d ended in a draw' %(i+1))
            tie += 1

        index = np.where(hist_move[:,0] == mvcntr)[0]
        if index.size > 0:
            hist_move[index, 1] += 1
        else:
            hist_move = np.append(hist_move, np.array([[mvcntr, 1]]), axis = 0)
    
    end_time = time.time()
    time_diff = end_time - start_time
    minutes = int(time_diff/60)
    seconds = int(time_diff%60)

    print ("Total time taken is " + str(minutes) + " minutes and " + "{:.2f}".format(seconds) + " seconds")
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('player 1 wins  %d time(s)' % (win_1))
    print('player 2 wins  %d time(s)' % (win_2))
    print('Game tied  %d time(s)' % (tie))
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    gameWinsPercent = np.around(gameWins*1.0/(win_1 + win_2),3)
    print(gameWinsPercent)

    histogram[0] = win_1
    histogram[1] = win_2
    histogram[2] = tie

    return histogram, gameWinsPercent, hist_move

# Function to search heuristically till a defined depth, till 
def backtrack(board, col, player, curr_depth):
    # tempBoard = board.copy()

    row = getLowestEmptySpace(board, col)
    if row >= 0:
        board[row, col] = player
    else:
        # tempBoard = None
        return col, None
    
    if move_was_winning_move(board, player, row, col):
        # board = None
        return col, player * 100
    else:
        player *= -1
        bm = np.empty((0, 2), dtype = int)
        if curr_depth < DEPTH and move_still_possible(board):
            for c in range(GAMEARENAWIDTH):
                r = getLowestEmptySpace(board, c)
                if r > -1:
                    _, val = backtrack(board.copy(), c, player, curr_depth + 1)
                    if val == None:
                        continue
                    else:
                        bm = np.append(bm, np.array([[c, val]]), axis = 0)
            if player == 1:
                max_val = np.amax(bm, axis = 0)[1]
                bm = bm[bm[:,1] == max_val]
                best_col = np.random.choice(bm[:,0])
                return best_col, max_val
            else:
                min_val = np.amin(bm, axis = 0)[1]
                bm = bm[bm[:,1] == min_val]
                best_col = np.random.choice(bm[:,0])
                return best_col, min_val

        return col, 0

# Helper Function to get a possible move
def getLowestEmptySpace(board, column):
    # Return the row number of the lowest empty row in the given column.
    row = np.where(board[:,column] == 0)[0]
    if row.size > 0:
        return np.max(row)
    else:
        return -1

# Helper Function to check if board is full or not
def move_still_possible(board):
    return not (board[board==0].size == 0)

# Helper Function to make random move
def move_at_random(board, p):
    xs = np.zeros((0,0), dtype = int)
    ys = np.zeros((0,0), dtype = int)
    for i in range(GAMEARENAWIDTH):
        row = getLowestEmptySpace(board, i)
        if row >= 0 and row < GAMEARENAHEIGHT:
            xs = np.append(xs, row)
            ys = np.append(ys,i)

    i = np.random.permutation(np.arange(xs.size))[0]
    
    board[xs[i],ys[i]] = p

    return xs[i], ys[i]

def check_vertical(board, curr_r, curr_c, p):
    index = curr_r
    counter = 0
    for i in range(4):
        if board[index, curr_c] == p:
            counter += 1
        else:
            break
        index += 1
    return counter

def check_horizontal(board, curr_r, curr_c, p):
    direction = -1
    counter = 0
    index = curr_c
    for i in range(6):
        if index >= 0 and index < GAMEARENAWIDTH and board[curr_r, index] == p:
            counter += 1
        else:
            if direction == -1:
                direction = 1
                index = curr_c
            else:
                break
        if counter == 4:
            break
        index += direction    
    return counter

# Helper Function to check winning move along diagonal
def check_diagonal(board, curr_r, curr_c, direction_r, direction_c, p):
    index_r = curr_r
    index_c = curr_c
    counter = 0
    for i in range(6):
        if index_r >= 0 and index_c >= 0 and index_r < GAMEARENAHEIGHT and index_c < GAMEARENAWIDTH and board[index_r,index_c] == p:
            counter += 1
        else:
            if direction_r == -1:
                direction_r = 1
                direction_c *= -1
                index_r = curr_r
                index_c = curr_c
            else:
                break
        if counter == 4:
            # return True
            break

        index_r += direction_r
        index_c += direction_c
    
    # return False
    return counter

# Helper Function to check winning move
def move_was_winning_move(board, p, curr_r, curr_c):

    # Check vertical
    if GAMEARENAHEIGHT - curr_r > 3 and check_vertical(board, curr_r, curr_c, p) == 4:
        return True

    # Check Horizontal
    if check_horizontal(board, curr_r, curr_c, p) == 4:
        return True

    # Check Left Diagonal
    if check_diagonal(board, curr_r, curr_c, -1, -1, p) == 4:
        return True
    # Check Right Diagonal
    elif check_diagonal(board, curr_r, curr_c, -1, 1, p) == 4:
        return True

    return False

# # Helper Function to print Board matrix using symbols
def print_game_state(board):
    B = np.copy(board).astype(object)
    for n in [-1, 0, 1]:
        B[B==n] = symbols[n]
    print('[\'|1|\' \'|2|\' \'|3|\' \'|4|\' \'|5|\' \'|6|\' \'|7|\']')
    for val in B:
        print('|' + val + '|')

def plothistogram(fig_id, hist, title):
    x = [0, 1, 2]
    plt.figure(fig_id)
    plt.bar(x, hist,color='red')
    
    plt.xticks(x, ('player 1', 'player 2', 'draws'))
    plt.title(title)
    plt.text(x[0], hist[0]/2, hist[0])    
    plt.text(x[1], hist[1]/2, hist[1])
    plt.text(x[2], hist[2]/2, hist[2])


if __name__ == '__main__':
    main()