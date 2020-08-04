def conv2dto1d(r, c, wide):
    """
    2次元座標を1次元座標に変換する関数
    
    Parameters
    ----------
    r : int 
        行
    c : int
        列
    wide : int
        幅
    
    
    Returns
    -------
    r * size + c : int
        変換した1次元座標
    """
    return r * wide + c

def conv1dto2d(idx, wide):
    """
    1次元座標を2次元座標に変換する関数
    
    Parameters
    ----------
    idx : int
        1次元座標
    
    Returns
    -------
    (row, col) : tuple(int, int)
        2次元座標
    """
    return (int(idx / wide), idx % wide)