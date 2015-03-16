# -*- coding:utf-8 -*-
import os


def check_folder_file(folder_path):
    """
    检测保存结果时目录路径和文件是否存在，目录不存在时创建目录，文件存在时先删除
    :param folder_path:目录路径
    :return:Null
    """
    # 检验目标文件夹是否存在，不存在则创建
    if os.path.exists(folder_path):
        pass
    else:
        os.makedirs(folder_path)


def store_json(file_name, dict_name, folder_path=None):
    """
    将字典写入json文件
    :param file_name:文件名称
    :param dict_name:字典名称
    :param folder_path:保存文件路径，默认为None时为当前执行目录
    :return:Null
    """
    # 检查file_name是否包含json后缀名
    if '.json' not in file_name:
        file_name += '.json'
    full_path = os.path.join(folder_path, file_name)
    with open(full_path, 'w') as mf:
        import json
        mf.write(json.dumps(dict_name))


def read_json(file_path):
    """
    从指定路径读取json文件
    :param file_path:包含文件名的路径名称
    :return:解析后的json对象
    """
    if os.path.exists(file_path):
        import json
        with open(file_path, 'r') as mf:
            r = json.loads(mf.read())
    else:
        r = None

    return r