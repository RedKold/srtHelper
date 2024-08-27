from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QMainWindow
import sys
import setVectorBase
from Ui_qwidget import Ui_SrtHelper
from PyQt5.QtWidgets import QFileDialog
import os
import storeVectorBase

#主窗口类，继承自qwideget
class MyWidget(QWidget, Ui_SrtHelper):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
        self.inputPush.clicked.connect(self.inputPush_clicked)  # 将点击事件绑定到类方法
        #init the default srt path
        self.FilenameLabel.setText("/srt/Frozen_chs.srt")
        
        # 初始化 SubtitleViewer 为 None
        self.viewer = None

        self.selectSrtButton.clicked.connect(self.openFileDialog)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # 只读模式（可选）
        
        # 第一个参数是父组件，第二个参数是对话框标题，第三个参数是默认路径
        #过滤出符合srt条件的文件
        file_path, _ = QFileDialog.getOpenFileName(None, "选择.srt 文件", "", "字幕文件 (*.srt)", options=options)
        
        if file_path:
            self.FilenameLabel.setText(file_path)

        

    def inputPush_clicked(self):
        # 获取前 k 条最相似的台词和时间轴
        k=self.amtspinBox.value()
        query=self.inputLineEdit.text()

        #调试
        print(query)

        filename=self.FilenameLabel.text()
        db_filename=f"{filename}_db.pkl"
        if not os.path.exists(db_filename):
            print("不存在现有的数据库，创建新数据库中")
            storeVectorBase.generate_and_save_embeddings(filename,db_file=db_filename)
        else:
            print("已存在相关数据库，为你检索中")
            
        top_k_lines, top_k_timestamps, top_k_similarities = setVectorBase.find_most_similar(query,k,db_file=db_filename)

        # 创建并显示 SubtitleViewer
        self.viewer = SubtitleViewer(top_k_lines, top_k_timestamps, top_k_similarities,k)
        self.viewer.show()  # 使用 show() 方法显示窗口


class SubtitleViewer(QWidget):
    def __init__(self, lines, timestamps, similarities,k=5):
        super().__init__()

        self.setWindowTitle("最相似台词查询结果")
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()

        # 显示前 k 条最相似的台词和时间轴
        for i in range(k):
            label = QLabel(f"{i+1}. 相似度: {similarities[i]:.4f}\n时间轴: {timestamps[i]}\n台词: {lines[i]}\n")
            layout.addWidget(label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWidget()
    myWin.show()
    sys.exit(app.exec_())
