import discord
from discord.ext import commands
from discord.commands import Option
##############################################2048
loc2048={
    0:"<:blank:1063777142577573898>",
    2:"<:2_:1063776226633850880>",
    4:"<:4_:1063776228265435177>",
    8:"<:8_:1063776231222411354>",
    16:"<:16:1063776233063727146>",
    32:"<:32:1063776236582744075>",
    64:"<:64:1063776238742818857>",
    128:"<:128:1063776241724952707>",
    256:"<:256:1063776244824547372>",
    512:"<:512:1063776247194341499>",
    1024:"<:1024:1063776223215493171>",
    2048:"<:2048:1063776250985979924>"
}
def draw_board(board): #繪製棋盤
    s=""
    for dx in range(4):
        for dy in range(4):
            s+=loc2048[board[dx][dy]]
        s+='\n'
    return s
def check_2048(board,now_block_quan):#True為結束，False還沒結束
    if now_block_quan==16:
        for x in range(4):
            for y in range(4):
                now=board[x][y]
                if x==0:
                    if y==0:
                        if now==board[x+1][y] or now==board[x][y+1]:
                            return False
                    elif y==4-1:
                        if now==board[x+1][y] or now==board[x][y-1]:
                            return False
                    else:
                        if now==board[x+1][y] or now==board[x][y-1] or now==board[x][y+1]:
                            return False
                elif y==0:
                    if x==4-1:
                        if now==board[x-1][y] or now==board[x][y+1]:
                            return False
                    else:
                        if now==board[x][y+1] or now==board[x-1][y] or now==board[x+1][y]:
                            return False
                elif x==4-1:
                    if y==4-1:
                        if now==board[x-1][y] or now==board[x][y-1]:
                            return False
                        else:
                            if now==board[x][y-1] or now==board[x][y+1] or now==board[x-1][y]:
                                return False
                elif y==4-1:
                    if now==board[x][y-1] or now==board[x-1][y] or now==board[x+1][y]:
                        return False
                else:
                    if now==board[x-1][y] or now==board[x+1][y] or now==board[x][y-1] or now==board[x][y+1]:
                        return False
        return True
def is_zero(w:int,board,row):#判斷是否全部擠過去1右2左3上4下，不是為true
    if w == 1:
        ii=0
        for jnd in range(4):
            if jnd<=2 and board[row][jnd]==board[row][jnd+1] and board[row][jnd]!=0:
                return True
            if board[row][jnd] != 0:
                ii = 1
            if ii == 1 and board[row][jnd] == 0:
                return True
        return False
    elif w == 2:
        ii = 0
        for jnd in range(3, -1, -1):
            if jnd>=1 and board[row][jnd]==board[row][jnd-1] and board[row][jnd]!=0:
                return True
            if board[row][jnd] != 0:
                ii = 1
            if ii == 1 and board[row][jnd] == 0:
                return True
        return False
    elif w == 3:
        ii = 0
        for jnd in range(3, -1, -1):
            if jnd>=1 and board[jnd][row]==board[jnd-1][row] and board[jnd][row]!=0:
                return True
            if board[jnd][row] != 0:
                ii = 1
            if ii == 1 and board[jnd][row] == 0:
                return True
        return False
    elif w == 4:
        ii = 0
        for jnd in range(4):
            if jnd<=2 and board[jnd][row]==board[jnd+1][row] and board[jnd][row]!=0:
                return True
            if board[jnd][row] != 0:
                ii = 1
            if ii == 1 and board[jnd][row] == 0:
                return True
        return False
##############################################2048
##############################################OOXX
def check_OOXX_win(ba,now): #檢查輸贏，false為贏
    if ba[0]==ba[1] and ba[1]==ba[2]:
        return False
    elif ba[3]==ba[4] and ba[4]==ba[5]:
        return False
    elif ba[6]==ba[7] and ba[7]==ba[8]:
        return False
    elif ba[0]==ba[4] and ba[4]==ba[8]:
        return False
    elif ba[2]==ba[4] and ba[4]==ba[6]:
        return False
    elif ba[0]==ba[3] and ba[3]==ba[6]:
        return False
    elif ba[1]==ba[4] and ba[4]==ba[7]:
        return False
    elif ba[2]==ba[5] and ba[5]==ba[8]:
        return False
    return True
def draw(board): #繪製盤面，回傳需要輸出的字串
    search={1:":one:",2:":two:",3:":three:",4:":four:",5:":five:",6:":six:",7:":seven:",8:":eight:",9:":nine:",10:':o:',11:':x:'}
    s=search[board[0]]+search[board[1]]+search[board[2]]+'\n'+search[board[3]]+search[board[4]]+search[board[5]]+'\n'+search[board[6]]+search[board[7]]+search[board[8]]
    return s
##############################################OOXX
##############################################五子棋
def check_chess_win(chess,ChessBoard):#判斷輸贏(傳入目前哪方)
    for i in range(8):
        for j in range(8):
            if ChessBoard[i][j] == chess:
                try:
                    if ChessBoard[i][j] == ChessBoard[i][j+1]==ChessBoard[i][j+2]==ChessBoard[i][j+3]==ChessBoard[i][j+4]:
                        return True
                    elif ChessBoard[i][j] == ChessBoard[i+1][j]==ChessBoard[i+2][j]==ChessBoard[i+3][j]==ChessBoard[i+4][j]:
                        return True
                    elif ChessBoard[i][j] == ChessBoard[i+1][j+1]==ChessBoard[i+2][j+2]==ChessBoard[i+3][j+3]==ChessBoard[i+4][j+4]:
                        return True
                    elif ChessBoard[i][j] == ChessBoard[i-1][j+1]==ChessBoard[i-2][j+2]==ChessBoard[i-3][j+3]==ChessBoard[i-4][j+4]:
                        return True
                except:
                    print()
    return False
##############################################五子棋
##############################################大聲公_modal

