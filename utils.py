"""
Utility functions used in chess_game
"""

def translate(x,y):
    """Function to turn numpy coordinates into chess board coordinates

    Args:
        x (int): Vertical position on board (1-8)
        y (int): Horizontal position on board (1-8)

    Returns:
        str: Chess board coordinate in traditional format (ex. 'A4')
    """
    y_translation = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f',6:'g',7:'h'}
    return str(y_translation[y]) + str(x + 1)

def detranslate(movestring):
    """
    Function to turn traditional chess board coordinates into numpy coordinates

    Args:
        movestring (str): traditional chess board cooridnate (ex. 'A4')

    Returns:
        list: numpy coordinates of chess board position 
    """
    y_translation = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f',6:'g',7:'h'}
    y_detranslation = {v: k for k, v in y_translation.items()} 
    x = int(movestring[1]) - 1  
    y = int(y_detranslation[movestring[0]]) 
    return [x,y]

def empty_board():
    """Creates empty chess board
    Returns:
        np array [8,8]: All empty type objects
    """
    Board =  Board = np.full([8,8], E)
    return Board

def pawn_promote():
    """
    Checks if any pawns are eligable for promotion. 
    If a pawn has reached the opponent's back row the function executes the kill method 
    on that pawn and revives a dormant queen in that pawn's y position.
    """
    
    #Pawn promotion dictionary
    promdict = {'W_aPQ':W_aPQ, 'W_bPQ':W_bPQ, 'W_cPQ':W_cPQ, 'W_dPQ':W_dPQ, 'W_ePQ':W_ePQ, 'W_fPQ':W_fPQ, 
            'W_gPQ':W_gPQ, 'W_hPQ':W_hPQ, 'B_aPQ':B_aPQ, 'B_bPQ':B_bPQ, 'B_cPQ':B_cPQ, 'B_dPQ':B_dPQ,
            'B_ePQ':W_ePQ, 'B_fPQ':W_fPQ,'B_gPQ':W_gPQ, 'B_hPQ':W_hPQ}
    
    for i in pawns:
        
        if i.team =='W':
            if i.x == 7:
                curry = i.y
                i.kill()
                promdict['W_' + y_translation[curry] + 'PQ'].revive()
                Board[0,curry] = promdict['W_' + y_translation[curry] + 'PQ']
                
        if i.team =='B':
             if i.x == 0:
                 curry = i.y
                 i.kill()
                 promdict['B_' + y_translation[curry] + 'PQ'].revive()
                 Board[0,curry] = promdict['B_' + y_translation[curry] + 'PQ']
                 
def buildteams():
    """
    Builds arrays for both teams with all pieces in their starting positions 

    Returns:
        np.array [16, 1]: two numpy arrays, one for each team
    """
    
    startpos = {W_a : [1,0], W_b : [1,1], W_c : [1,2], W_d : [1,3], W_e : [1,4], W_f : [1,5], W_g : [1,6], W_h : [1,7],
         W_Ra : [0,0], W_Nb : [0,1], W_Bc : [0,2], W_Qd : [0,3], W_Ke : [0,4], W_Bf : [0,5], W_Ng : [0,6], W_Rh : [0,7],
         B_a : [6,0], B_b : [6,1], B_c : [6,2], B_d : [6,3], B_e : [6,4], B_f : [6,5], B_g : [6,6], B_h : [6,7],
         B_Ra : [7,0], B_Nb : [7,1], B_Bc : [7,2], B_Qd : [7,3], B_Ke : [7,4], B_Bf : [7,5], B_Ng : [7,6], B_Rh : [7,7],
         W_aPQ: [],  W_bPQ: [],  W_cPQ: [],  W_dPQ: [],  W_ePQ: [],  W_fPQ: [],  W_gPQ: [],  W_hPQ: [],
         B_aPQ: [],  B_bPQ: [],  B_cPQ: [],  B_dPQ: [],  B_ePQ: [],  B_fPQ: [],  B_gPQ: [],  B_hPQ: []}

    white = []
    black = []

    for i in list(startpos.keys()):
        if i.alive == True:     
            if i.team == 'W':
                white =  np.append(white,i)
            if i.team == 'B':
                black = np.append(black,i)

    return white, black

