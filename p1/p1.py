import pandas as pd

file_path = 'concepts.csv'


# depth first search
def csv2json_helper(df, row, col):
    '''
    Helper function used to transform matrix to dictionary
    :param df:
    :param row:
    :param col:
    :return:
    '''
    if col == df.shape[1] - 1:
        res = dict()
        res[df[col][row]] = []
        return res, row + 1
    res = dict()
    res[df[col][row]] = []
    tmp, row_new = csv2json_helper(df, row, col + 1)
    res[df[col][row]].append(tmp)
    while row_new < df.shape[0] and pd.isnull(df.iloc[row_new,col]):
        tmp, row_new = csv2json_helper(df, row_new, col + 1)
        res[df[col][row]].append(tmp)
    return res, row_new


def csv2json(file_path):
    try:
        note_df = pd.read_csv(file_path, header=None)
        res, row = csv2json_helper(note_df, 0, 0)
        del note_df
        return res
    except:
        print('{} is empty'.format(file_path))
    

def find_helper(data, res, target):
    '''
    Helper function used to search the target from data.
    :param data:
    :param res:
    :param target:
    :return:
    '''
    # depth first search
    for key, values in data.items():
        if key == target:
            res.append(key)
            return True
        if len(values) == 0:
            return False
        else:
            for value in values:
                if find_helper(value, res, target):
                    res.append(key)
                    return True
            return False


def find(key):
    try:
        ref_data = csv2json(file_path)
        res = []
        if find_helper(ref_data, res, key):
            res.reverse()
            return '.'.join(res)
        else:
            return '不存在关键字：{}'.format(key)
    except:
        print('文档不存在或者文档读取错误')
        return None
