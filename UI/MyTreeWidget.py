import traceback

from PyQt5.QtWidgets import QTreeWidget, QLineEdit, QTreeWidgetItem, QWidget, QAbstractItemView, QListView, QListWidget, \
    QListWidgetItem
from UI.drag_drop_treewidget import DATA_ROLE, SectionObj, SectionLvEnum

DATA_COLUMN = 0  # used for treeWgtItem to set/get data
TEXT_COLUMN = 0  # used for treeWgtItem to set/get text


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setDefaultDropAction(Qt.DropAction)
        pass

    def dragEnterEvent(self, event):
        super(MyTreeWidget, self).dragEnterEvent(event)
        pass

    def dragMoveEvent(self, event):
        super(MyTreeWidget, self).dragMoveEvent(event)
        pass

    def dropEvent(self, event):
        """处理drop后的一系列操作"""
        """check_can_be_dropped HERE"""
        # detection of dragMove is VERY sensitive..
        dropped_item = self.__get_dropped_item(event)
        treeWgt_item = self.__transfer_to_treeWidgetItem(dropped_item)
        current_item_data = self.__get_dropped_item_data(treeWgt_item)

        potential_parent_item = self.itemAt(event.pos())  # VERY useful, pos()... 不可靠,蹭着边的时候有问题...
        if potential_parent_item:
            potential_parent_item = self.itemAt(event.pos())  # VERY useful, pos()... 不可靠,蹭着边的时候有问题...
            can_be_dropped = self.__check_can_be_dropped(current_item_data, potential_parent_item)
            if can_be_dropped:
                potential_parent_item.addChild(treeWgt_item)
            pass
        elif not potential_parent_item:
            can_be_dropped = self.__check_can_be_dropped(current_item_data, self)
            if can_be_dropped:
                self.addTopLevelItem(treeWgt_item)
            pass
        pass

    @staticmethod
    def __transfer_to_treeWidgetItem(original_item):
        result_treeWidgetItem = None
        if isinstance(original_item, QListWidgetItem):  # ?? what's basic type of listWidgetItem, treeWgtItem
            result_treeWidgetItem = QTreeWidgetItem()
            result_treeWidgetItem.setText(TEXT_COLUMN, original_item.text())
            data = original_item.data(DATA_ROLE)
            result_treeWidgetItem.setData(DATA_COLUMN, DATA_ROLE, data)
            pass
        elif isinstance(original_item, QTreeWidgetItem):
            result_treeWidgetItem = original_item
            pass
        return result_treeWidgetItem
        pass

    @staticmethod
    def __check_can_be_dropped(child_item_data: SectionObj, parent):
        """
        check the possibility of dropping according to the current_item_data, and dropped parent item

        :param child_item_data: the data of child_treeWgtItem
        :param parent: the parent, maybe a treeWgtItem , maybe a treeWgt
        :return: True or False
        """
        can_be_added_rst = False
        if not isinstance(parent, QTreeWidgetItem):  # check the type of parent
            # child_item is going to add to topLevel of the tree
            child_level = child_item_data.level
            desired_level = SectionLvEnum.LV1
            if child_item_data.level.value == SectionLvEnum.LV1.value:
                can_be_added_rst = True
            pass
        elif isinstance(parent, QTreeWidgetItem):
            # child_item is going to add to another treeWidgetItem
            parent_item_data = parent.data(DATA_COLUMN, DATA_ROLE)
            # assert isinstance(parent_item_data, SectionObj)
            if child_item_data.level.value - parent_item_data.level.value == 1:
                can_be_added_rst = True
                pass
            pass
        return can_be_added_rst
        pass

    @staticmethod
    def __get_dropped_item(event):
        source_widget = event.source()
        dropped_item = source_widget.currentItem()
        return dropped_item
        pass

    @staticmethod
    def __get_dropped_item_data(widget_item):
        try:
            if isinstance(widget_item, QTreeWidgetItem):
                current_item_data = widget_item.data(DATA_COLUMN, DATA_ROLE)
                return current_item_data
            pass
        except:
            traceback.print_exc()
            pass
        pass

    # def rightClickMenu(self, pos):
    #     try:
    #         self.contextMenu = QMenu()  # 创建对象
    #         self.actionA = self.contextMenu.addAction(u'动作')  # 添加动作
    #         self.actionA = self.contextMenu.addAction(u'动作b')
    #         self.actionA.triggered.connect(self.actionHandler)
    #         self.contextMenu.exec_(self.mapToGlobal(pos))  # 随指针的位置显示菜单
    #         self.contextMenu.show()  # 显示
    #     except Exception as e:
    #         print(e)
    #
    # def actionHandler(self):
    #     print(self.currentItem().text(0))
