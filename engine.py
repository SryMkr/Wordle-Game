import pygame
from datetime import datetime, timedelta
import xlrd
from numpy import random
import copy

# 直接设置游戏的主要入口
class MainGame(object):
    def __init__(self, window_width, window_height, GAME_NAME='Wordle Game'):
        self.gameplay_time = 0
        pygame.init()  # 初始化游戏里面的一些模块（包括字体，音乐等六种）
        self.window_width = window_width  # 游戏窗口的宽度
        self.window_height = window_height  # 游戏窗口的高度
        self.window = pygame.display.set_mode((self.window_width, self.window_height))  # 初始化游戏窗口
        pygame.display.set_caption(GAME_NAME)  # 设置游戏的名字
        self.Main_Game_Running = True  # 控制主游戏的运行
        self.GREEN = (0, 255, 0)  # 绿色
        self.RED = (255, 0, 0)    # 红色
        self.BLACK = (0, 0, 0)    # 黑色
        self.GRAY = (130, 130, 130)  # 灰色
        self.WHITE = (255, 255, 255)  # 白色
        self.mouse_rel_x = 0  # 获得当前鼠标点击位置的x的坐标
        self.mouse_rel_y = 0  # 获得当前鼠标点击位置y的坐标
        self.mouse_x = 0  # 获得当前鼠标实时位置的x的坐标
        self.mouse_y = 0  # 获得当前鼠标实时位置的y的坐标
        self.click_event = False  # 判断当前鼠标点击没有
        self.check_spelling = False  # 判断拼写
        self.pronunciation = False  # 判断是否发音

    # 检查事件，鼠标事件
    def check_Events(self):
        for event in pygame.event.get():  # 获得当前所有得事件
            if event.type == pygame.QUIT:  # 如果退出游戏
                self.Main_Game_Running = False  # 直接退出游戏
            if event.type == pygame.MOUSEBUTTONDOWN:   # 如果鼠标点击了
                self.click_event = True  # 鼠标点击了左键，代表选中了字母
            if event.type == pygame.MOUSEBUTTONUP:  # 如果释放了鼠标
                self.click_event = False  # # 释放了鼠标
            if event.type == pygame.MOUSEMOTION:  # 如果鼠标移动了
                self.mouse_x, self.mouse_y = event.pos  # 获得当前鼠标的位置
                self.mouse_rel_x, self.mouse_rel_y = event.rel  # 获得当前鼠标的位置
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 开始检查单词拼写
                    self.check_spelling = True
                if event.key == pygame.K_q:   # 开始单词发音
                    self.pronunciation = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:  # 结束检查
                    self.check_spelling = False
                if event.key == pygame.K_q:   # 结束发音
                    self.pronunciation = False

    # 保证游戏可以正常运行
    def game_Loop(self):
        if self.Main_Game_Running:
            self.gameplay_time = pygame.time.get_ticks() # 记录游戏运行的时间，很重要，需要控制游戏进程
            self.window.fill(self.BLACK)  # 每次都刷新屏幕
            self.check_Events()  # 获取游戏的事件


