"""拖拽各小节的界面设计, 生成list"""
from enum import Enum

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QMenu, QAction, QTreeWidgetItem

import sys
import os

# for cmd searching path
from UI.MyTreeWidget import MyTreeWidget

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from UI.drag_drop_treewidget_UI import Ui_MainWindow

# todo total view
"""
drag drop的策略:
- 顶层只有一级标题可放  OK
- 一个级数的标题只能放到对应-1级的标题的子树中 OK
- 标题号根据每一个命名空间来自动判定, 但是标题号格式不要写死 OK
- 同一个节点层中,有可能有相同的标题, 但是在不同的命名空间中,可以有相同的标题 TODO
    - 为SectionObj添加 can_have_multiple 属性
- 加多级(至少三级)的页面, 编号要能够自动按1.1.1. ...向下排 

todo now
"""
section_list = []
DATA_ROLE = 1
DATA_COLUMN = 0  # the column where treeWidget stores data
TEXT_COLUMN = 0


# class section_obj:
#     """obj for the smallest word section, will be saved into TreeWidgetItem afterwards"""
#
#     def __init__(self, para_dict: dict):
#         """
#         initiate the section_obj
#         :param para_dict: a dict that stores the parameters which object-initiation needs
#         """
#         self.section_lv = 0  # 章节的级别, 包括1级, 2级...
#         self.elements_list = []
#
#         for key in para_dict.keys():
#             setattr(self, key, para_dict[key])
#         pass
#
#     pass


class SectionObj:
    """a model class, simulating one Word section"""

    def __init__(self, raw_dict: dict):
        self.name = ''
        self.level = 0  # need an enum
        self.section_no = 0  # stores the section_num, the num_namespace is set in parent_section
        self.can_have_multiple = False  # used to check if one tree can have multiple same-name items
        self.desc = ''  # some description of the section

        for key in raw_dict.keys():
            setattr(self, key, raw_dict[key])
            pass
        pass

    pass


class SectionLvEnum(Enum):
    LV1 = 1
    LV2 = 2
    LV3 = 3
    pass


class SectionFactory:
    """from where we get fruit_obj"""

    @staticmethod
    def getFreeFruits():
        """return some fruits """
        section_dict_list = [
            {'name': '第一部分', 'level': SectionLvEnum.LV1, 'can_have_multiple': False, 'desc': '第一部分desc'},
            {'name': '第二部分', 'level': SectionLvEnum.LV1, 'can_have_multiple': False, 'desc': '第二部分desc'},
            {'name': '第x部分', 'level': SectionLvEnum.LV1, 'can_have_multiple': False, 'desc': '第x部分desc'},
            {'name': '小节1', 'level': SectionLvEnum.LV2, 'can_have_multiple': False, 'desc': '小节1_desc'},
            {'name': '小节2', 'level': SectionLvEnum.LV2, 'can_have_multiple': False, 'desc': '小节2_desc'},
            {'name': '小节x', 'level': SectionLvEnum.LV2, 'can_have_multiple': False, 'desc': '小节x_desc'},
            {'name': '小小节1', 'level': SectionLvEnum.LV2, 'can_have_multiple': False, 'desc': '小小节1_desc'},
            {'name': '小小节2', 'level': SectionLvEnum.LV2, 'can_have_multiple': False, 'desc': '小小节2_desc'},
            {'name': '小小节x', 'level': SectionLvEnum.LV2, 'can_have_multiple': False, 'desc': '小小节x_desc'},
        ]
        final_section_obj_list = []
        for section_dict in section_dict_list:
            section_obj = SectionObj(section_dict)
            final_section_obj_list.append(section_obj)
            pass
        return final_section_obj_list
        pass

    pass


