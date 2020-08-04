import PySimpleGUI as sg
from keras.models import load_model
import tictactoe_env
import cpu
import utils

def show_result():
    """
    勝敗を文字列に直して返す関数
    
    Returns
    -------
    - : str
        勝敗を示す文字列
    """
    if info['x_win']:
        return 'Xの勝ちです'
    elif info['o_win']:
        return 'Oの勝ちです'
    else:
        return '引き分けです'
    
# 学習済みモデルを読み込み
model = load_model('../train/my_model.h5')
# OXゲームクラスをインスタンス化
env = tictactoe_env.TictactoeEnv()

# レイアウトとウィンドウの生成
img_e = './img/-.png'
img_o = './img/o.png'
img_x = './img/x.png'

layout =  [
    [sg.Button('', 
               size=(1,1), 
               key=(i,j), 
               pad=(0,0),
               image_filename=img_e,
               image_size=(1,1),
               image_subsample=4,
              ) for j in range(env.BOARD_SIZE)] for i in range(env.BOARD_SIZE)
]

window = sg.Window('AI×OXゲーム', layout)

# イベントループ
while True:
    event, values = window.read()

    # ウィンドウを閉じる
    if event is None:
        print('exit')
        break
    
    print(event, values)
    
    # プレーヤのターン
    index, is_fin, info, valid = env.put(utils.conv2dto1d(event[0], event[1], env.BOARD_SIZE))
    if not valid:
        sg.popup('すでに置かれています！')
        continue
    window[event].update('', image_filename=img_x, image_size=(1,1), image_subsample=4)
    
    print(env.board.reshape(3, 3))
    print(info)
    
    if is_fin:
        sg.popup(show_result(), custom_text=('もう一回'), title='対戦結果')
        env = tictactoe_env.TictactoeEnv()
        [window[utils.conv1dto2d(i, env.BOARD_SIZE)].update('', image_filename=img_e, image_size=(1,1), image_subsample=4) for i in range(env.BOARD_SIZE * env.BOARD_SIZE)]
        continue
        
    # CPUのターン
    index, is_fin, info, valid = env.put(cpu.cpu(env, model))
    window[utils.conv1dto2d(index, env.BOARD_SIZE)].update('',
                                                           image_filename=img_o,
                                                           image_size=(1,1),
                                                           image_subsample=4
                                                          )
    
    print(env.board.reshape(3, 3))
    print(info)
    
    if is_fin:
        sg.popup(show_result(), custom_text=('もう一回'), title='対戦結果')
        env = tictactoe_env.TictactoeEnv()
        [window[utils.conv1dto2d(i, env.BOARD_SIZE)].update('', image_filename=img_e, image_size=(1,1), image_subsample=4) for i in range(env.BOARD_SIZE * env.BOARD_SIZE)]
        continue
    
# ウィンドウの破棄と終了
window.close()
