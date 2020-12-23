from PyQt5.QtWidgets import QTreeWidget, QLineEdit, QTreeWidgetItem
from UI.drag_drop_treewidget import DATA_ROLE


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setDefaultDropAction(Qt.DropAction)

    def dropEvent(self, event):
        super(MyTreeWidget, self).dropEvent(event)
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
