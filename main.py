from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton, QMainWindow
import sys
import setVectorBase
from Ui_qwidget import Ui_SrtHelper
from PyQt5.QtWidgets import QFileDialog
import os
import storeVectorBase

os.chdir("E:\\Codinglife\\Python_project\\SRT-learner")


#主窗口类，继承自qwideget
class MyWidget(QWidget, Ui_SrtHelper):
    #定义几个模式的常数
    #Fl:File, Dr:Directory
    Models=['Fl','Dr']
    #初始值
    model=Models[0]
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setupUi(self)
        self.inputPush.clicked.connect(self.inputPush_clicked)  # 将点击事件绑定到类方法
        #init the default srt path
        self.FilenameLabel.setText("E:/Codinglife/Python_project/SRT-learner/srt/Frozen_chs.srt")
        
        # 初始化 SubtitleViewer 为 None
        self.viewer = None
        # 将选择字幕文件按钮点击信号与对应处理函数连接
        self.selectSrtButton.clicked.connect(self.openFileDialog)
        self.selectDirecButton.clicked.connect(self.openDirecDialog)

        #隐藏工具人文件名label
        self.FilenameLabel.setVisible(False)
        

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # 只读模式（可选）
        
        # 第一个参数是父组件，第二个参数是对话框标题，第三个参数是默认路径
        #过滤出符合srt条件的文件
        file_path, _ = QFileDialog.getOpenFileName(None, "选择.srt 文件", "", "字幕文件 (*.srt)", options=options)
        
        if file_path:
            self.FilenameLabel.setText(file_path)

    def openDirecDialog(self):
            # 获取前 k 条最相似的台词和时间轴
        k = self.amtspinBox.value()
        query = self.inputLineEdit.text()

        # 调试
        print(query)

        # 选择一个目录
        dir_path = QFileDialog.getExistingDirectory(self, "选择包含数据库的目录")
        
        if not dir_path:
            print("未选择目录")
            return
        
        # 遍历目录中的所有 .pkl 文件
        db_files = [f for f in os.listdir(dir_path) if f.endswith('_db.pkl')]
        
        if not db_files:
            print("未找到数据库文件")
            return
        
        # 存储所有数据库的检索结果
        all_top_k_lines = []
        all_top_k_timestamps = []
        all_top_k_similarities = []
        all_top_k_filmnames=[]

        # 对每个数据库文件进行检索
        for db_filename in db_files:
            full_path = os.path.join(dir_path, db_filename)
            print(f"正在加载数据库 {full_path}")

            # 加载数据库（这里假设有一个 load_db 函数）
            setVectorBase.load_embeddings(full_path)

            # 查找最相似的台词
            top_k_lines, top_k_timestamps, top_k_similarities,top_k_filmname = setVectorBase.find_most_similar(query, k,db_file=full_path)

            # 将结果存储到总列表中
            # (Python tips) extend 会把元素内容展开加到后面，append会直接硬加进来
            all_top_k_lines.extend(top_k_lines)
            all_top_k_timestamps.extend(top_k_timestamps)
            all_top_k_similarities.extend(top_k_similarities)
            all_top_k_filmnames.extend(top_k_filmname)

            #排序处理
            # 合并为一个包含所有数据的元组列表
            all_results = list(zip(all_top_k_lines, all_top_k_timestamps, all_top_k_similarities, all_top_k_filmnames))

            # 按相似度从高到低排序
            all_results.sort(key=lambda x: x[2], reverse=True)

            #print(f"all_result is: {list(all_results)}")
            # 将排序后的结果重新解压
            all_top_k_lines, all_top_k_timestamps, all_top_k_similarities, all_top_k_filmnames = zip(*all_results)#'*'是解包运算符
           
            all_top_k_lines=list(all_top_k_lines)
            all_top_k_timestamps=list(all_top_k_timestamps)
            all_top_k_similarities=list(all_top_k_similarities)
            all_top_k_filmnames=list(all_top_k_filmnames)

        # 显示所有数据库的综合结果



        self.viewer = SubtitleViewer(all_top_k_lines, all_top_k_timestamps, all_top_k_similarities,all_top_k_filmnames,k)
        self.viewer.show()
        

    def inputPush_clicked(self):
        # 获取前 k 条最相似的台词和时间轴
        k=self.amtspinBox.value()
        query=self.inputLineEdit.text()

        #调试
        print(f"当前查找请求为{query}")

        filename=self.FilenameLabel.text()

        #print(f"inputPush按钮要打开的是{filename}")

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
    def __init__(self, lines, timestamps, similarities,filmname,k=5):
        super().__init__()

        self.setWindowTitle("最相似台词查询结果")
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()

        print(filmname)
        # 显示前 k 条最相似的台词和时间轴
        for i in range(k):
            if(len(filmname)>=1):
                label = QLabel(f"{i+1}. 电影: {filmname[i]}\n相似度: {similarities[i]:.4f}\n时间轴: {timestamps[i]}\n台词: {lines[i]}\n")
            else:
                label = QLabel(f"{i+1}.相似度: {similarities[i]:.4f}\n时间轴: {timestamps[i]}\n台词: {lines[i]}\n")
            layout.addWidget(label)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWidget()
    myWin.show()
    sys.exit(app.exec_())
