from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(400, 600)

        self.tree = MyTreeWidget(self)
        self.tree.setHeaderHidden(True)
        self.tree.setDragEnabled(True)  # ...  whether the view supports dragging of its own items
        self.tree.setAcceptDrops(True)  # ... whether drop events are enabled for this widget
        # 第一个根节点, 朋友
        root_friends = QTreeWidgetItem(self.tree)
        root_friends.setText(0, '朋友')
        child1 = QTreeWidgetItem(root_friends)
        child1.setText(0, '朋友1')
        # 第二个根节点, 家人
        root_familyMembers = QTreeWidgetItem(self.tree)
        root_familyMembers.setText(0, '家人')
        child2 = QTreeWidgetItem(root_familyMembers)
        child2.setText(0, '家人1')

        self.tree.clicked.connect(self.onTreeClicked)
        self.tree.collapsed.connect(self.onTreeCollapsed)  # collapsed, 收缩(折叠), 反义词是expanded,同义词是fold

        self.tree.itemClicked.connect(self.itemClicked)

        self.edit = QLineEdit(self)
        self.edit.setDragEnabled(True)
        self.edit.move(300, 300)

        self.btn = QPushButton(self)
        self.btn.move(300, 50)
        self.btn.clicked.connect(self.btnClick)

    def itemClicked(self, item, column):
        # print(column)
        pass

    def btnClick(self, sender):
        print(self.tree.currentItem().text(0))
        print(type(sender))

    def onTreeClicked(self, qmodelindex):
        # print(self.tree.currentItem().text(0))
        pass

    def onTreeCollapsed(self, qmodelindex):
        # print(self.tree.currentItem().text(0) + 'collapsed')
        pass


class MyTreeWidget(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDefaultDropAction(Qt.MoveAction)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print("dragEnterEvent")
        e.accept()
        # if e.mimeData().hasText():
        #     e.accept()
        # else:
        #     e.ignore()

    def dragMoveEvent(self, e):
        pass

    def dropEvent(self, event):
        # todo , critical !!
        currentItem = self.itemAt(event.pos())
        if currentItem:
            if isinstance(event.source(), MyTreeWidget):
                if self.currentItem().parent():
                    super().dropEvent(event)
                else:
                    pass
            elif isinstance(event.source(), QLineEdit):
                item = QTreeWidgetItem(currentItem)
                item.setText(0, event.mimeData().text())
                #
                # item.setContextMenuPolicy(Qt.CustomContextMenu)  # 打开右键菜单的策略
                # item.customContextMenuRequested.connect(self.rightClickMenu)  # 绑定事件
        else:
            pass

    def rightClickMenu(self, pos):
        try:
            self.contextMenu = QMenu()  # 创建对象
            self.actionA = self.contextMenu.addAction(u'动作')  # 添加动作
            self.actionA = self.contextMenu.addAction(u'动作b')
            self.actionA.triggered.connect(self.actionHandler)
            self.contextMenu.exec_(self.mapToGlobal(pos))  # 随指针的位置显示菜单
            self.contextMenu.show()  # 显示
        except Exception as e:
            print(e)

    def actionHandler(self):
        print(self.currentItem().text(0))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
