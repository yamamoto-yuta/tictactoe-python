import numpy as np

class TictactoeEnv:
    def __init__(self, board_size=3, first_player=-1):
        """
        コンストラクタ
        
        Parameters
        ----------
        board_size ; int
            ボードのサイズ
        first_player : str
            先攻のプレーヤ
            -1(X) か 1(O) を指定
        """
        # 定数
        self.BOARD_SIZE = board_size
        self.O_ID = 1
        self.E_ID = 0
        self.X_ID = -1
        
        # 初期化
        self.board = None
        self.first_player = first_player
        self.current_player = None
        self.result = None
        self.reset()
        
    def reset(self):
        """
        ゲームを初期化する関数
        """
        self.board = np.zeros(9, dtype=np.int32)
        self.current_player = self.first_player
        
    def put(self, index):
        """
        OXを置く関数
        
        Parameters
        ----------
        index : int
            置く座標
            
        Returns
        -------
        index : int
            置いた座標
        is_fin : bool
            勝敗が着いたかどうか
        info : {'x_win': bool, 'o_win': bool, 'is_full': bool}
            勝敗の情報
        valid : bool
            ちゃんと置けたかどうか
        """
        # OXを置く
        if self.board[index] != self.E_ID:
            # その座標にもうすでにOXが置かれている場合
            return None, None, False
        elif self.current_player == self.X_ID:
            # 現在のプレーヤがXの場合
            self.board[index] = self.X_ID
            self.current_player = self.O_ID
        else:
            # 現在のプレーヤがOの場合
            self.board[index] = self.O_ID
            self.current_player = self.X_ID
        
        # 勝敗を判定
        is_fin, info = self.judge()
        
        return index, is_fin, info, True
    
    
    def judge(self):
        """
        ゲームの勝敗を判定する関数
        
        Returns
        -------
        is_fin : bool
            決着が着いたかどうか
        {
            x_win : bool
                Xが勝ったかどうか
            o_win : bool
                Oが勝ったかどうか
            is_full : bool
                ボードが全て埋まったかどうか
        }
        """
        x_win, o_win, is_full = False, False, False
        
        # 縦と横を調べる
        for i in range(self.BOARD_SIZE):
            row = self.board[(i * self.BOARD_SIZE) : (i * self.BOARD_SIZE + self.BOARD_SIZE)]
            col = self.board[i::self.BOARD_SIZE]
            if np.sum(row) == self.BOARD_SIZE or np.sum(col) == self.BOARD_SIZE:
                o_win = True
            if np.sum(row) == -self.BOARD_SIZE or np.sum(col) == -self.BOARD_SIZE:
                x_win = True
        
        
        # 斜めを調べる
        board = self.board.reshape(3, 3)
        if np.diag(board).sum() == self.BOARD_SIZE or np.diag(np.fliplr(board)).sum() == self.BOARD_SIZE:
            o_win = True
        if np.diag(board).sum() == -self.BOARD_SIZE or np.diag(np.fliplr(board)).sum() == -self.BOARD_SIZE:
            x_win = True
            
        # ボードが全て埋まっているか調べる
        if self.E_ID not in self.board:
            is_full = True
            
        # 決着が着いたかどうか調べる
        is_fin = x_win or o_win or is_full
        
        return is_fin, {'x_win': x_win, 'o_win': o_win, 'is_full': is_full}