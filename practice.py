'''

切换到下一个任务，有几个条件
1:  回答正确时候的场景，回答错误时候的场景，都要展示正确的单词的拼写
2： 分数系统，如何加减分数
4： 累计节省的时间可以换为分数
5： 单词循环结束是切换到下一关

'''


from engine import *
import copy


g = MainGame(1000, 800)  # 首先展示一个屏幕,这个是主游戏界面
# 设置单词以及倒数的时间 这个函数仅仅在第一阶段展示用，自成体系
SHOW_WORDS = ShowWords(5, 'words_pool/three_grade/three_grade_known.xls', 5)

FIRST_LEVEL = FirstLevel('words_pool/three_grade/three_grade_known.xls')  # 定义一个第一关的类

FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[0])
letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标

letter_contact = False  # 如果没有触碰到单词
contact_rect_list = []  # 每一轮都看几个碰了
first_chance_spelling = ''
used_chance = []  # 已经用了哪些机会
used_spelling = []  # 已经用了哪些机会
current_task = 0  # 当前是第几个任务
spelling_start_time = datetime.now()   # 获得游戏开始的时间
spelling_countdown_number = 60  # 答题时间
while g.Main_Game_Running:  # 主游戏在运行

    g.game_Loop()  # 调用函数
    if g.pronunciation:  # 这个控制单词发音
        FIRST_LEVEL.pronunciation()
    '''
    if SHOW_WORDS.start_countdown_running:  # 先倒数5秒，准备开始
        SHOW_WORDS.start_Countdown()
        g.window.blit(SHOW_WORDS.show_words_surface, (0, 0))
    if SHOW_WORDS.show_words_running:  # 然后展示单词
        SHOW_WORDS.show_words()
        SHOW_WORDS.draw_words()
        g.window.blit(SHOW_WORDS.show_words_surface, (0, 0))
    if SHOW_WORDS.show_all_words_running:  # 最后让记忆一次
        SHOW_WORDS.draw_all_words()
        g.window.blit(SHOW_WORDS.show_words_surface, (0, 0))
    '''
    # if SHOW_WORDS.show_first_level_running:
    if True:

        FIRST_LEVEL.draw_Blocks(3)  # 画表格，参数的意思是给三次机会，所以有三行

        if g.check_spelling and len(current_spelling) == len(FIRST_LEVEL.current_word): # 如果已经拼写完毕，才能按enter检查拼写
            first_chance_spelling = copy.deepcopy(current_spelling)  # 复制当前玩家的拼写
            used_chance.append(FIRST_LEVEL.current_chance)  # 将当前使用的机会行加入到已经使用过的机会中
            used_spelling.append(first_chance_spelling)     # 将玩家的历史拼写写入到一个列表中
            show_indicator_time = g.gameplay_time  # 记录按下enter得时间，为了以后再展示答案几秒钟
            FIRST_LEVEL.current_chance += 1  # 将机会加 1
            if FIRST_LEVEL.current_chance == 3:  # 如果机会已经使用完
                FIRST_LEVEL.current_chance = 2  # 让机会的次数一直等于第三次机会
            # 检查完把坐标送回到原来的坐标，重新开始拼写
            for key in FIRST_LEVEL.letter_coordinate.keys():
                FIRST_LEVEL.letter_coordinate[key][0] = letter_original_coordinate[key][0]  # 横坐标
                FIRST_LEVEL.letter_coordinate[key][1] = letter_original_coordinate[key][1]  # 纵坐标

        #  展示答题倒计时
        if datetime.now() > spelling_start_time + timedelta(seconds=1):  # 每过一秒
            spelling_start_time = datetime.now()  # 将当前的时间给旧时间
            if first_chance_spelling != FIRST_LEVEL.current_word: # 如果拼写错误，要惩罚时间
                spelling_countdown_number -= 1  # 将时间减1

        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150,
                  str(spelling_countdown_number), (255, 0, 0), 880, 70)  # 将剩余的时间画到屏幕上

        if first_chance_spelling:  # 如果玩家已经有了拼写答案
            for i in used_chance:  # 将所有的答案画到表格对应的位置
                FIRST_LEVEL.indicator_Spelling(used_spelling[i], used_chance[i])

            # 如果是拼写正确，展示正确得单词5秒再切换到下一个单词，并将该reset的参数全部reset
            if first_chance_spelling == FIRST_LEVEL.current_word and g.gameplay_time > show_indicator_time + 5000:
                spelling_countdown_number += 60  # 到了下一个单词重新倒计时60秒
                FIRST_LEVEL.letter_coordinate = {}
                current_task += 1  # 这块有一个问题，可能会超出边界
                FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []
                used_chance = []
                FIRST_LEVEL.current_chance = 0
            # 如果拼写不正确，而且所有的机会都已经用完了
            if len(used_spelling) == 3 and used_spelling[FIRST_LEVEL.current_chance] != FIRST_LEVEL.current_word \
                    and g.gameplay_time > show_indicator_time + 5000:
                spelling_countdown_number += 60  # 到了下一个单词重新倒计时60秒
                FIRST_LEVEL.letter_coordinate = {}
                current_task += 1  # 这块有一个问题，可能会超出边界
                FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []
                used_chance = []
                FIRST_LEVEL.current_chance = 0




        FIRST_LEVEL.first_level_surface.blit(FIRST_LEVEL.Blocks_Surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
        FIRST_LEVEL.draw_Letters()  # 把本次所有用到的字母都画到屏幕上
        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/Lucida-Sans-Unicode.ttf', 100,
                  FIRST_LEVEL.current_phonetic[current_task],
                  FIRST_LEVEL.WHITE, 200, 600)
        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/STKAITI.TTF', 100,
                  FIRST_LEVEL.current_translation[current_task],
                  FIRST_LEVEL.WHITE, 200, 700)

        g.window.blit(FIRST_LEVEL.first_level_surface, (0, 0))  # 将该页面画到屏幕上

        if not letter_contact:  # 如果目前没有接触到字母
            for current_letter_key in FIRST_LEVEL.letter_coordinate.keys():  # 循环列表里所有的字母
                # 如果鼠标选中了这个字母，并且点击了鼠标
                if is_in_rect((g.mouse_x, g.mouse_y), (FIRST_LEVEL.letter_coordinate[current_letter_key][0],
                                                       FIRST_LEVEL.letter_coordinate[current_letter_key][1], 60,
                                                       60)) and g.click_event:
                    letter_contact = True  # 选中了这个单词

                    break  # 只要选中了就不循环了

        if letter_contact:  # 如果已经选择了一个单词，那么图片就要随着鼠标移动
            FIRST_LEVEL.letter_coordinate[current_letter_key][0] = g.mouse_x - 30 + g.mouse_rel_x  # 移动X坐标
            FIRST_LEVEL.letter_coordinate[current_letter_key][1] = g.mouse_y - 30 + g.mouse_rel_y  # 移动Y坐标

        if not g.click_event:  # 如果松开了鼠标
            letter_contact = False  # 就需要继续循环找下一个被选中的字母是什么
            # 看看单词有没有放到框框里
            contact_rect = letter_in_rect(FIRST_LEVEL.letter_coordinate[current_letter_key][0],
                                          FIRST_LEVEL.letter_coordinate[current_letter_key][1],
                                          FIRST_LEVEL.Blocks_Rect[FIRST_LEVEL.current_chance], (7 - 7) * 45, 200)

            if contact_rect:  # 如果放到框里面了，这时已经确定放进去了,那我要得到它得字母
                # 如果此时的列表为空,将这个框加进去
                if not contact_rect_list:
                    # 那么就将坐标改为框框里
                    FIRST_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                    FIRST_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                    contact_rect_list.append(contact_rect)  # 并将这个位置加到列表中
                # 已经是最后一个字母,只加一个
                elif current_letter_key == list(FIRST_LEVEL.letter_coordinate.keys())[-1]:  # 如果一直是最后一个字母
                    FIRST_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                    FIRST_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                    if contact_rect not in contact_rect_list:  # 别重复加坐标
                        contact_rect_list.append(contact_rect)
                else:  # 如果没有重复，那么就放进去
                    if pygame.Rect.collidelist(contact_rect, contact_rect_list) == -1:
                        FIRST_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                        FIRST_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                        contact_rect_list.append(contact_rect)
                    else:  # 如果坐标重复，就回到原来的位置
                        FIRST_LEVEL.letter_coordinate[current_letter_key][0] = \
                            letter_original_coordinate[current_letter_key][0]
                        FIRST_LEVEL.letter_coordinate[current_letter_key][1] = \
                            letter_original_coordinate[current_letter_key][1]
            else:  # 不在框框内就回到原来得坐标
                FIRST_LEVEL.letter_coordinate[current_letter_key][0] = letter_original_coordinate[current_letter_key][0]
                FIRST_LEVEL.letter_coordinate[current_letter_key][1] = letter_original_coordinate[current_letter_key][1]
    # 这个循环的目的是为了删除不在框中的坐标,并得到当前的拼写
    current_block_letter_rect = []
    current_spelling_dic = {}  # 记录玩家得单词拼写的字典
    current_spelling = ''  # 记录玩家当前的拼写
    for key, coordinate in FIRST_LEVEL.letter_coordinate.items():
        current_block_letter = letter_in_rect(coordinate[0], coordinate[1],
                                      FIRST_LEVEL.Blocks_Rect[FIRST_LEVEL.current_chance], (7 - 7) * 45, 200)
        # 得到在框内的坐标
        if current_block_letter:
            current_block_letter_rect.append(current_block_letter)
            current_spelling_dic[coordinate[0]] = key
    # 下面的循环是为了得到拼写
    for index in sorted(current_spelling_dic):
        current_spelling += current_spelling_dic[index].split('_')[0]  # 得到玩家的拼写
    for i in contact_rect_list:  # 循环之前加入的坐标
        if i not in current_block_letter_rect:  # 如果这个坐标不在放在框中的坐标，那么将它删除
            contact_rect_list.remove(i)
    pygame.display.update()

