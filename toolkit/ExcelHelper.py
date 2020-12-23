import traceback
from datetime import datetime

import xlrd


class ExcelHelper:
    """需要确定excelName和sheetIndex, 只能处理单个sheet"""

    def __init__(self, file_name, sheet_index=0):
        self.book = xlrd.open_workbook(file_name)
        self.sheet = self.book.sheet_by_index(sheet_index)
        pass

    def getAllSheets(self):
        sheetList = self.book.sheet_names()
        return sheetList
        pass

    def readOneRow(self, row: int = 0):
        """得到一行的内容"""
        rowContents = self.sheet.row(row)
        return rowContents
        pass

    def readOneColumn(self, column: int = 0):
        """得到一列的内容"""
        columnContents = self.sheet.col(column)
        return columnContents
        pass

    def readOneCell(self, row: int, column: int):
        """
        返回一个单元格的内容

        :param row: cells num
        :param column: column num
        :return: 一个cell
        """
        cell = self.sheet.cell(row, column)
        return cell
        pass

    def readAllRows(self, need_header=False):
        """
        得到row_list, 其中row是一行内容的list

        :param need_header: 是否读取第一行(通常是表头而不是内容)
        :returns: row_list, 默认不包含列头
        """

        sheet = self.sheet
        row_list = []
        for row in range(sheet.nrows):
            if row == 0 and (not need_header):
                continue  # 列头不加入此list
            else:
                row_content = []
                column_num = sheet.ncols
                for column in range(column_num):
                    cell_value = sheet.cell(row, column).value
                    if isinstance(cell_value, str):
                        cell_value = str(cell_value).strip()  # 去除左右两侧的空白
                    row_content.append(cell_value)
                row_list.append(row_content)
        return row_list

    def findTableHeader_row(self, cellContent):
        """
        根据cellContent的内容, 返回内容所在的行

        :param cellContent: 单元格的内容
        :return: row_no: int 错误则返回-1
        """
        rows = self.sheet.get_rows()
        find_out_flag = -1  # 记录是否找到对应的行
        row_no = 0
        for row in rows:
            if not row:
                continue
            if row[0].value == cellContent:
                return row_no

            row_no += 1
        return find_out_flag
        pass

    def readOneTableAll(self, the_start_row, the_end_row):
        """得到[the_start_row, the_end_row)之间(包括头, 去掉尾)的所有row_list"""
        sheet = self.sheet
        row_list = []
        for row in range(the_start_row, the_end_row):
            row_content = []
            column_num = sheet.ncols
            for column in range(column_num):
                cell_value = sheet.cell(row, column).value
                if isinstance(cell_value, str):
                    cell_value = cell_value.strip()  # 去除string左右两侧的空白
                    pass
                row_content.append(cell_value)
            row_list.append(row_content)

        return row_list
        pass

    def readOneTable_2Column(self, header_row, row_list, useless_rows):
        """
        得到一个sheet中的一张表的内容, 处理仅有2列的表

        :param useless_rows: 无用的行内容, 没有对应的值
        :param header_row: 表头的所在行数
        :param row_list: 需要填的项的list
        :return: row_list对应的value_list, 即对应的值的list
        """
        content_start_row = header_row + 1
        content_end_row = header_row + len(row_list) + len(useless_rows)
        result_list = []
        for row in range(content_start_row, content_end_row + 1):
            first_column_value = str(self.sheet.cell(row, 0).value).strip()
            if first_column_value in useless_rows:  # 如果开头就是无用的列, 则跳过这一行
                continue
                pass

            row_content = []
            for column in range(self.sheet.ncols):
                cell_value = self.sheet.cell(row, column).value
                cell_value = str(cell_value).strip()
                if cell_value != '':
                    row_content.append(cell_value)
                pass
            try:
                result_list.append(row_content[1])  # 2列的表, 其第二列是结果
            except IndexError:
                traceback.print_exc()
                print(row)
            pass
        return result_list
        pass


class SheetHelper:
    """在调用ExcelHelper之前需要知道sheetName"""

    @staticmethod
    def getSheetNames(excelName):
        book = xlrd.open_workbook(excelName)
        sheetList = book.sheet_names()
        return sheetList

    pass


if __name__ == '__main__':
    pass
