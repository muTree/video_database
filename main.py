import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from moviepy.editor import *
#import moviepy.video.io.ffmpeg as ffmpeg
import sqlite3
from pathlib import Path

path = r'd:\video'

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个按钮和一个标签
        self.button = QPushButton('Click me!')
        self.label = QLabel('Hello, world!')

        # 将按钮和标签添加到布局中
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        # 将布局设置为主窗口的布局
        self.setLayout(layout)

        # 绑定按钮的点击事件
        self.button.clicked.connect(self.update_label)

    def update_label(self):
        self.label.setText('Button clicked!')

if __name__ == '__main__':
    conn = sqlite3.connect("files.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS files
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    path TEXT UNIQUE,
                    type TEXT,
                    md5sum TEXT,
                    suffix TEXT,
                    duration INT,
                    fps INT,
                    size_width INT,
                    size_height INT)''')
    conn.commit()

    files_list = os.listdir(path)
    print(files_list)

    for file in files_list:
        # 打开视频文件
        # 获取视频属性
        name = file
        file_path = os.path.join(path, file)
        clip = VideoFileClip(file_path)

        type = ""
        md5sum = ""
        suffix = Path(file).suffix
        duration = clip.duration  # 视频时长
        fps = clip.fps  # 视频帧率
        size_width, size_height = clip.size  # 视频分辨率（宽度和高度）

        # 打印视频属性
        print("视频时长：", duration, "秒")
        print("视频帧率：", fps, "帧/秒")
        print("视频分辨率：", size_width, "x", size_height)
        #print("视频码率：", video_bitrate, "bps")
        #print("音频码率：", audio_bitrate, "bps" if audio_bitrate else "无音频流")

        # 关闭视频文件
        clip.reader.close()
        clip.audio.reader.close_proc()

        sql = '''INSERT INTO files (name, path, type, md5sum, suffix, duration, fps, size_width, size_height) values
                                            ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")''' % (name, file_path, type, md5sum, suffix, duration, fps, size_width, size_height)
        print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
        except sqlite3.IntegrityError:
            print()

    conn.close()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    print("a")
    sys.exit(app.exec_())
