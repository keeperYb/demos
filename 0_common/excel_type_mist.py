import xlrd
from toolkit.ExcelHelper import ExcelHelper

VALUE_ERROR_FLAG = -404


def getValueFromExcel_playground():
    the_excel_file = r'C:\Users\xuyb\Desktop\excel\playground.xlsx'
    the_sheet_index = 1
    excel_helper = ExcelHelper(the_excel_file, the_sheet_index)
    all_content = excel_helper.readAllRows(need_header=True)
    for row in all_content:
        for cell in row:
            # 强制转化为int, 再转为str  why cell in row is NOT changed??
            cell_index = row.index(cell)
            try:
                row[cell_index] = (int(cell))  # 先int化,在str化
            except ValueError:  # 转换错误
                row[cell_index] = VALUE_ERROR_FLAG
            # the_cell = row[cell_index]
            # the_cell =
            pass
    pass


def changeListValue():
    """尝试改变一个list中的值, 用for循环的方式"""
    list_of_int = [1, 1, 3]
    # for one_int in list_of_int:
    #     index = list_of_int.index(one_int)
    #     list_of_int[index] = one_int + 0
    #     pass
    for i in range(len(list_of_int)):
        list_of_int[i] = str(list_of_int[i])
        pass
    print(list_of_int)
    pass


if __name__ == '__main__':
    # changeListValue()
    getValueFromExcel_playground()
    pass
