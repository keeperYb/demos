"""拖拽各小节的界面设计, 生成list"""
from enum import Enum

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QMenu, QAction

import sys
import os

# for cmd searching path
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from UI.drag_drop_treewidget_UI import Ui_MainWindow

# todo total view
"""
drag drop的策略:
1. 顶层只有一级标题可放
2. 一个级数的标题只能放到对应-1级的标题的子树中
3. 同一个节点层中,不能有相同的标题, 但是在不同的命名空间中,可以有相同的标题
4. 标题号根据每一个命名空间来自动判定, 但是标题号格式不要写死

todo now
    -在 MyTreeWidget dropEvent() 中, 获取到data数据
    -根据drop的上层node, 以及自身node情况, 判断can_be_dropped() __NOW
    
"""
section_list = []
DATA_ROLE = 1
DATA_COLUMN = 0  # the column where treeWidget stores data


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
            {'name': '第一部分', 'level': SectionLvEnum.LV1, 'desc': '第一部分desc'},
            {'name': '第二部分', 'level': SectionLvEnum.LV1, 'desc': '第二部分desc'},
            {'name': '小节1', 'level': SectionLvEnum.LV2, 'desc': '小节1_desc'},
            {'name': '小节a', 'level': SectionLvEnum.LV2, 'desc': '小节a_desc'}
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
        # set accept drops (QWidget)
        treeWgt.setAcceptDrops(True)
        # # set drag enabled
        # treeWgt.setDragEnabled(True)
        pass

    def __connectSlots(self):
        # list
        listWgt = self.listWidget
        listWgt.itemClicked.connect(self.__onListItemClicked)
        # tree
        treeWgt = self.treeWidget
        assert isinstance(treeWgt, QTreeWidget)
        treeWgt.itemClicked.connect(self.__onTreeItemClicked)
        # treeWidget 右键方法
        treeWgt.setContextMenuPolicy(Qt.CustomContextMenu)  # 自定义右键菜单, from QWidget
        treeWgt.customContextMenuRequested.connect(self.__onHandleCustomMenu)
        # btn
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
        assert isinstance(treeWgt, QTreeWidget)
        currentItem = treeWgt.currentItem()

        parent_tree_item = currentItem.parent()

        # topLv delete
        if parent_tree_item is None:
            index = treeWgt.indexOfTopLevelItem(currentItem)
            treeWgt.takeTopLevelItem(index)
        # child delete
        elif parent_tree_item is not None:
            parent_tree_item.removeChild(currentItem)
        pass

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
