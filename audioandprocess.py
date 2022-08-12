'''
这个文件里没有什么主要的内容，其实就是一些对于文件的操作
如果保存结果的东西
'''


# 导入所需要的包
import pyaudio
import threading
import os
from isebynetease import *


# 定义一个声音得model类别
class Audio_model():
    def __init__(self, audio_path, is_recording):
        self.current_file = ''  # 当前选中的这个文件
        self.is_recording = is_recording  # 是不是正在保存文件
        self.audio_file_name = ''  # 这个是保存玩家的发音
        self.audio_chunk_size = 1600  # 缓冲块的大小，多久输出一次
        self.audio_channels = 1  # 单声道
        self.audio_format = pyaudio.paInt16  # 采样点的宽度为16位
        self.audio_rate = 16000  # 采样率

    # 获得文件的名字,这个读取一个txt文件，但是在我的游戏中并不需要，以love.txt为例子，最终结果为love
    def get_file_name(self, file_path):
        file_name = os.path.basename(file_path).split('.')[0]   # 前面是获得文件路径最后一个文件，split是为了去除拓展名
        return file_name  # 最后输出love

    # 这个是记录玩家的发音，挺有用的，可以让玩家听到自己的发音
    def record(self, file_name):
        p = pyaudio.PyAudio()  # 实例化一个audio对象
        # 打开一个信号流
        stream = p.open(
            format=self.audio_format,
            channels=self.audio_channels,
            rate=self.audio_rate,
            input=True,
            frames_per_buffer=self.audio_chunk_size
        )
        wf = wave.open(file_name, 'wb')  # 打开文件
        wf.setnchannels(self.audio_channels)  # 设置声道
        wf.setsampwidth(p.get_sample_size(self.audio_format))  # 设置采样点的位数
        wf.setframerate(self.audio_rate)  # 设置采样率
        # 读取数据写入文件
        while self.is_recording:
            data = stream.read(self.audio_chunk_size)  # 开始读取数据
            wf.writeframes(data)  # 写入数据
        wf.close()  # 关闭文件
        stream.stop_stream()  # 关闭信号
        stream.close()  # 流关闭
        p.terminate()  # 线程结束

    # 这个是记录并且保存结果
    def record_and_save(self):
        self.is_recording = True
        file_name = self.get_file_name(self.current_file)  # 获得当前文件的文件名
        self.audio_file_name = './record/'+file_name+'.wav'  # 保存玩家的发音路径
        # 启动一个线程，target是调用一个函数，args是固定的参数，就是我的文件名字，start是启动线程
        threading.Thread(target=self.record, args=(self.audio_file_name,)).start()

    # 获得文本中的内容
    def get_content(self, file_path):
        with open(file_path, "r") as f:  # 以只读的方式读取文件
            file_content = f.read()  # 读取文本中的所有内容
            return file_content  # 返回文本中的内容

    # 获得玩家的分数,输入的还是我文件的路径'C:/Users/srymkr/Desktop/Love.txt'
    def get_score(self, dict):
        result = []
        for path in dict:  # 支持多个多个类似于Love.txt的文本输入
            file_content = self.get_content(path)  # 获得文件中的内容
            file_name = self.get_file_name(path)  # 获得文件名字 love
            audio_path = './record/'+file_name+'.wav'  # 玩家发音文件要存的地方
            # connect相当于打包发给语音库给打分
            score_result = connect(audio_path, file_content)  # 第一个参数为玩家的发音路径，第二个参数为文件中的内容
            result.append(score_result)  # 将每一个文件的结果一一存到变量中，就是这个意思
        return result