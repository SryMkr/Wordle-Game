# 导入所需要的包
import sys
import uuid
import requests
import wave
import base64
import hashlib
import json
from importlib import reload
import time

reload(sys)  # 重新加载之前载入的模块 但是不重新载入会怎么样了？

YOUDAO_URL = 'https://openapi.youdao.com/iseapi'  # 要使用的有道API网址
APP_KEY = '3d96861d86e5d1eb'  # 我得应用ID
APP_SECRET = '0wq0M3dYpvMhlgpzgcTv6MyWLCn7ou0A'  # 我得应用密钥


# 要评测的音频文件的Base64编码字符串
def truncate(q):
    # 如果字符串为空值，那么返回空值
    if q is None:
        return None
    # 然后判断字符串的长度
    size = len(q)
    # 如果长度小于20 input直接为20 如果字符串长度大于20 字符串等于【前十个字符】+【字符串的长度】+【后10个字符串】
    return q if size <= 20 else q[0:10] + str(size) + q[size-10:size]


# 将字符串用hash算法加密
def encrypt(signStr):
    hash_algorithm = hashlib.sha256()  # 生成一个公式
    hash_algorithm.update(signStr.encode('utf-8'))  # 用上面的公式将字符串编码
    return hash_algorithm.hexdigest()  # 返回编码后的一串字符串


# 发送请求有一系列固定的东西
def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # 这个头部是固定的东西
    # 第一个参数发送的URL,第二个参数data里一些固定的东西，第三个就是头部一些参数
    return requests.post(YOUDAO_URL, data=data, headers=headers)


# 这个是主要的代码 输入的参数是 玩家的语音文件路径，以及原始文件的内容【'./record/'+file_name+'.wav'， cat】
def connect(audio_file_path, audio_text):
    recordname = audio_file_path.split("/")[-1]  # 取得发音的wav文件 例如 cat.wav
    audio_file_path = audio_file_path  # 玩家发音文件的路径
    lang_type = 'en'  # 源语言类型，就是英文
    #  rindex() 返回子字符串 str 在字符串中最后出现的位置 其实就是获得文件的拓展名 可是不就是 .wav么
    extension = audio_file_path[audio_file_path.rindex('.')+1:]
    if extension != 'wav':
        print('不支持的音频类型')
        sys.exit(1)
    wav_info = wave.open(audio_file_path, 'rb')  # 打开音频文件
    sample_rate = wav_info.getframerate()  # 获得音频的采样率
    nchannels = wav_info.getnchannels()  # 获得音频的声道
    wav_info.close()  # 关闭文件
    with open(audio_file_path, 'rb') as file_wav:
        q = base64.b64encode(file_wav.read()).decode('utf-8')  # 要评测的音频文件的Base64编码字符串

    data = {}  # 创建一个data的字典，要发送到url进行打分
    data['text'] = audio_text  # 要评测的音频文件对应的文本
    curtime = str(int(time.time()))  # 获得当前开始的时间戳（秒）
    data['curtime'] = curtime  # # 获得当前开始的时间戳（秒）
    salt = str(uuid.uuid1())  # 唯一通用识别码 就是全球唯一的一个标志而已
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET  # 一个签名的原始组成
    sign = encrypt(signStr)  # 将这个签名使用hash算法编码
    data['appKey'] = APP_KEY # 应用ID
    data['q'] = q  # 就是q的值
    data['salt'] = salt  # 唯一通用识别码
    data['sign'] = sign  # hash转换后的值
    data['signType'] = "v2"  # 签名类型
    data['langType'] = lang_type  # 语言类型，只支持英文
    data['rate'] = sample_rate  # 采样率16000
    data['format'] = 'wav'  # 文件类型wav
    data['channel'] = nchannels  # 声道数， 仅支持单声道，请填写固定值1
    data['type'] = 1  # 上传类型， 仅支持base64上传，请填写固定值1

    response = do_request(data)  # 发送打分请求
    j = json.loads(str(response.content, encoding="utf-8"))  # 返回一个json文件，就是返回的结果
    # 这里设置自己想要保存什么样的结果 记录一下自己需要的参数
    contextIntegrity = "句子完整度:"+str(round(j["integrity"], 2))+"  "  # integrity 单词发音的完整度检查是不是这个单词
    current_content = "当前单词:"+str(j["refText"])+"  "  # 显示的是所有的单词
    pronunciation = "发音准确度:"+str(round(j["pronunciation"], 2)) + "  "  # 所有单词的发音准确度
    word_list = j["words"]  # 获得有关单词的所有信息
    word_information_list = []   # 创建一个列表将不同的单词分开
    recordAndResult = ''  # 创建一个空的字符串
    # 我要获得每一个单词的分数,而且还要获得每一个音素的单词，音标，分数
    for word_index in range(len(word_list)):  # 这个是顺序循环每一单词的得分，以及音素得分
        word_information = {}  # 创建一个字典用来记录单词的所有信息
        current_word = word_list[word_index]['word']  # 得到当前的单词
        recordAndResult = recordAndResult + current_word + '的得分：'  # 显示目前的单词
        word_information['第' + str(word_index+1) + '个单词是'] = current_word
        pronunciation_score = int(word_list[word_index]['pronunciation']) # 获得单词的整体发音
        recordAndResult = recordAndResult + str(pronunciation_score) + '   '  # 显示单词的得分
        word_information[current_word + '的得分'] = pronunciation_score
        word_phonemes = word_list[word_index]['phonemes']

        for phonemes_index in range(len(word_phonemes)):  # 顺序循环单词的音素
            current_phoneme = word_phonemes[phonemes_index]["phoneme"]  # 当前的音素
            word_information[current_word + '的第' + str(phonemes_index+1) + '音素是'] = current_phoneme  # 获得这个音素
            recordAndResult = recordAndResult + '音素' + current_phoneme + '的得分: '
            phonemes_pronunciation = int(word_phonemes[phonemes_index]['pronunciation'])  # 获得这个音素的发音分数
            word_information[current_word + '的音素' + str(current_phoneme) + '得分'] = phonemes_pronunciation
            recordAndResult = recordAndResult + str(phonemes_pronunciation) + '   '
        recordAndResult = recordAndResult + '\n'  # 对于每一单词都要换行
        word_information_list.append(word_information)  # 每一个字典为列表的每一个元素
    # 这计划的意思是将整个返回的结果存到一个文件夹中
    result_file = open('./result' + '/result_' + recordname.split('.')[0] + '.txt', 'w', encoding='utf-8').write(str(j))
    # 这个是返回我们需要的结果 以下的代码是必须的
    #recordAndResult = recordname+" "+contextIntegrity+current_content+pronunciation+"\n"
    return recordAndResult