# 在游戏开始第一个阶段先展示单词,第一阶段作为一个独立得存在
class ShowWords(object):
    def __init__(self, count_seconds, path, seconds):
        self.show_words_surface = pygame.Surface((1000, 800))  # 设置一个surface,和原来的屏幕一样大
        self.start_time = datetime.now()  # 获取游戏开始的时间
        self.count_seconds = count_seconds  # 倒数秒针
        self.start_countdown = 5  # 游戏开始之前给5秒准备时间
        self.show_all_words_countdown = 95  # 最后展示95秒的所有单词
        self.start_countdown_running = True  # 控制5秒倒计时结束
        self.show_words_running = False  # 控制中间展示单词得时间
        self.show_all_words_running = False  # 控制最后展示单词的时间
        self.show_first_level_running = False  # 控制第一关运行
        self.word_index = 0  # 单词的索引
        self.seconds = seconds  # 给多少时间记忆每个单词
        self.word, self.phonetic, self.word_tra = read_taskwords_xls(path)  # 读取单词，音标， 翻译
        self.RED = (255, 0, 0)   # 红色
        self.GREEN = (0, 255, 0)  # 绿色
        self.BLACK = (0, 0, 0)  # 黑色

    # 游戏开始之前先倒数5秒
    def start_Countdown(self):
        self.show_words_surface.fill(self.BLACK)  # 每次都要刷新屏幕，去掉旧页面，展示新的页面
        if datetime.now() > self.start_time + timedelta(seconds=1):  # 如果已经过了一秒钟
            self.start_time = datetime.now()  # 将现在的时间给旧的时间
            self.start_countdown -= 1   # 将秒数减1
            if self.start_countdown == -1:  # 如果倒数结束
                self.show_words_running = True  # 控制开始展示单词
                self.start_countdown_running = False  # 结束这个倒数页面

        # 显示的倒计时的大小和位置
        draw_Text(self.show_words_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150,
                  str(self.start_countdown),
                  self.RED, 500, 250)

    # 用于开始游戏前的展示
    def show_words(self):
        self.show_words_surface.fill(self.BLACK)   # 每次都要刷新屏幕，去掉旧页面，展示新的页面
        if datetime.now() > self.start_time + timedelta(seconds=1):  # 每过一秒
            self.start_time = datetime.now()   # 将现在的时间给过去的时间
            # 没过10秒20秒发出一次发音
            if self.count_seconds == self.seconds or self.count_seconds == self.seconds/2:
                game_Sound('Pronunciation/three_grade/' + self.word[self.word_index] + '.mp3', 0.2)
            self.count_seconds -= 1  # 倒计时减 1
            if self.count_seconds == -1:  # 如果20秒倒计时结束
                self.word_index += 1   # 换到下一个单词
                self.count_seconds = self.seconds  # 从20秒重新倒数
                if self.word_index > len(self.word) - 1:  # 如果展示结束，所有的都结束
                    self.word_index = 0
                    self.show_words_running = False
                    self.show_all_words_running = True
        draw_Text(self.show_words_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150, str(self.count_seconds),
                  self.RED, 500, 250)

    # 画内容
    def draw_words(self):
        # 画单词
        draw_Text(self.show_words_surface, 'Fonts/arial.ttf', 100, str(self.word[self.word_index]), self.RED, 500, 400)
        # 画音标
        draw_Text(self.show_words_surface, 'Fonts/arial.ttf', 100, str(self.phonetic[self.word_index]), self.RED, 500, 500)
        # 画 汉语意思
        draw_Text(self.show_words_surface, 'Fonts/STKAITI.TTF', 100, str(self.word_tra[self.word_index]), self.RED, 500, 600)

    # 然后展示所有单词95秒
    def draw_all_words(self):
        self.show_words_surface.fill(self.BLACK)  # 每次都要刷新屏幕
        if datetime.now() > self.start_time + timedelta(seconds=1):
            self.start_time = datetime.now()
            self.show_all_words_countdown -= 1
            if self.show_all_words_countdown == -1:  # 如果时间结束，结束所有的运行
                self.show_all_words_running = False
                self.show_first_level_running = True
        draw_Text(self.show_words_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150, str(self.show_all_words_countdown),
                  self.RED, 880, 70)   # 展示秒针
        for i in range(len(self.word)):
            # 展示英文
            draw_Text(self.show_words_surface, 'Fonts/arial.ttf', 40, str(self.word[i]), self.RED, 100, (i+1)*70)
            # 展示音标
            draw_Text(self.show_words_surface, 'Fonts/Lucida-Sans-Unicode.ttf', 40, str(self.phonetic[i]), self.RED, 400,
                  (i+1)*70)
            # 展示翻译
            draw_Text(self.show_words_surface, 'Fonts/STKAITI.TTF', 40, str(self.word_tra[i]), self.RED, 700,
                  (i+1)*70)