'''
# 游戏字体一体化
CHINESE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 25)  # show the Chinese fonts on the display
SCORE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 50)  # show the score on the display
OTHER_FONT = pygame.font.Font('Fonts/arial.ttf', 25)  # show  English font on the display
PHONETIC_FONT = pygame.font.Font('Fonts/Lucida-Sans-Unicode.ttf', 25)  # show the phonetic font on the display
# import necessary packages
from English_Vocabulary_Review import English_review
from Snake_body_library import *
from game_introducation import *
import time, datetime, sys
from words_handling_library import *
from words_phonetic_library import get_word_pho
import pygame_menu


# ------------------------------------------------------------------------------------------
# 定义一些全局变量，以及全局要使用的东西
t0 = time.perf_counter()  # 游戏运行开始计时为 0，为了计算玩家玩了多长时间
current_score = 0  # 玩家每轮游戏得多少分
current_remembered_words = 0  # 结束游戏之前，玩家一共记了多少单词
# 总记忆单词数，总共玩游戏的时间，历史最高得分，历史最高记忆的单词数
total_remembered_words, total_spent_words, highest_score, highest_words = \
    read_excel_game_record('saved_files/game_record.xls')
record_list = [total_remembered_words, total_spent_words, highest_score, highest_words]  # 把读出的记录放到一个列表中
# 初始化本轮游戏已经记忆的单词列表（英文）
words_list_known = []
# 初始化本轮游戏已经记忆的单词列表（汉语）
task_words_known = []
# 初始化玩家的拼写
player_spelling = []
# 要记录这个单词已经拼写到哪了
spell_list = list()
# 要记录玩家已经练习多少个单词了，要是练习玩了要游戏结束
words_number = 0
# 追踪蛇已经吃的字母，正确和错误都要记录
eating_spelling = list()
# 游戏结束开关
game_over = False
# ------------------------------------------------------------------------------------------

# 对游戏屏幕，标题，字体的初始化
screen_grid_width = 22  # 设置屏幕宽有多少30像素
screen_grid_high = 22  # 设置屏幕高有多少30像素
pygame.init()  # initialize some modules
# set the width and height of window
screen = pygame.display.set_mode((FRAME_WIDTH * screen_grid_width, FRAME_WIDTH * screen_grid_high))
pygame.display.set_caption("English Vocabulary Practice")  # set screen caption
# 游戏字体一体化
CHINESE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 25)  # show the Chinese fonts on the display
SCORE_FONT = pygame.font.Font('Fonts/STKAITI.TTF', 50)  # show the score on the display
OTHER_FONT = pygame.font.Font('Fonts/arial.ttf', 25)  # show  English font on the display
PHONETIC_FONT = pygame.font.Font('Fonts/Lucida-Sans-Unicode.ttf', 25)  # show the phonetic font on the display


# ------------------------------------------------------------------------------------------
# 在每一轮游戏结束之后都要保存游戏记录，并清除已经保存得记录
def save_game_record():
    global total_spent_words, words_list_known, task_words_known
    player_played_game = (time.perf_counter() - t0) / 60
    # 记录本论游戏玩家的游戏记录：1： 玩游戏的日期 2：玩家玩了多长时间
    review_list = [str(datetime.date.today()), round(player_played_game, 2), current_score, current_remembered_words]
    total_spent_words += player_played_game
    # 总共记忆的单词，和总的游戏时间
    record_list[0] = total_remembered_words + current_remembered_words
    record_list[1] = total_spent_words
    write_excel_game_review('saved_files/game_review.xls', review_list)
    write_excel_game_record('saved_files/game_record.xls', record_list)
    # 原单词表中删除已经记住的单词
    delete_taskwords_xls(word_file_path, words_list_known)
    # 英语单词，和翻译都要写进已经记住的单词库里面
    write_knownwords_xls(word_review_file_path, words_list_known, task_words_known)
    words_list_known = []  # 本轮游戏已经记忆的单词列表清零 （英语）
    task_words_known = []  # 本轮游戏已经记忆的单词列表清零（汉语）


def game_init():
    # global variate
    global snake, snake_speed, background_music_setting, track_spelling_setting, train_words_number, alphabet, alphabet_group, \
        wrong_words_num_setting, words_phonetic_setting, tip_show_setting, train_words_num_setting, words_list, word_file_path, \
        phonetic_file_path, pronunciation_file_path, word_review_file_path, continuous_correct_alphabet, task_words
    # -------------------------------------------------------------------------------------------------------
    # 第一页的菜单，背景和标题背景都会有默认值很丑，所以这句话的意思是给他全部弄成透明的就不会在游戏上显示了
    mytheme_fix = pygame_menu.themes.Theme(background_color=(0, 0, 0, 0), title_background_color=(0, 0, 0, 0))
    # 实例化第一层菜单
    game_fix_menu = pygame_menu.Menu(400, 400, '', theme=mytheme_fix, menu_position=(80, 60))
    # 第二层菜单的位置和大小
    game_first_mune = pygame_menu.Menu(400, 200, '', theme=mytheme_fix, menu_position=(65, 60))

    # 设置本次训练的单词个数
    train_words_num_setting = game_fix_menu.add_text_input('单词数(10-20): ', default='10', font_name='Fonts/STKAITI.TTF',
                                                           selection_color=(255, 0, 0), background_color=(0, 255, 0))
    # 进入游戏
    game_fix_menu.add_button('进入游戏', game_first_mune, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                             selection_color=(255, 0, 0))
    # -------------------------------------------------------------------------------------------------------
    # 游戏设置里面的所有菜单
    myimage = pygame_menu.baseimage.BaseImage('Game_Pictures/game_intro.jpg')
    mytheme = pygame_menu.themes.Theme(background_color=myimage, title_background_color=(0, 0, 0, 0),
                                       title_font_color=(255, 0, 0))
    game_setting_mune = pygame_menu.Menu(FRAME_WIDTH * screen_grid_width, FRAME_WIDTH * screen_grid_high, '',
                                         theme=mytheme, menu_id='game_setting')

    # 设置干扰选项
    wrong_words_num_setting = game_setting_mune.add_text_input('干扰选项(1-2): ', default='1',
                                                               font_name='Fonts/STKAITI.TTF',
                                                               selection_color=(255, 0, 0))

    # 蛇的移动速度设置
    snake_speed = game_setting_mune.add_text_input('蛇的移动速度(100-800): ', default='200', font_name='Fonts/STKAITI.TTF',
                                                   textinput_id='snake_speed', selection_color=(255, 0, 0))
    # 有无字母追踪
    track_spelling_setting = game_setting_mune.add_selector('拼写追踪', [('YES', screen), ('NO', screen)],
                                                            font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 有无背景音乐
    background_music_setting = game_setting_mune.add_selector('背景音乐', [('YES', screen), ('NO', screen)],
                                                              font_name='Fonts/STKAITI.TTF',
                                                              selection_color=(255, 0, 0))
    # 有无提示
    tip_show_setting = game_setting_mune.add_selector('单词提示', [('YES', screen), ('NO', screen)],
                                                      font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 有无音节
    words_phonetic_setting = game_setting_mune.add_selector('单词音节', [('YES', screen), ('NO', screen)],
                                                            font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # 保存设置，并返回上一级菜单
    game_setting_mune.add_button('保存并返回', pygame_menu.events.BACK,
                                 font_name='Fonts/STKAITI.TTF', selection_color=(255, 0, 0))
    # ------------------------------------------------------------------------------------------------------------------
    # 第二页里面的选项
    game_first_mune.add_button('复习模式', English_review, screen, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))
    game_first_mune.add_button('开始游戏', main_game, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏设置', game_setting_mune, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏记录', game_record, screen, CHINESE_FONT, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('游戏帮助', game_intro, screen, CHINESE_FONT, font_name='Fonts/STKAITI.TTF',
                               background_color=(0, 255, 0), selection_color=(255, 0, 0))
    game_first_mune.add_button('结束游戏', sys.exit, 0, font_name='Fonts/STKAITI.TTF', background_color=(0, 255, 0),
                               selection_color=(255, 0, 0))
    snake = Snake_body_Sprite()  # 初始化蛇头，还有蛇会的一些动作
    # 创建一个正确单词的组
    alphabet_group = pygame.sprite.Group()
    alphabet = MySprite_food()
    alphabet.load_multi_frames("Game_Pictures/lower_letter.png", FRAME_WIDTH, FRAME_WIDTH, 13)
    alphabet_group.add(alphabet)
    game_bgp = pygame.image.load(
        "Game_Pictures/Snake_Begin_UI.png").convert_alpha()  # load the background of first menu
    # 有时候图片太大，需要调整图片大小符合目标屏幕大小
    game_bgp = pygame.transform.scale(game_bgp, (FRAME_WIDTH * screen_grid_width, FRAME_WIDTH * screen_grid_high))
    # ------------------------------------------------------------------------------------------------------------------
    # 抓举菜单里所有的更新选项，并且第一次读取要学习的单词列表
    menu_running = True
    while menu_running:
        screen.blit(game_bgp, (0, 0))
        if train_words_num_setting.get_selected_time():
            train_words_number = game_play_setting(train_words_num_setting)
            # 选择本轮要学习的单词
            word_file_path = 'words_pool/three_grade/three_grade_unknown.xls'
            phonetic_file_path = 'Words_phonetic/three_grade/three_grade_phonetic.xls'
            pronunciation_file_path = 'Speech_EN/three_grade/'
            word_review_file_path = 'words_pool/three_grade/three_grade_known.xls'
            # 得到单词，和翻译 是分开的
            words_list, task_words = read_taskwords_xls(word_file_path, train_words_number)
            # 这是一个字典 第几个单词-第几个字母：以及对应单词的字母索引
            continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)
        # 获得当前所有事件
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        game_fix_menu.update(events)  # 抓取菜单的改变
        game_fix_menu.draw(screen)  # 将改变后的菜单画到桌面上
        pygame.display.update()  # 整个游戏更新


# define pause and continue game
def checkquit(events):
    global pause, main_game_running, player_spelling, game_over, words_list, \
        task_words, current_score, continuous_correct_alphabet, alphabet_group, alphabet
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_game_running = False
                # 如果第一轮学习已经结束，重新读取单词列表
                if game_over:
                    player_spelling = []
                    current_score = 0  # 每一轮学习结束，分数清零
                    # 得到单词，和翻译 是分开的
                    words_list, task_words = read_taskwords_xls(word_file_path, train_words_number)
                    # 这是一个字典 第几个单词-第几个字母：以及对应单词的字母索引
                    continuous_correct_alphabet = built_spelling_dic(words_list, ALPHABET_LIST)
                    # 创建一个正确单词的组
                    alphabet_group = pygame.sprite.Group()
                    alphabet = MySprite_food()
                    alphabet.load_multi_frames("Game_Pictures/lower_letter.png", FRAME_WIDTH, FRAME_WIDTH, 13)
                    alphabet_group.add(alphabet)
            elif event.key == pygame.K_p:
                pause = False
            elif event.key == pygame.K_SPACE:
                pause = True
            elif event.key == pygame.K_q:
                word_pro = words_list[int(alphabet.current_word_number) - 1]
                pygame.mixer.music.load(pronunciation_file_path + word_pro + ".mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()


def main_game():
    global highest_words, highest_score, continuous_correct_alphabet, \
        pause, record_list, words_list_known, task_words_known, eating_spelling, words_number, \
        current_score, alphabet, task_words, spell_list, player_spelling, game_over, \
        current_remembered_words, main_game_running, words_list, \
        phonetic_file_path, pronunciation_file_path, word_review_file_path

    game_over = False  # 游戏结束开关

    # ------------------------------------------------------------------------------------------------------------------
    # 每次重新进入游戏都要知道玩家进行了什么设置
    # 得到BGM的设置是什么
    snake_moving_speed = game_play_setting(snake_speed)  # 得到玩家设置的蛇的移动速度
    bgm = game_play_setting(background_music_setting)
    if bgm[0][0] == 'YES':
        pygame.mixer.stop()  # 先得把开始设置的那个背景音乐停止
        game_audio("game_sound/bgm.wav", volumn=0.3, times=-1)  # 才能开始新的，不然就会有双重奏乐
    # 静音游戏背景音乐
    elif bgm[0][0] == 'NO':
        pygame.mixer.stop()
    # 单词提示 ‘yes’ 'no'
    prompt_show = game_play_setting(tip_show_setting)
    # 拼写追踪 ‘yes’ 'no'
    track_spelling = game_play_setting(track_spelling_setting)
    # 有无音节 ‘yes’ 'no'
    word_phone = game_play_setting(words_phonetic_setting)
    # 迷惑字母个数
    wrong_letters_num = int(game_play_setting(wrong_words_num_setting))
    # 默认需要提示，然后设置一个精灵库 在这里修改字母照片
    if prompt_show[0][0] == 'YES':
        # create tip sprite
        tip_group = pygame.sprite.Group()
        tip = MySprite_food()
        tip.load_multi_frames("Game_Pictures/health.png", FRAME_WIDTH, FRAME_WIDTH, 1)
        tip_group.add(tip)
    # 根据迷惑单词个数创造精灵
    random_alphabet_group = pygame.sprite.Group()
    for i in range(wrong_letters_num):
        random_alphabet = MySprite_food()
        random_alphabet.load_multi_frames("Game_Pictures/lower_letter.png", FRAME_WIDTH, FRAME_WIDTH, 13)
        random_alphabet_group.add(random_alphabet)
    # ------------------------------------------------------------------------------------------------------------------
    # 游戏基本参数的设置
    pause = False  # 是否暂停
    # 下面这两个参数完全是为了避免出现的精灵位置和蛇偶然重叠
    food_snake_conflict = False
    count = 0
    # 下面的参数是为了设置提示
    tip_time = 0
    tip_show = False
    # 玩家有没有用提示？
    tip_use = False
    # 控制蛇头那个分数的展示
    score_show_time = 0
    score_show = False
    correct_increase = False
    wrong_decrease = False
    tip_decrease = False
    # 主要是控制结束的那个声音，不然游戏结束了那个声音会一直响
    write_button = False
    # 总的游戏执行程序
    main_game_running = True

    while main_game_running:
        # game clock
        timer = pygame.time.Clock()
        # how many frames in 1S
        timer.tick(60)
        # get kinds of events
        events = pygame.event.get()
        checkquit(events)
        # 记录游戏运行的时间，很重要，需要控制游戏进程
        gameplay_time = pygame.time.get_ticks()
        # 得到玩家的最高分数和最高单词记录
        record_list[2] = highest_score
        record_list[3] = highest_words
        # 画游戏的网格背景
        grid_bg = pygame.image.load("Game_Pictures/grid_bgb.png").convert_alpha()
        screen.blit(grid_bg, (0, 180))
        # 最高分数和最高单词记录
        if current_score > int(highest_score):
            highest_score = current_score
        if current_remembered_words > int(highest_words):
            highest_words = current_remembered_words
        # 一轮游戏结束， 改变一些参数，并保存记录
        if words_number == len(task_words):
            game_over = True  # 游戏结束，显示游戏结束的内容
            words_number = 0  # 记住的游戏单词也清零
            write_button = True
            save_game_record()  # 保存游戏记录
        # 当游戏暂停的时候显示的东西
        if pause:
            pygame.mixer.pause()  # Pause BGM
            pause_pic = pygame.image.load("Game_Pictures/pause.png").convert_alpha()
            screen.blit(pause_pic, (150, 400))

        # --------------------------------------------------------------------------------------------------------------
        # 如果没有暂停
        else:
            pygame.mixer.unpause()  # 解除音乐暂停
            x = snake.segments[0].x_coordinate // 30  # 得到蛇头所在的x的坐标
            y = snake.segments[0].y_coordinate // 30  # 得到蛇头所在的y的坐标
            # 触碰到墙的会从另外的一面出来
            if x < 0:
                snake.segments[0].x_coordinate = 21 * 30
            elif x >= 22:
                snake.segments[0].x_coordinate = 0
            elif y < 6:
                snake.segments[0].y_coordinate = 21 * 30
            elif y >= 22:
                snake.segments[0].y_coordinate = 30 * 6
            # 控制蛇的方向
            for event in events:
                if 0 <= x <= 22 and 6 <= y <= 22:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w and snake.velocity.second_variate != 1:  # up
                            snake.velocity = two_Variate(0, -1)
                        elif event.key == pygame.K_s and snake.velocity.second_variate != -1:  # down
                            snake.velocity = two_Variate(0, 1)
                        elif event.key == pygame.K_a and snake.velocity.first_variate != 1:  # left
                            snake.velocity = two_Variate(-1, 0)
                        elif event.key == pygame.K_d and snake.velocity.first_variate != -1:  # right
                            snake.velocity = two_Variate(1, 0)
            snake_head_direction(snake, snake.velocity)  # 获得蛇的行动方向
            snake.snake_head.head_update(gameplay_time, 100)  # 蛇的更新
            # ----------------------------------------------------------------------------------------------------------
            # 如何没有没有暂停，如果游戏没有结束
            if not game_over:
                # 游戏没有结束，必须先判断坐标有没有重叠
                while not food_snake_conflict:
                    # 得到蛇头的坐标
                    snake_head_x_coordinate = snake.snake_head.x_coordinate
                    snake_head_y_coordinate = snake.snake_head.y_coordinate
                    # 在这里修改要添加字母的个数，随机位置首先不能刚好在蛇头那个方向上，会误吃
                    x_position_list, y_position_list = food_random_position(snake_head_x_coordinate,
                                                                            snake_head_y_coordinate,
                                                                            wrong_letters_num + 2)
                    # 生成的位置同样不能在蛇的身上
                    food_position, snake_position = snake.snake_position(x_position_list, y_position_list)
                    # 将所有的坐标和蛇所有的坐标进行比对
                    for i in food_position:
                        # if not go on
                        if i not in snake_position:
                            count += 1
                        # if so, get new position
                        else:
                            count = 0
                            break
                    # 当所有的坐标和蛇都不重叠
                    if count == wrong_letters_num + 2:
                        food_snake_conflict = True
                # reset，这两个参数完全是为了上面的避免重叠服务
                food_snake_conflict = False
                count = 0

                # 首先更新提示
                if prompt_show[0][0] == 'YES':
                    tip.tip_update(1, 0, x_position_list, y_position_list)
                # 还没吃的时候要先更新，但是当更新一次之后，后面就不在更新了，因为在更新代码里时间卡住了
                alphabet.target_update(continuous_correct_alphabet, 1, 0, x_position_list, y_position_list)
                # 保证错误字母不会和正确的字母一样，也不能互相相同
                wrong_letters_image = [1, 1]
                while len(wrong_letters_image) != len(set(wrong_letters_image)):
                    wrong_letters_postion = 2  # 每生成一个错误字母，都要在坐标中依次选择
                    wrong_letters_image.clear()
                    for sprite in random_alphabet_group.sprites():
                        sprite.random_update(alphabet.current_frame, 1, 0, x_position_list[wrong_letters_postion],
                                             y_position_list[wrong_letters_postion])
                        wrong_letters_postion += 1
                        wrong_letters_image.append(sprite.random_frame)

                # ------------------------------------------------------------------------------------------------------

                #   如果吃了头部触碰到了正确的字母
                if len(pygame.sprite.spritecollide(snake.segments[0], alphabet_group, False)) > 0:
                    current_frame = alphabet.current_frame  # 获得当前正确字母
                    score_show_time = gameplay_time  # 得到当前得游戏时间
                    score_show = True  # 展示分数
                    correct_increase = True  # 蛇的头部分数增加
                    a = Snakebody_alphabet(current_frame)  # 得到当前碰撞的字母是什么
                    spell_list.append(ALPHABET_LIST[current_frame])  # 记录单词拼写到哪里了只记录正确的
                    eating_spelling.append(ALPHABET_LIST[current_frame])  # 记录吃了的字母不管对错
                    snake.add_segment(a)  # 添加到蛇的尾部
                    # 更新到下一个单词
                    alphabet.target_update(continuous_correct_alphabet, gameplay_time + 1, 1, x_position_list,
                                           y_position_list)
                    # 保证扰乱的字母和正确的字母各不相同，错误的字母也要更新
                    wrong_letters_image = [1, 1]
                    # 三个字母不能相同，只有相同就必须重新选择
                    while len(wrong_letters_image) != len(set(wrong_letters_image)):
                        # 给错误选择位置
                        wrong_letters_postion = 2
                        wrong_letters_image.clear()
                        for sprite in random_alphabet_group.sprites():
                            sprite.random_update(alphabet.current_frame, gameplay_time + 10, 10,
                                                 x_position_list[wrong_letters_postion],
                                                 y_position_list[wrong_letters_postion])
                            wrong_letters_postion += 1
                            # 将错误字母的图片都保存起来
                            wrong_letters_image.append(sprite.random_frame)
                    # 如果有提示的话，提示更新
                    if prompt_show[0][0] == 'YES':
                        tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    # 字母吃对了有一个声音
                    game_audio("game_sound/right.wav")
                    # 分数加10分
                    current_score += 10

                # -----------------------------------------------------------------------------------------------------
                #   如果蛇的头部碰到了错误的字母
                elif len(pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)) > 0:
                    # 到底碰到了那个错误字母
                    collide_sprite = pygame.sprite.spritecollide(snake.segments[0], random_alphabet_group, False, False)
                    score_show_time = gameplay_time  # 得到当前得游戏时间
                    score_show = True  # 展示分数
                    wrong_decrease = True  # 分数减展示
                    game_audio("game_sound/wrong.wav")  # 错误字母的声音
                    random_frame = collide_sprite[0].random_frame  # 得到碰撞的那个字母的编号
                    eating_spelling.append(ALPHABET_LIST[random_frame])  # 即使吃错了也要加进去

                    # 保证出现位置不会重复，在这只关心错误字母的更新
                    wrong_letters_image = [1, 1]
                    while len(wrong_letters_image) != len(set(wrong_letters_image)):
                        wrong_letters_postion = 2
                        wrong_letters_image.clear()
                        for sprite in random_alphabet_group.sprites():
                            sprite.random_update(alphabet.current_frame, gameplay_time + 10, 10,
                                                 x_position_list[wrong_letters_postion],
                                                 y_position_list[wrong_letters_postion])
                            wrong_letters_postion += 1
                            wrong_letters_image.append(sprite.random_frame)
                    # 提示也要更新
                    if prompt_show[0][0] == 'YES':
                        tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)
                    # 得到的分数也减10
                    current_score -= 10

                #   如果触碰到了提示
                if prompt_show[0][0] == 'YES':
                    if len(pygame.sprite.groupcollide(snake.segments, tip_group, False, False)) > 0:
                        tip_show = True  # 提示展示
                        tip_time = gameplay_time  # 提示展示的时间
                        score_show_time = gameplay_time  # 得到当前得游戏时间
                        score_show = True  # 展示分数
                        tip_decrease = True  # 提示分数增加
                        # 到蛇的第二个就开始消失计时
                        if len(pygame.sprite.spritecollide(snake.segments[1], tip_group, False, False)) > 0:
                            current_score -= 30  # 当前分数减30分
                            tip.tip_update(gameplay_time + 100, 100, x_position_list, y_position_list)  # 提示更新
                            game_audio("game_sound/health.wav")  # 提示的声音
                # 游戏没有结束，首先移动蛇
                snake.snake_moving(gameplay_time, snake_moving_speed)
        # --------------------------------------------------------------------------------------------------------------
        # 以下需要对游戏结束后的一些事情进行处理
        if game_over:
            if write_button:  # 因为游戏结束了会一直循环这个代码，所以这个变量的功能是为了让下面循环的代码只执行一次
                pygame.mixer.stop()  # 主游戏背景音乐要结束
                # game_audio("game_sound/game_over.wav")  # 游戏结束的背景音乐
                del snake.segments[2:]  # 每次游戏结束之后，要清除蛇后面的东西
                write_button = False  # 在结尾改为FALSE，只执行一次
            # 游戏结束时的背景板
            game_over_image = pygame.image.load("Game_Pictures/game_intro.jpg").convert_alpha()
            game_over_image = pygame.transform.scale(game_over_image, (FRAME_WIDTH * 27, FRAME_WIDTH * 24))
            screen.blit(game_over_image, (0, 0))
            # print results after game over
            print_text(CHINESE_FONT, 0 * 0, 0, "学习结束")
            print_text(CHINESE_FONT, FRAME_WIDTH * 7, 0, "本轮得分: " + str(current_score))
            # show how many words player remembered in one round
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 2, "正确拼写")
            print_result(OTHER_FONT, 0, FRAME_WIDTH * 4, words_list)
            print_text(CHINESE_FONT, 200, FRAME_WIDTH * 2, "汉语翻译")
            print_result(CHINESE_FONT, 200, FRAME_WIDTH * 4, task_words)
            print_text(CHINESE_FONT, 400, FRAME_WIDTH * 2, "你的拼写")
            print_result(CHINESE_FONT, 400, FRAME_WIDTH * 4, player_spelling)
        # --------------------------------------------------------------------------------------------------------------
        #  如果游戏还在运行
        else:
            # 画游戏上方的背景
            title_bg = pygame.image.load("Game_Pictures/title-bgd.png").convert_alpha()
            screen.blit(title_bg, (0, 0))
            # 要不要展示提示，及其展示的时间
            print_text(CHINESE_FONT, FRAME_WIDTH * 14, 75, "提示: ")
            if tip_show:
                print_text(OTHER_FONT, FRAME_WIDTH * 16, 75,
                           words_list[int(alphabet.current_word_number) - 1],
                           color=(255, 0, 0))
                tip_use = True  # 提示已经被使用
                # 1.5秒以后提示消失
                if gameplay_time > tip_time + 1500:
                    tip_show = False

            # 以下代码是为了展示分数的变化
            if score_show:
                if snake.velocity.first_variate == -1 or snake.velocity.first_variate == 1:  # 如何蛇横向移动
                    score_position_y = -60
                    score_position_x = 0
                elif snake.velocity.second_variate == -1 or snake.velocity.second_variate == 1:  # 如何蛇纵向移动
                    score_position_y = 0
                    score_position_x = 30
                if correct_increase:
                    print_text(SCORE_FONT, snake.snake_head.x_coordinate + score_position_x,
                               snake.snake_head.y_coordinate + score_position_y, '+10')
                elif wrong_decrease:
                    print_text(SCORE_FONT, snake.snake_head.x_coordinate + score_position_x,
                               snake.snake_head.y_coordinate + score_position_y, '-10')
                elif tip_decrease:
                    print_text(SCORE_FONT, snake.snake_head.x_coordinate + score_position_x,
                               snake.snake_head.y_coordinate + score_position_y, '-30')
                if gameplay_time > score_show_time + 450:  # 分数展示450毫秒，并初始化原来的参数
                    score_show = False
                    correct_increase = False
                    wrong_decrease = False
                    tip_decrease = False

            # 输出当前任务是什么
            print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, 15,
                       "当前任务: " + task_words[int(alphabet.current_word_number) - 1])

            # 音标
            if word_phone[0][0] == 'YES':
                print_text(CHINESE_FONT, FRAME_WIDTH
                           * 14, 15, '音标： ')
                pho_current_words = get_word_pho(phonetic_file_path, words_list[int(alphabet.current_word_number) - 1])
                print_text(PHONETIC_FONT, FRAME_WIDTH
                           * 16, 15, '/' + pho_current_words + '/')

            print_text(CHINESE_FONT, 0, 15, "当前得分: " + str(current_score))
            print_text(CHINESE_FONT, FRAME_WIDTH * 16, FRAME_WIDTH * 4 + 10,
                       "剩余任务: " + str(len(task_words) - int(alphabet.current_word_number) + 1))
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 2 + 15, "最高分数: " + str(int(highest_score)))
            print_text(CHINESE_FONT, 0, FRAME_WIDTH * 4 + 10, "单词记录: " + str(int(highest_words)))

            # 刚刚拼写完成的单词，当前在拼第几个单词，第二个之后才显示
            if int(alphabet.current_word_number) > 1:
                print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, FRAME_WIDTH * 4 + 10,
                           "刚完成:" + task_words[int(alphabet.current_word_number) - 2] + ': ' + words_list[
                               int(alphabet.current_word_number) - 2])
            # 第一个单词的时候没有任何单词
            else:
                print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, FRAME_WIDTH * 4 + 10, "刚完成: " + '    ')

            # 追踪单词的正确拼写
            if track_spelling[0][0] == 'YES':
                print_text(CHINESE_FONT, FRAME_WIDTH * 6 + 2, FRAME_WIDTH * 2 + 15, '拼写追踪：')
                for i in range(len(spell_list)):
                    print_text(OTHER_FONT, FRAME_WIDTH * 10 + i * 15 + 2, FRAME_WIDTH * 2 + 15, spell_list[i],
                               color=(255, 0, 0))

            # 如果当前单词已经拼写完毕
            if ''.join(spell_list) == words_list[int(alphabet.current_word_number) - 2]:
                # 如果已经拼写完毕，删除蛇后面的所有字母
                del snake.segments[2:]
                # 每次在单词拼写完成后，都要强制发音
                word_pro = words_list[int(alphabet.current_word_number) - 2]
                pygame.mixer.music.load(pronunciation_file_path + word_pro + ".mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                # record word from words_list if do not make mistake，如果没有拼错，就完全添加到review里面
                if words_list[int(alphabet.current_word_number) - 2] not in words_list_known:
                    if ''.join(eating_spelling) == words_list[
                                                            int(alphabet.current_word_number) - 2] and tip_use == False:
                        words_list_known.append(words_list[int(alphabet.current_word_number) - 2])  # 添加到已经记忆的单词列表
                        task_words_known.append(task_words[int(alphabet.current_word_number) - 2])  # 添加到已经记忆的单词列表
                        current_remembered_words += 1
                # clear the two list once task change
                player_spelling.append(''.join(eating_spelling))
                eating_spelling.clear()
                words_number += 1
                spell_list.clear()
                tip_use = False

            # draw all sprites
            snake.draw(screen)
            random_alphabet_group.draw(screen)
            alphabet_group.draw(screen)

            # set up whether there are prompts or not
            if prompt_show[0][0] == 'YES':
                tip_group.draw(screen)
        # draw all sprites
        pygame.display.update()


game_init()
'''
