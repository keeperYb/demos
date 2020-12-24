import traceback

from PyQt5.QtWidgets import QTreeWidget, QLineEdit, QTreeWidgetItem, QWidget, QAbstractItemView, QListView, QListWidget
from UI.drag_drop_treewidget import DATA_ROLE, SectionObj


class MyTreeWidget(QTreeWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setDefaultDropAction(Qt.DropAction)
        pass

    def dragEnterEvent(self, event):
        super(MyTreeWidget, self).dragEnterEvent(event)
        pass

    def dragMoveEvent(self, event):
        """check_can_be_dropped HERE"""
        # detection of dragMove is VERY sensitive..
        current_item_data = self.__get_dropped_item_data(event)
        # todo , detect the item under the current_item, which is potential to become the parent of current_item
        try:
            potential_parent_item = self.itemAt(event.pos())  # VERY useful, pos()!
            print(potential_parent_item.text(0))
        except AttributeError:  # when adding to ROOT

            print("ROOT")

        # can_be_dropped = self.__check_can_be_dropped(event, current_item_data)
        # if can_be_dropped:
        #     pass
        #     self.dropEvent(event)
        # elif not can_be_dropped:
        #     pass
        pass

    def dropEvent(self, event):
        """处理drop后的一系列操作"""
        super(MyTreeWidget, self).dropEvent(event)
        pass

    def __check_can_be_dropped(self, event, current_item_data):
        """
        check the possibility of dropping according to the current_item_data, and dropped parent item

        :return: True or False
        """
        dropped_parent_item = ''  # xx
        return True
        pass

    @staticmethod
    def __get_dropped_item_data(event):
        source_widget = event.source()  # 获得发来event的source_widget, 再通过它来获得source_item
        try:
            assert isinstance(source_widget, QAbstractItemView)  # use the base class of QListWidget, QTreeWidget
            current_item_data = source_widget.currentItem().data(DATA_ROLE)
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