# 因为要设置难度关卡，所以最好也弄一个类，互不干扰
class FirstLevel(object):
    def __init__(self, path):
        self.first_level_surface = pygame.Surface((1000, 800))  # 设置一个surface,和原来的屏幕一样大
        self.first_level_running = False # 第一关不运行
        self.BLUE = (0, 0, 255)  # 定义一个绿色，主要是字母用
        self.BLACK = (0, 0, 0)  # 屏幕背景为黑色
        self.WHITE = (255, 255, 255)  # 设置一个白色
        self.letter_coordinate = {}  # 这里面放字母 及其对应的坐标
        self.current_word_length = 0  # 当前字母的长度
        self.BLOCK_SIZE = 90  # 设置框的大小
        self.current_word = 0  # 当前任务单词
        self.current_words_list, self.current_phonetic, self.current_translation = read_taskwords_xls(path)
        self.Blocks_Rect = 0  # 初始化框框的列表
        self.Blocks_Surface = 0  # 初始化要画的框框
        self.font = pygame.font.Font('Fonts/arial.ttf', 50)  # 得到想要用的字体，以及字体的大小
        self.current_chance = 0
        # 当前是第几次机会

    # 该函数的作用是将单词拆分为字母，以后加入混淆的字母，并固定其初始的位置，每个单词都需要运行一次
    def split_Word(self, word):  # 首先输入一个单词
        letter_list = []  # 创建一个列表准备读取单词的字母
        self.current_word_length = len(word)  # 获得当前单词的长度
        self.current_word = word  # 获得当前字母的拼写
        for letter in word:  # 循环读取字母
            letter_list.append(letter)  # 将字母加入到列表中,如果有迷惑字母也要加进去
        random.shuffle(letter_list)  # 将里面加入列表的字母的顺序随机打乱
        letter_x = 0  # 横坐标从0开始
        letter_y = 30  # 纵坐标从30开始
        increase = 70  # 字母与字母之间的间距为70
        for i in range(len(letter_list)):  # 循环字母的个数
            coordinate = [letter_x, letter_y]  # 每个字母的坐标都需要重新刷新
            letter_x += increase
            self.letter_coordinate[letter_list[i]+'_'+str(i)] = coordinate  # 因为重复字母在字典里不能存在，没办法

    # 该函数的作用是将所有的字母画到主屏幕上
    def draw_Letters(self):
        for key, coordinate in self.letter_coordinate.items():  # 循环字母及其坐标
            letter_surface = pygame.Surface((60, 60))  # 创建一个surface把字母放进去
            letter_surface.fill((255, 0, 0))  # 将背景填充为红色
            letter = key.split('_')[0]
            text_surface = self.font.render(letter, True, self.BLUE)  # 要写的文本，以及字体颜色
            text_rect = text_surface.get_rect()  # 相当于给当前的surface 框起来 这样比较容易获得和使用参数
            letter_surface.blit(text_surface, (30 - text_rect.width / 2, 30 - text_rect.height / 2))  # 将字母放在中间
            self.first_level_surface.blit(letter_surface, (coordinate[0], coordinate[1]))  # 控制画到游戏屏幕的位置

    # 实现画表格的功能, 在画线之前，要判断本次的单词的字母数，以及本关的难度
    def draw_Blocks(self, Chance_Number):
        self.first_level_surface.fill(self.BLACK)
        self.Blocks_Rect = [[] for i in range(Chance_Number)]  # 按照行和列把每一个格都框起来
        self.Blocks_Surface = pygame.Surface((self.current_word_length*self.BLOCK_SIZE, Chance_Number*self.BLOCK_SIZE))  # 创建一个屏幕
        self.Blocks_Surface.fill((255, 255, 255))  # 填充屏幕的颜色
        # 这个循环是画横线的，代表的是给多少次机会
        for j in range(1, Chance_Number, 1):
            pygame.draw.line(self.Blocks_Surface, (0, 200, 0), (0, j*self.BLOCK_SIZE), (self.current_word_length*self.BLOCK_SIZE, j*self.BLOCK_SIZE), 1)
        # 这个循环是画竖线的，代表的是这个单词有多少个字母
        for i in range(1, self.current_word_length, 1):
            pygame.draw.line(self.Blocks_Surface, (0, 200, 0), (i*self.BLOCK_SIZE, 0), (i*self.BLOCK_SIZE, Chance_Number*self.BLOCK_SIZE), 1)
        # 获得每一个格子的Rect并存入列表中
        for j in range(Chance_Number):
            for i in range(self.current_word_length):
                self.Blocks_Rect[j].append(pygame.Rect(i*self.BLOCK_SIZE, j*self.BLOCK_SIZE, self.BLOCK_SIZE, self.BLOCK_SIZE))

    # 颜色和位置，必须锁定当前的拼写，不随字母的移动而改变的方式，然后画图，还得一直显示在屏幕上
    def indicator_Spelling(self, player_spelling, chance):
        for index in range(len(self.current_word)):  # 一个字母一个字母判断
            if player_spelling[index] not in self.current_word:  # 如果不在单词中
                fill_surface = pygame.Surface((90, 90))
                fill_surface.fill((200, 200, 200))
                text_surface = self.font.render(player_spelling[index], True, self.BLUE)  # 要写的文本，以及字体颜色
                text_rect = text_surface.get_rect()  # 相当于给当前的surface 框起来 这样比较容易获得和使用参数
                fill_surface.blit(text_surface, (30 - text_rect.width / 2, 30 - text_rect.height / 2))  # 将字母放在中间
                self.Blocks_Surface.blit(fill_surface, (index * 90, chance*90))
            elif player_spelling[index] == self.current_word[index]:  # 如果在正确的位置
                fill_surface = pygame.Surface((90, 90))
                fill_surface.fill((0, 255, 0))
                text_surface = self.font.render(player_spelling[index], True, self.BLUE)  # 要写的文本，以及字体颜色
                text_rect = text_surface.get_rect()  # 相当于给当前的surface 框起来 这样比较容易获得和使用参数
                fill_surface.blit(text_surface, (30 - text_rect.width / 2, 30 - text_rect.height / 2))  # 将字母放在中间
                self.Blocks_Surface.blit(fill_surface, (index * 90, chance*90))
            else:
                fill_surface = pygame.Surface((90, 90))
                fill_surface.fill((255, 0, 0))
                text_surface = self.font.render(player_spelling[index], True, self.BLUE)  # 要写的文本，以及字体颜色
                text_rect = text_surface.get_rect()  # 相当于给当前的surface 框起来 这样比较容易获得和使用参数
                fill_surface.blit(text_surface, (30 - text_rect.width / 2, 30 - text_rect.height / 2))  # 将字母放在中间
                self.Blocks_Surface.blit(fill_surface, (index * 90, chance*90
                                                        ))

    def letters_in_Rect(self):
        for key, coordinate in self.letter_coordinate.items():
            print(coordinate)
            contact_rect = letter_in_rect(coordinate[0], coordinate[1], self.Blocks_Rect[0], 0, 200)
            self.contacts_list.append(contact_rect)

    def pronunciation(self):
        pygame.mixer.music.load('Pronunciation/three_grade/' + self.current_word + ".mp3")
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()