class DemoDragDropTreeWidget(QMainWindow, Ui_MainWindow):
    """demo of drag and drop"""

    def __init__(self, parent=None, the_list=[]):
        self.the_list = the_list

        super(DemoDragDropTreeWidget, self).__init__(parent)
        self.setupUi(self)
        self.__initUi()
        self.__connectSlots()

        pass

    def __initUi(self):
        # list
        self.__initListWidget()
        # tree
        self.__initTreeWidget()
        pass

    def __initListWidget(self):
        """initiate appearance of listWidget"""
        listWgt = self.listWidget
        section_obj_list = self.the_list

        # for show
        fruit_name_list = []
        for fruit_obj in section_obj_list:
            assert isinstance(fruit_obj, SectionObj)
            fruit_name_list.append(fruit_obj.name)
            pass
        listWgt.addItems(fruit_name_list)

        # for data
        row_num = listWgt.count()
        for the_row in range(row_num):
            the_item = listWgt.item(the_row)
            the_item.setData(DATA_ROLE, section_obj_list[the_row])
            pass

        # set style
        self.__list_set_style()
        pass

    def __list_set_style(self):
        """set style for listWidget"""
        listWgt = self.listWidget
        # drag enabled
        listWgt.setDragEnabled(True)
        pass

    def __initTreeWidget(self):
        """initiate appearance of treeWidget"""
        treeWgt = self.treeWidget
        self.__tree_set_style()
        # self.treeWidget.dropEvent() # dropMimeData()
        pass

    def __tree_set_style(self):
        """set style for treeWidget"""
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, QTreeWidget)
        treeWgt.setAcceptDrops(True)  # set accept drops (QWidget)
        pass

    def __connectSlots(self):
        # list
        listWgt = self.listWidget
        listWgt.itemClicked.connect(self.__onListItemClicked)

        # treeWgt
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, MyTreeWidget)
        '''item clicked'''
        treeWgt.itemClicked.connect(self.__onTreeItemClicked)
        '''treeWidget 右键方法'''
        treeWgt.setContextMenuPolicy(Qt.CustomContextMenu)  # 自定义右键菜单, from QWidget
        treeWgt.customContextMenuRequested.connect(self.__onHandleCustomMenu)
        '''custom slots for treeWgtItem addition and deletion'''
        # do something
        treeWgt.treeWgtItem_add_signal.connect(self.__onTreeItemAdd)
        pass

    def __onHandleCustomMenu(self, pos):
        """handle issue of right-click menu"""
        item_current = self.treeWidget.currentItem()
        item_position = self.treeWidget.itemAt(pos)

        if item_current == item_position and item_current is not None:  # 右击了treeWidgetItem
            rightClick_menu_treeItem = QMenu()
            action_delete_item = QAction('删除', self)
            action_delete_item.triggered.connect(self.__onDeleteTreeItem)
            rightClick_menu_treeItem.addAction(action_delete_item)
            rightClick_menu_treeItem.exec_(QCursor.pos())  # 让右键菜单不会瞬间消失...
        pass

    def __onDeleteTreeItem(self):
        """right-click delete"""
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, MyTreeWidget)
        currentItem = treeWgt.currentItem()

        parent_tree_item = currentItem.parent()

        # topLv delete
        if parent_tree_item is None:
            index = treeWgt.indexOfTopLevelItem(currentItem)
            treeWgt.setCurrentItem(currentItem)
            treeWgt.treeWgtItem_delete_signal.emit(0)
            treeWgt.takeTopLevelItem(index)
        # child delete
        elif parent_tree_item is not None:
            treeWgt.setCurrentItem(currentItem)
            treeWgt.treeWgtItem_delete_signal.emit(0)
            parent_tree_item.removeChild(currentItem)
            pass

        pass

    def __onTreeItemAdd(self, add_delete_flag):
        """handle issue when treeWgtItem changed"""
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, QTreeWidget)
        # judge and set section_no
        '''add_delete_flag: 1 is add , 0 is delete'''
        if add_delete_flag == 1:
            self.__generate_section_no(add_delete_flag)
            pass
        elif add_delete_flag == 0:
            self.__generate_section_no(add_delete_flag)
            # print('delete ' + changed_item.text(0))
            pass
        treeWgt.expandAll()
        pass

    def __generate_section_no(self, add_delete_flag):
        """
        自动生成section_no

        :param add_delete_flag: 判断是加还是减小节, add:1, delete:0
        :return: None
        """
        # todo now, need recursion...
        '''
        增加是没有问题的, 删除会影响排名在后的同级别子树...
        '''
        treeWgt = self.treeWidget
        changed_item = treeWgt.currentItem()
        # for addition
        para_dict = {
            'changed_item': changed_item,
            'add_delete_flag': add_delete_flag
        }
        self.__set_sectionNo_simple(para_dict)

        # for deletion

        # if not parent:  # parent is TreeWidget
        #     topLv_count = treeWgt.topLevelItemCount()
        #     for index in range(topLv_count):
        #         each_topLv_item = treeWgt.topLevelItem(index)
        #         data = each_topLv_item.data(DATA_COLUMN, DATA_ROLE)
        #         assert isinstance(data, SectionObj)
        #         # update data
        #         if add_delete_flag == 1:
        #             data.section_no = index + 1  # section_no is count from 1
        #         elif add_delete_flag == 0:
        #             if index >= 1:
        #                 data.section_no = index
        #                 pass
        #             else:
        #                 data.section_no = 1
        #         # set appearance
        #         self.__set_text_for_treeWgtItem(each_topLv_item)
        #         # each_topLv_item.setText(TEXT_COLUMN, str(data.section_no) + data.name)
        #     pass
        # elif parent:  # parent is TreeWidgetItem
        #     child_count = parent.childCount()
        #     pass
        #     for child_index in range(child_count):
        #         child_data = parent.child(child_index).data(DATA_COLUMN, DATA_ROLE)
        #         assert isinstance(child_data, SectionObj)
        #         if add_delete_flag == 1:
        #             child_data.section_no = child_index + 1  # section_no is count from 1
        #         elif add_delete_flag == 0:
        #             if child_index >= 1:
        #                 child_data.section_no = child_index
        #             else:
        #                 child_data.section_no = 1
        #         # set the appearance
        #         self.__set_text_for_treeWgtItem(parent.child(child_index))
        #         pass
        pass

    def __set_sectionNo_simple(self, para_dict):
        """设定简单的section_no, 只设置一个数字"""
        # todo 把加sectionNo加和减分开...
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, QTreeWidget)
        changed_item = para_dict['changed_item']
        add_delete_flag = para_dict['add_delete_flag']
        changed_item_index = 0  # TBD
        parent = changed_item.parent()
        if not parent:  # parent is TreeWidget
            topLv_count = treeWgt.topLevelItemCount()
            for index in range(topLv_count):
                each_topLv_item = treeWgt.topLevelItem(index)
                the_changed_data = each_topLv_item.data(DATA_COLUMN, DATA_ROLE)
                assert isinstance(the_changed_data, SectionObj)

                # update data
                if add_delete_flag == 1:  # add one
                    the_changed_data.section_no = index + 1  # section_no is count from 1
                elif add_delete_flag == 0:  # delete one
                    for afterwards_index in range(index + 1, topLv_count): # from the next item, reset the section_no
                        each_after_item = treeWgt.topLevelItem(afterwards_index)
                        each_after_data = each_after_item.data(DATA_COLUMN, DATA_ROLE)
                        each_after_data.section_no = index  # just minus 1, index starts from 0
                        pass
                    pass
                else:
                    the_changed_data.section_no = 1
                # set appearance
                # self.__set_text_for_treeWgtItem(each_topLv_item)

                each_topLv_item.setText(TEXT_COLUMN, str(the_changed_data.section_no) + the_changed_data.name)
        #     pass
        # elif parent:  # parent is TreeWidgetItem
        #     child_count = parent.childCount()
        #     pass
        #     for child_index in range(child_count):
        #         child_data = parent.child(child_index).data(DATA_COLUMN, DATA_ROLE)
        #         assert isinstance(child_data, SectionObj)
        #         if add_delete_flag == 1:
        #             child_data.section_no = child_index + 1  # section_no is count from 1
        #         elif add_delete_flag == 0:
        #             if child_index >= 1:
        #                 child_data.section_no = child_index
        #             else:
        #                 child_data.section_no = 1
        #         # set the appearance
        #         self.__set_text_for_treeWgtItem(parent.child(child_index))
        #         pass
        pass

    @staticmethod
    def __set_text_for_treeWgtItem(treeWgtItem: QTreeWidgetItem):
        chinese_num = DemoDragDropTreeWidget.__get_chineseCharacter_from_1_to_n(99)
        data = treeWgtItem.data(DATA_COLUMN, DATA_ROLE)
        assert isinstance(data, SectionObj)
        if data.level.value == SectionLvEnum.LV1.value:
            try:
                sectionNo_in_chinese = chinese_num[data.section_no - 1]  # section_no starts with 1
            except IndexError:
                sectionNo_in_chinese = '越界'
                pass
            treeWgtItem.setText(TEXT_COLUMN, str(sectionNo_in_chinese) + '.' + data.name)
            pass
        elif data.level.value != SectionLvEnum.LV1.value:
            treeWgtItem.setText(TEXT_COLUMN, str(data.section_no) + '.' + data.name)
            pass
        pass

    @staticmethod
    def __get_chineseCharacter_from_1_to_n(number_n: int):
        """得到从1 到 number_n 的整数的中文字符表达, 如:三十一, 九十九..., 现在只支持最高到99"""
        result_list = []
        chinese_num_list = ['一', '二', '三', '四', '五',
                            '六', '七', '八', '九', '十']
        for each_num in range(1, number_n + 1):
            one_chinese_num = ''
            if each_num <= 10:
                one_chinese_num = chinese_num_list[each_num - 1]
                result_list.append(one_chinese_num)
                pass
            elif each_num > 10:
                tens_digit_num = int(each_num / 10)
                single_digit_num = each_num % 10
                if tens_digit_num == 1:
                    one_chinese_num = '十' + chinese_num_list[single_digit_num - 1]
                elif tens_digit_num != 1:
                    if single_digit_num != 0:
                        one_chinese_num = chinese_num_list[tens_digit_num - 1] + '十' + chinese_num_list[single_digit_num - 1]
                        pass
                    elif single_digit_num == 0:  # 输出'二十', 而不是 '二十十'
                        one_chinese_num = chinese_num_list[tens_digit_num - 1] + '十'
                        pass
                result_list.append(one_chinese_num)
                pass
        return result_list
        pass

    # @staticmethod
    # def get_chinese(n):  # just for test
    #     result_list = DemoDragDropTreeWidget.__get_chineseCharacter_from_1_to_n(n)
    #     pass

    def __onTreeItemClicked(self):
        """handle issue when treeItem clicked"""
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, QTreeWidget)
        current_item = treeWgt.currentItem()
        current_data = current_item.data(DATA_COLUMN, DATA_ROLE)
        assert isinstance(current_data, SectionObj)
        print(current_data.desc)
        pass

    def __onListItemClicked(self):
        """handle the issue when list_item clicked"""
        # current_item = self.listWidget.currentItem()
        # current_data = current_item.data(DATA_ROLE)
        # assert isinstance(current_data, SectionObj)
        # print(current_data.name + ': ' + current_data.desc)
        pass

    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    free_fruit_list = SectionFactory.getFreeFruits()
    win = DemoDragDropTreeWidget(the_list=free_fruit_list)
    win.show()
    sys.exit(app.exec_())

    # sectionA = SectionObj('A')
    # sectionB = SectionObj('B')
    # section_list = [sectionA, sectionB]
    pass
