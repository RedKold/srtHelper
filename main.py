from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QMainWindow
import sys
import setVectorBase
from Ui_qwidget import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
        self.inputPush.clicked.connect(self.inputPush_clicked)  # 将点击事件绑定到类方法

        # 初始化 SubtitleViewer 为 None
        self.viewer = None

    def inputPush_clicked(self):
        # 获取前 5 条最相似的台词和时间轴
        top_5_lines, top_5_timestamps, top_5_similarities = setVectorBase.setVector()

        # 创建并显示 SubtitleViewer
        self.viewer = SubtitleViewer(top_5_lines, top_5_timestamps, top_5_similarities)
        self.viewer.show()  # 使用 show() 方法显示窗口


class SubtitleViewer(QWidget):
    def __init__(self, lines, timestamps, similarities):
        super().__init__()

        self.setWindowTitle("最相似台词查询结果")
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()

        # 显示前 5 条最相似的台词和时间轴
        for i in range(5):
            label = QLabel(f"相似度: {similarities[i]:.4f}\n时间轴: {timestamps[i]}\n台词: {lines[i]}")
            layout.addWidget(label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWidget()
    myWin.show()
    sys.exit(app.exec_())