# 在游戏里面写一些文字
def draw_Text(surface, font_path, size, text, font_color, center_x, center_y):
    font = pygame.font.Font(font_path, size)  # 得到想要用的字体，以及字体的大小
    text_surface = font.render(text, True, font_color)  # 要写的文本，以及字体颜色
    text_rect = text_surface.get_rect()  # 相当于给当前的surface 框起来 这样比较容易获得和使用参数
    text_rect.center = (center_x, center_y)  # 文本要显示的位置
    surface.blit(text_surface, text_rect)


# 取得本次在词库中的所有单词，音标和翻译
def read_taskwords_xls(path):
    words = []
    ci_xing = []
    words_tra = []
    # open workbook
    workbook = xlrd.open_workbook(path)
    # get all sheets by sheet names
    sheets = workbook.sheet_names()
    # get the first sheet
    worksheet = workbook.sheet_by_name(sheets[0])
    # 获得单词的行数
    words_numbers = worksheet.nrows
    # 顺序获得选中单词的英文与中文
    for word_index in range(words_numbers):
        # get the correspond content
        words.append(worksheet.cell_value(word_index, 0))
        # if word in words
        ci_xing.append(worksheet.cell_value(word_index, 1))
        words_tra.append(worksheet.cell_value(word_index, 2))
    return words, ci_xing, words_tra


# 因为背景音乐的控制就一句话，所以在每个游戏中直接使用pygame.mixer.music里面 load, play(-1), pause, unpause stop,控制就行
# pygame.mixer.sound 是用来控制极短的声音，属于独立的游戏模块
def game_Sound(game_sound_path, volume):
    pygame.init()
    pygame.mixer.music.load(game_sound_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play()


# 判断鼠标是否和图形触碰
def is_in_rect(pos, rect):
    mouse_x, mouse_y = pos  # 获得鼠标的坐标
    rect_x, rect_y, rect_w, rect_h = rect   # 获得当前这个正方形的属性
    if (rect_x <= mouse_x <= rect_x + rect_w) and (rect_y <= mouse_y <= rect_y + rect_h):  # 判断是否在里面
        return True  # 在里面就返回真
    else:
        return False  # 不在里面就返回假


# 判断字母有没有放到框框当中
def letter_in_rect(letter_coordinate_x, letter_coordinate_y, rect_list, relative_x, relative_y):
    for rect in rect_list:
        if (letter_coordinate_x > (rect.x + relative_x)) and ((letter_coordinate_x+60) < (rect.x + 90 + relative_x)) and \
                (letter_coordinate_y > (rect.y + relative_y)) and ((letter_coordinate_y+60) < (rect.y+ 90+ relative_y)):
            return rect


# 倒计时答题的时间
def answer_Countdown(surface,spelling_start_time, countdown_number):
    if datetime.now() > spelling_start_time + timedelta(seconds=1): # 每过一秒钟
        spelling_start_time = datetime.now()
        countdown_number -= 1
        # 展示秒针