def brd():
    """
    Displays the board with the piece's symbols.

    Returns:
        np array [8,8]: Current status of board
    """
    white, black = buildteams()
        
    board_status = np.full([8,8], '[]')
    
    for i in white:
        board_status[i.x, i.y] = 'W' + i.symbol 
        
    for j in black:
        board_status[j.x, j.y] = 'B' + j.symbol 
        
    return board_status

def kill_moves(team):
    """
    Finds all moves that can place a king in check. Basically just removes the pawns attacking forward.

    Args:
        team (str): 'W' for white or 'B' for black

    Returns:
        np.array [possible moves, 1]: Array of all possible moves for the next turn that can place the king in check 
    """
    killmoves = []
    for i in startpos:
        if i.alive == True :
            if i.team == team:
                for m in i.allowedmoves():
                    killmoves.append(m)
                     
    if len(killmoves) > 0:
        for j in pawns:
            if j.alive == True:
                if j.team == team:
                    for k in j.allowedmoves():
                        if y_detranslation[k[0]] == j.y:
                            if k in killmoves:
                                killmoves.remove(k)
    
    return killmoves

def checkforcheck(team):
    """
    Determines if the given team is currently in check by analyzing the oppenent's next possible moves

    Args:
        team (str): 'W' for white or 'B' for black  
    """
    W_Ke.check = False
    B_Ke.check = False 
    
    if team == 'W':
        if translate(W_Ke.x,W_Ke.y) in kill_moves('B'):
            W_Ke.check = True  
        
    if team == 'B':
        if translate(B_Ke.x,B_Ke.y) in kill_moves('W'):
            B_Ke.check = True
            
def all_moves(team):
    """
    Finds all moves avaialble to team on the next turn 

    Args:
        team (str): 'W' for white or 'B' for black  

    Returns:
        set: All possible moves for the next turn in the format "piece position"
    """
    allmoves ={}
    
    for i in startpos:
            if i.alive == True:
                if i.team == team:
                    allmoves[i.symbol + " " + i.status()] = i.possmoves()    
    return allmoves

def checkformate():
    """
    Checks to see if either team is in checkmate by determining if they have any possible moves that 
    do not result in the team still being in check 
    """
    white, black = buildteams()
    
    wnummoves = 0
    bnummoves = 0
    
    for i in white:
        wnummoves += len(i.allowedmoves())

    for j in black:
        bnummoves += len(j.allowedmoves())
        
    if wnummoves == 0:
        W_Ke.mate = True 
    if bnummoves == 0:
        B_Ke.mate = True 
        
def reset():
    """
    Resets the game to the originally starting position.
    """
    Board = empty_board()
    
    for i in list(startpos.keys())[32:]:
        i.kill()
        
    for i in list(startpos.keys())[:32]:
        i.revive()
        i.testmove(startpos[i][0],startpos[i][1])
        i.startpos = True 
        i.check = False
        i.mate = False
        
def random_move(team):
    """
    Chooses a random move from the list of possible moves for a given team and board position

    Args:
        team (str): 'W' for white, 'B' for black

    Returns:
        piece.symbol: Interpretable symbol of piece that is chosen to move
        curpos: Starting position of the piece
        piece.status: Position for piece to move to
    """
    white, black = buildteams()
    
    pos = []
    while len(pos) == 0:
        if team == 'W':
            piece = random.choice(white)
            piece.allowedmoves()
            pos = piece.poss
        else:
            piece = random.choice(black)
            piece.allowedmoves()
            pos = piece.poss
            
    currpos = piece.status()
    
    randmove = random.choice(pos)
    
    piece.move(randmove)
    
    return piece.symbol, currpos, piece.status()