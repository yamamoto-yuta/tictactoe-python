import numpy as np
from copy import deepcopy
from keras.models import load_model
import tictactoe_env

def cpu(env, model):
    # 自分が勝てる確率の閾値
    TH_PRED_P_WIN = 0.05
    
    # おけるマスの座標をリストアップ
    can_put_idx = [idx for idx, cell in enumerate(env.board) if cell == env.E_ID]
    
    # 置けるパターンを全て格納
    pred_boards = []
    for idx in can_put_idx:
        board = deepcopy(env.board)
        board[idx] = env.current_player
        pred_boards.append(board)
    pred_boards = np.array(pred_boards)

    # 各パターンで勝敗の確率を計算
    pred = model.predict(pred_boards)
    
    # 自分が一番勝てる確率と敵が一番負ける確率が高いパターンをそれぞれ決定
    # - (x, -, y) = (-1, 0, 1) に+1して添字に利用
    pred_p_id = env.current_player + 1
    pred_e_id = -env.current_player + 1
    best_p_win_pred = np.argmax([p[pred_p_id] for p in pred])
    best_e_lose_pred = np.argmax([p[pred_e_id] for p in pred])
    
    # パターンを決定
    if pred_p_id >= TH_PRED_P_WIN:
        # 自分が一番勝てる確率が閾値以上ならそうする
        best_pred = best_p_win_pred
    else:
        # 閾値未満なら、敵が一番負けるようにする
        best_pred = best_e_lose_pred
    
    # 決定したパターンで置く座標を返す
    return can_put_idx[best_pred]