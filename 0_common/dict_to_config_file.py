dict_number_four = {
    'number': 4,
    'english': 'four',
    'simplified_chinese': '四'
}


class DictNumber:
    number = 0
    english = ''
    simplified_chinese = ''

    def __init__(self, dict_number: dict):
        for key in dict_number.keys():
            setattr(self, key, dict_number[key])
        pass

    pass


if __name__ == '__main__':
    # 通过xls表格自动生成DictNumber类的对象num_obj
    num_obj_4 = DictNumber(dict_number_four)
    print(num_obj_4.simplified_chinese)
    # 将num_obj存入一个json格式的文件中
    pass
