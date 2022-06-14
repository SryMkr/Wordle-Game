
from engine import *
import copy


g = MainGame(1000, 800)  # 首先展示一个屏幕,这个是主游戏界面
# 设置单词以及倒数的时间 这个函数仅仅在第一阶段展示用，自成体系
SHOW_WORDS = ShowWords(2, 'words_pool/three_grade/three_grade_known.xls', 2)


while g.Main_Game_Running:  # 主游戏在运行
    g.game_Loop()  # 主函数程序

    # 以下循环只运行一次，然后不再运行
    if SHOW_WORDS.start_countdown_running:  # 先倒数5秒，准备开始
        SHOW_WORDS.start_Countdown()   # 只有5秒的倒计时
        g.window.blit(SHOW_WORDS.show_words_surface, (0, 0))  # 将倒计时画到频幕上

    # 以下代码只循环一次，然后不再运行，目的是为了让学生记忆单词
    if SHOW_WORDS.show_words_running:  # 然后展示单词
        SHOW_WORDS.show_words()  # 这个是获得要展示的时间和单词
        SHOW_WORDS.draw_words()  # 单独一个函数展示单词
        g.window.blit(SHOW_WORDS.show_words_surface, (0, 0))  # 将之画到频幕上

    # 以下代码要重复使用至少3次
    if SHOW_WORDS.show_all_words_running:  # 最后让记忆一次
        SHOW_WORDS.draw_all_words()  # 最后将10个单词画到频幕上
        g.window.blit(SHOW_WORDS.show_words_surface, (0, 0))  # 将10的单词的surface画到主频幕上

    # 第一关的初始参数
    if g.first_level_running:
        FIRST_LEVEL = FirstLevel('words_pool/three_grade/three_grade_known.xls')  # 定义一个第一关的类
        FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[0])  # 得到第一个单词
        letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标
        letter_contact = False  # 如果没有触碰到单词
        contact_rect_list = []  # 每一轮都看几个碰了
        first_chance_spelling = ''  # 得到每次检查时的拼写
        used_chance = []  # 已经用了哪些机会
        used_spelling = []  # 储存玩家的所有拼写
        current_task = 0  # 当前是第几个任务
        spelling_start_time = datetime.now()  # 获得游戏开始的时间
        spelling_countdown_number = 60  # 每个单词的答题时间
        player_spelling_show = {}  # 定义一个字典，来展示正确的拼写以及玩家的拼写，让玩家复习
        player_score = 0  # 用来记录玩家的得分
        play_pronunciation = False  # 用来控制展示错误的时候的发音
        g.first_level_running = False  # 第一关的初始参数设置为假
    # 第一关的代码
    if SHOW_WORDS.show_first_level_running and g.first_level_switch:
        if g.pronunciation:  # 这个控制单词发音按enter发音
            FIRST_LEVEL.pronunciation()

        FIRST_LEVEL.draw_Blocks(3)  # 画表格，参数的意思是给三次机会，所以有三行

        # 如果已经拼写完毕，才能按enter检查拼写
        if g.check_spelling and len(current_spelling) == len(FIRST_LEVEL.current_word):
            # 每检查一次都要发音一次
            game_Sound('Pronunciation/three_grade/' + FIRST_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
            play_pronunciation = True  # 让底下可以发音
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
            if first_chance_spelling != FIRST_LEVEL.current_word:  # 如果拼写错误，要惩罚时间
                spelling_countdown_number -= 1  # 将时间减1

        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150,
                  str(spelling_countdown_number), (255, 0, 0), 880, 70)  # 将剩余的时间画到屏幕上

        if first_chance_spelling:  # 如果玩家已经有了拼写答案
            for i in used_chance:  # 将所有的答案画到表格对应的位置
                FIRST_LEVEL.indicator_Spelling(used_spelling[i], used_chance[i])
            # 如果是拼写正确，展示正确得单词5秒再切换到下一个单词，并将该reset的参数全部reset
            if first_chance_spelling == FIRST_LEVEL.current_word and g.gameplay_time > show_indicator_time + 5000:
                player_score += 10 * len(first_chance_spelling)  # 如果玩家拼写正确，那么每个字母10分
                player_spelling_show[FIRST_LEVEL.current_word] = used_spelling  # 记录玩家正确的拼写和玩家的拼写
                spelling_countdown_number += 60  # 到了下一个单词重新倒计时60秒
                FIRST_LEVEL.letter_coordinate = {}

                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    SHOW_WORDS.show_first_level_running = False  # 结束这一关
                    SHOW_WORDS.show_all_words_running = True
                    FIRST_LEVEL.second_level_running = True  # 打开第二关的开关
                    SHOW_WORDS.show_all_words_countdown = 5  # 将倒计时的时间设置为5
                    g.first_level_switch = False  # 第一关的开关结束
                    current_task = 0
                else:
                    pass
                FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []   # 记录玩家的拼写
                used_chance = []    # 记录玩家已经使用的机会
                FIRST_LEVEL.current_chance = 0  # 将机会回归到最开始

            # 如果拼写不正确，而且所有的机会都已经用完了
            if len(used_spelling) == 3 and used_spelling[FIRST_LEVEL.current_chance] != FIRST_LEVEL.current_word \
                    and g.gameplay_time > show_indicator_time + 5000:
                for letter_index in range(len(FIRST_LEVEL.current_word)):  # 循环单词
                    #  如果这个字母根本就不在单词的拼写中
                    if used_spelling[FIRST_LEVEL.current_chance][letter_index] not in FIRST_LEVEL.current_word:
                        player_score -= 10  # 如果玩家拼写正确，那么分数减10分
                    # 如果选对了字母，而且放对了位置
                    elif used_spelling[FIRST_LEVEL.current_chance][letter_index] == FIRST_LEVEL.current_word[letter_index]:
                        player_score += 10  # 如果玩家拼写正确，那么分数加10分
                    else:
                        player_score += 5  # 如果有这个字母，但是没放对位置，只加5分

                player_spelling_show[FIRST_LEVEL.current_word] = used_spelling  # 记录玩家正确的拼写和玩家的拼写
                spelling_countdown_number += 60  # 到了下一个单词重新倒计时60秒
                FIRST_LEVEL.letter_coordinate = {}
                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    SHOW_WORDS.show_first_level_running = False  # 结束这一关
                    SHOW_WORDS.show_all_words_running = True
                    FIRST_LEVEL.second_level_running = True  # 打开第二关的开关
                    SHOW_WORDS.show_all_words_countdown = 5  # 将倒计时的时间设置为5
                    g.first_level_switch = False  # 第一关的开关结束
                    current_task = 0

                else:
                    pass
                FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []  # 记录玩家的拼写
                used_chance = []    # 记录玩家已经使用的机会
                FIRST_LEVEL.current_chance = 0  # 将机会回归到最开始

        # 展示已经拼写完成的单词
        if player_spelling_show:
            show_history(FIRST_LEVEL.first_level_surface, player_spelling_show)
        FIRST_LEVEL.first_level_surface.blit(FIRST_LEVEL.Blocks_Surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
        FIRST_LEVEL.draw_Letters()  # 把本次所有用到的字母都画到屏幕上
        # 如果玩家答题超时，显示当前的单词并且直接切换到下一个任务

        if spelling_countdown_number < 0:
            Failure_surface = show_Failure(FIRST_LEVEL.current_words_list[current_task],
                                           FIRST_LEVEL.current_phonetic[current_task],
                                           FIRST_LEVEL.current_translation[current_task])
            FIRST_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
            if spelling_countdown_number < -5:
                spelling_countdown_number = 60
                FIRST_LEVEL.letter_coordinate = {}

                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    SHOW_WORDS.show_first_level_running = False  # 结束这一关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示所有单词
                    FIRST_LEVEL.second_level_running = True  # 打开第二关的开关
                    SHOW_WORDS.show_all_words_countdown = 5  # 将倒计时的时间设置为5
                    g.first_level_switch = False  # 第一关的开关结束
                    current_task = 0
                else:
                    pass

                FIRST_LEVEL.split_Word(FIRST_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(FIRST_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []  # 记录玩家的拼写
                used_chance = []  # 记录玩家已经使用的机会
                FIRST_LEVEL.current_chance = 0  # 将机会回归到最开始

        #  当玩家三次机会都用完还拼写错误的时候
        if len(used_spelling) == 3 and used_spelling[FIRST_LEVEL.current_chance] != FIRST_LEVEL.current_word         :
            if play_pronunciation:
                game_Sound('Pronunciation/three_grade/' + FIRST_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
                game_Sound('game_sound/game_over.wav', 0.1)   # 游戏失败的声音
                play_pronunciation = False
            Failure_surface = show_Failure(FIRST_LEVEL.current_words_list[current_task],
                                           FIRST_LEVEL.current_phonetic[current_task],
                                           FIRST_LEVEL.current_translation[current_task])
            FIRST_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上

        # 当玩家回答正确了
        if first_chance_spelling == FIRST_LEVEL.current_word:
            if play_pronunciation:
                game_Sound('Pronunciation/three_grade/' + FIRST_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
                game_Sound('game_sound/game_win.mp3', 0.2)  # 游戏成功的声音
                play_pronunciation = False
            Failure_surface = show_Success(FIRST_LEVEL.current_words_list[current_task],
                                           FIRST_LEVEL.current_phonetic[current_task],
                                           FIRST_LEVEL.current_translation[current_task])
            FIRST_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上

        # 这个是画玩家的当前得分
        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/STKAITI.TTF', 70,
                  '分数:'+str(player_score),
                  FIRST_LEVEL.WHITE, 880, 240)

        # 这个是画当前任务的翻译
        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/Lucida-Sans-Unicode.ttf', 70,
                  FIRST_LEVEL.current_phonetic[current_task],
                  FIRST_LEVEL.WHITE, 580, 40)
        # 这个是画当前任务的音标
        draw_Text(FIRST_LEVEL.first_level_surface, 'Fonts/STKAITI.TTF', 70,
                  FIRST_LEVEL.current_translation[current_task],
                  FIRST_LEVEL.WHITE, 580, 140)

        g.window.blit(FIRST_LEVEL.first_level_surface, (0, 0))  # 将该页面画到屏幕上

        if not letter_contact:  # 如果目前没有接触到字母
            for current_letter_key in FIRST_LEVEL.letter_coordinate.keys():  # 循环列表里所有的字母
                # 如果鼠标选中了这个字母，并且点击了鼠标

                if is_in_rect((g.mouse_x, g.mouse_y), (FIRST_LEVEL.letter_coordinate[current_letter_key][0],
                                                       FIRST_LEVEL.letter_coordinate[current_letter_key][1], 60,
                                                       60)) and g.click_event:
                    game_Sound('game_sound/mouse_click_1.mp3', 0.2)  # 游戏鼠标的声音
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

    # 控制第二关的运行
    # 如果第一关结束，而且也展示结束，那么运行第二关
    if g.first_level_switch == False and FIRST_LEVEL.second_level_running == True \
           and SHOW_WORDS.show_all_words_running == False:
        if g.second_level_running:
            SECOND_LEVEL = SecondLevel('words_pool/three_grade/three_grade_known.xls')  # 定义一个第二关的类
            SECOND_LEVEL.split_Word(SECOND_LEVEL.current_words_list[0])  # 得到第一个单词
            letter_original_coordinate = copy.deepcopy(SECOND_LEVEL.letter_coordinate)  # 复制一份保留原坐标
            letter_contact = False  # 如果没有触碰到单词
            contact_rect_list = []  # 每一轮都看几个碰了
            first_chance_spelling = ''  # 得到每次检查时的拼写
            used_chance = []  # 已经用了哪些机会
            used_spelling = []  # 储存玩家的所有拼写
            current_task = 0  # 当前是第几个任务
            spelling_start_time = datetime.now()  # 获得游戏开始的时间
            spelling_countdown_number = 40  # 每个单词的答题时间缩短为40秒
            player_spelling_show = {}  # 定义一个字典，来展示正确的拼写以及玩家的拼写，让玩家复习
            play_pronunciation = False  # 用来控制展示错误的时候的发音
            g.second_level_running = False  # 这种设置只设置一次

        if g.pronunciation:  # 这个控制单词发音按enter发音
            SECOND_LEVEL.pronunciation()

        SECOND_LEVEL.draw_Blocks(2)  # 画表格，第二次机会

        # 如果已经拼写完毕，才能按enter检查拼写
        if g.check_spelling and len(current_spelling) == len(SECOND_LEVEL.current_word):
            # 每检查一次都要发音一次
            game_Sound('Pronunciation/three_grade/' + SECOND_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
            play_pronunciation = True  # 让底下可以发音
            first_chance_spelling = copy.deepcopy(current_spelling)  # 复制当前玩家的拼写
            used_chance.append(SECOND_LEVEL.current_chance)  # 将当前使用的机会行加入到已经使用过的机会中
            used_spelling.append(first_chance_spelling)     # 将玩家的历史拼写写入到一个列表中
            show_indicator_time = g.gameplay_time  # 记录按下enter得时间，为了以后再展示答案几秒钟

            SECOND_LEVEL.current_chance += 1  # 将机会加 1
            if SECOND_LEVEL.current_chance == 2:  # 如果机会已经使用完
                SECOND_LEVEL.current_chance = 1  # 让机会的次数一直等于第三次机会

            # 检查完把坐标送回到原来的坐标，重新开始拼写
            for key in SECOND_LEVEL.letter_coordinate.keys():
                SECOND_LEVEL.letter_coordinate[key][0] = letter_original_coordinate[key][0]  # 横坐标
                SECOND_LEVEL.letter_coordinate[key][1] = letter_original_coordinate[key][1]  # 纵坐标

        #  展示答题倒计时
        if datetime.now() > spelling_start_time + timedelta(seconds=1):  # 每过一秒
            spelling_start_time = datetime.now()  # 将当前的时间给旧时间
            if first_chance_spelling != SECOND_LEVEL.current_word:  # 如果拼写错误，要惩罚时间
                spelling_countdown_number -= 1  # 将时间减1

        draw_Text(SECOND_LEVEL.first_level_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150,
                  str(spelling_countdown_number), (255, 0, 0), 880, 70)  # 将剩余的时间画到屏幕上

        if first_chance_spelling:  # 如果玩家已经有了拼写答案
            for i in used_chance:  # 将所有的答案画到表格对应的位置
                SECOND_LEVEL.indicator_Spelling(used_spelling[i], used_chance[i])
            # 如果是拼写正确，展示正确得单词5秒再切换到下一个单词，并将该reset的参数全部reset
            if first_chance_spelling == SECOND_LEVEL.current_word and g.gameplay_time > show_indicator_time + 5000:
                player_score += 10 * len(first_chance_spelling)  # 如果玩家拼写正确，那么每个字母10分
                player_spelling_show[SECOND_LEVEL.current_word] = used_spelling  # 记录玩家正确的拼写和玩家的拼写
                spelling_countdown_number += 40  # 到了下一个单词重新倒计时60秒
                SECOND_LEVEL.letter_coordinate = {}

                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    FIRST_LEVEL.second_level_running = False  # 结束第二关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示单词
                    FIRST_LEVEL.third_level_running = True  # 开始第三关
                    SHOW_WORDS.show_all_words_countdown = 5  # 将倒计时的时间设置为5
                    current_task = 0

                else:
                    pass
                SECOND_LEVEL.split_Word(SECOND_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(SECOND_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []   # 记录玩家的拼写
                used_chance = []    # 记录玩家已经使用的机会
                SECOND_LEVEL.current_chance = 0  # 将机会回归到最开始

            # 如果拼写不正确，而且所有的机会都已经用完了
            if len(used_spelling) == 2 and used_spelling[SECOND_LEVEL.current_chance] != SECOND_LEVEL.current_word \
                    and g.gameplay_time > show_indicator_time + 5000:
                for letter_index in range(len(SECOND_LEVEL.current_word)):  # 循环单词
                    #  如果这个字母根本就不在单词的拼写中
                    if used_spelling[SECOND_LEVEL.current_chance][letter_index] not in SECOND_LEVEL.current_word:
                        player_score -= 10  # 如果玩家拼写正确，那么分数减10分
                    # 如果选对了字母，而且放对了位置
                    elif used_spelling[SECOND_LEVEL.current_chance][letter_index] == SECOND_LEVEL.current_word[letter_index]:
                        player_score += 10  # 如果玩家拼写正确，那么分数加10分
                    else:
                        player_score += 5  # 如果有这个字母，但是没放对位置，只加5分

                player_spelling_show[SECOND_LEVEL.current_word] = used_spelling  # 记录玩家正确的拼写和玩家的拼写
                spelling_countdown_number += 40  # 到了下一个单词重新倒计时60秒
                SECOND_LEVEL.letter_coordinate = {}
                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    FIRST_LEVEL.second_level_running = False  # 结束第二关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示单词
                    FIRST_LEVEL.third_level_running = True  # 开始第三关
                    SHOW_WORDS.show_all_words_countdown = 5  # 将倒计时的时间设置为5
                    current_task = 0
                else:
                    pass
                SECOND_LEVEL.split_Word(SECOND_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(SECOND_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []  # 记录玩家的拼写
                used_chance = []    # 记录玩家已经使用的机会
                SECOND_LEVEL.current_chance = 0  # 将机会回归到最开始

        # 展示已经拼写完成的单词
        if player_spelling_show:
            show_history(SECOND_LEVEL.first_level_surface, player_spelling_show)
        SECOND_LEVEL.first_level_surface.blit(SECOND_LEVEL.Blocks_Surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
        SECOND_LEVEL.draw_Letters()  # 把本次所有用到的字母都画到屏幕上
        # 如果玩家答题超时，显示当前的单词并且直接切换到下一个任务

        if spelling_countdown_number < 0:
            Failure_surface = show_Failure(SECOND_LEVEL.current_words_list[current_task],
                                           SECOND_LEVEL.current_phonetic[current_task],
                                           SECOND_LEVEL.current_translation[current_task])
            SECOND_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
            if spelling_countdown_number < -5:
                spelling_countdown_number = 40
                SECOND_LEVEL.letter_coordinate = {}

                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    FIRST_LEVEL.second_level_running = False  # 结束第二关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示单词
                    FIRST_LEVEL.third_level_running = True  # 开始第三关
                    SHOW_WORDS.show_all_words_countdown = 5  # 将倒计时的时间设置为5
                    current_task = 0
                else:
                    pass

                SECOND_LEVEL.split_Word(SECOND_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(SECOND_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []  # 记录玩家的拼写
                used_chance = []  # 记录玩家已经使用的机会
                SECOND_LEVEL.current_chance = 0  # 将机会回归到最开始

        #  当玩家三次机会都用完还拼写错误的时候
        if len(used_spelling) == 2 and used_spelling[SECOND_LEVEL.current_chance] != SECOND_LEVEL.current_word         :
            if play_pronunciation:
                game_Sound('Pronunciation/three_grade/' + SECOND_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
                game_Sound('game_sound/game_over.wav', 0.1)   # 游戏失败的声音
                play_pronunciation = False
            Failure_surface = show_Failure(SECOND_LEVEL.current_words_list[current_task],
                                           SECOND_LEVEL.current_phonetic[current_task],
                                           SECOND_LEVEL.current_translation[current_task])
            SECOND_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上

        # 当玩家回答正确了
        if first_chance_spelling == SECOND_LEVEL.current_word:
            if play_pronunciation:
                game_Sound('Pronunciation/three_grade/' + SECOND_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
                game_Sound('game_sound/game_win.mp3', 0.2)  # 游戏成功的声音
                play_pronunciation = False
            Failure_surface = show_Success(SECOND_LEVEL.current_words_list[current_task],
                                           SECOND_LEVEL.current_phonetic[current_task],
                                           SECOND_LEVEL.current_translation[current_task])
            SECOND_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上

        # 这个是画玩家的当前得分
        draw_Text(SECOND_LEVEL.first_level_surface, 'Fonts/STKAITI.TTF', 70,
                  '分数:'+str(player_score),
                  SECOND_LEVEL.WHITE, 880, 240)

        # 这个是画当前任务的翻译
        draw_Text(SECOND_LEVEL.first_level_surface, 'Fonts/STKAITI.TTF', 70,
                  SECOND_LEVEL.current_translation[current_task],
                  SECOND_LEVEL.WHITE, 580, 40)
        g.window.blit(SECOND_LEVEL.first_level_surface, (0, 0))  # 将该页面画到屏幕上

        if not letter_contact:  # 如果目前没有接触到字母
            for current_letter_key in SECOND_LEVEL.letter_coordinate.keys():  # 循环列表里所有的字母
                # 如果鼠标选中了这个字母，并且点击了鼠标

                if is_in_rect((g.mouse_x, g.mouse_y), (SECOND_LEVEL.letter_coordinate[current_letter_key][0],
                                                       SECOND_LEVEL.letter_coordinate[current_letter_key][1], 60,
                                                       60)) and g.click_event:
                    game_Sound('game_sound/mouse_click_1.mp3', 0.2)  # 游戏鼠标的声音
                    letter_contact = True  # 选中了这个单词
                    break  # 只要选中了就不循环了

        if letter_contact:  # 如果已经选择了一个单词，那么图片就要随着鼠标移动
            SECOND_LEVEL.letter_coordinate[current_letter_key][0] = g.mouse_x - 30 + g.mouse_rel_x  # 移动X坐标
            SECOND_LEVEL.letter_coordinate[current_letter_key][1] = g.mouse_y - 30 + g.mouse_rel_y  # 移动Y坐标

        if not g.click_event:  # 如果松开了鼠标
            letter_contact = False  # 就需要继续循环找下一个被选中的字母是什么
            # 看看单词有没有放到框框里
            contact_rect = letter_in_rect(SECOND_LEVEL.letter_coordinate[current_letter_key][0],
                                          SECOND_LEVEL.letter_coordinate[current_letter_key][1],
                                          SECOND_LEVEL.Blocks_Rect[SECOND_LEVEL.current_chance], (7 - 7) * 45, 200)

            if contact_rect:  # 如果放到框里面了，这时已经确定放进去了,那我要得到它得字母
                # 如果此时的列表为空,将这个框加进去
                if not contact_rect_list:
                    # 那么就将坐标改为框框里
                    SECOND_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                    SECOND_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                    contact_rect_list.append(contact_rect)  # 并将这个位置加到列表中
                # 已经是最后一个字母,只加一个
                elif current_letter_key == list(SECOND_LEVEL.letter_coordinate.keys())[-1]:  # 如果一直是最后一个字母
                    SECOND_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                    SECOND_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                    if contact_rect not in contact_rect_list:  # 别重复加坐标
                        contact_rect_list.append(contact_rect)
                else:  # 如果没有重复，那么就放进去
                    if pygame.Rect.collidelist(contact_rect, contact_rect_list) == -1:
                        SECOND_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                        SECOND_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                        contact_rect_list.append(contact_rect)
                    else:  # 如果坐标重复，就回到原来的位置
                        SECOND_LEVEL.letter_coordinate[current_letter_key][0] = \
                            letter_original_coordinate[current_letter_key][0]
                        SECOND_LEVEL.letter_coordinate[current_letter_key][1] = \
                            letter_original_coordinate[current_letter_key][1]
            else:  # 不在框框内就回到原来得坐标
                SECOND_LEVEL.letter_coordinate[current_letter_key][0] = letter_original_coordinate[current_letter_key][0]
                SECOND_LEVEL.letter_coordinate[current_letter_key][1] = letter_original_coordinate[current_letter_key][1]

        # 这个循环的目的是为了删除不在框中的坐标,并得到当前的拼写
        current_block_letter_rect = []
        current_spelling_dic = {}  # 记录玩家得单词拼写的字典
        current_spelling = ''  # 记录玩家当前的拼写
        for key, coordinate in SECOND_LEVEL.letter_coordinate.items():
            current_block_letter = letter_in_rect(coordinate[0], coordinate[1],
                                          SECOND_LEVEL.Blocks_Rect[SECOND_LEVEL.current_chance], (7 - 7) * 45, 200)
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

    # 第三关的代码
    if FIRST_LEVEL.third_level_running == True and SHOW_WORDS.show_all_words_running == False:
        if g.third_level_running:
            Third_LEVEL = ThirdLevel('words_pool/three_grade/three_grade_known.xls')  # 定义一个第二关的类
            Third_LEVEL.split_Word(Third_LEVEL.current_words_list[0])  # 得到第一个单词
            letter_original_coordinate = copy.deepcopy(Third_LEVEL.letter_coordinate)  # 复制一份保留原坐标
            letter_contact = False  # 如果没有触碰到单词
            contact_rect_list = []  # 每一轮都看几个碰了
            first_chance_spelling = ''  # 得到每次检查时的拼写
            used_chance = []  # 已经用了哪些机会
            used_spelling = []  # 储存玩家的所有拼写
            current_task = 0  # 当前是第几个任务
            spelling_start_time = datetime.now()  # 获得游戏开始的时间
            spelling_countdown_number = 30  # 每个单词的答题时间缩短为40秒
            player_spelling_show = {}  # 定义一个字典，来展示正确的拼写以及玩家的拼写，让玩家复习
            play_pronunciation = False  # 用来控制展示错误的时候的发音
            g.third_level_running = False  # 这种设置只设置一次

        if g.pronunciation:  # 这个控制单词发音按enter发音
            Third_LEVEL.pronunciation()

        Third_LEVEL.draw_Blocks(1)  # 画表格，第二次机会

        # 如果已经拼写完毕，才能按enter检查拼写
        if g.check_spelling and len(current_spelling) == len(Third_LEVEL.current_word):
            # 每检查一次都要发音一次
            game_Sound('Pronunciation/three_grade/' + Third_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
            play_pronunciation = True  # 让底下可以发音
            first_chance_spelling = copy.deepcopy(current_spelling)  # 复制当前玩家的拼写
            used_chance.append(Third_LEVEL.current_chance)  # 将当前使用的机会行加入到已经使用过的机会中
            used_spelling.append(first_chance_spelling)     # 将玩家的历史拼写写入到一个列表中
            show_indicator_time = g.gameplay_time  # 记录按下enter得时间，为了以后再展示答案几秒钟

            Third_LEVEL.current_chance += 1  # 将机会加 1
            if Third_LEVEL.current_chance == 1:  # 如果机会已经使用完
                Third_LEVEL.current_chance = 0  # 让机会的次数一直等于第一次机会

            # 检查完把坐标送回到原来的坐标，重新开始拼写
            for key in Third_LEVEL.letter_coordinate.keys():
                Third_LEVEL.letter_coordinate[key][0] = letter_original_coordinate[key][0]  # 横坐标
                Third_LEVEL.letter_coordinate[key][1] = letter_original_coordinate[key][1]  # 纵坐标

        #  展示答题倒计时
        if datetime.now() > spelling_start_time + timedelta(seconds=1):  # 每过一秒
            spelling_start_time = datetime.now()  # 将当前的时间给旧时间
            if first_chance_spelling != Third_LEVEL.current_word:  # 如果拼写错误，要惩罚时间
                spelling_countdown_number -= 1  # 将时间减1

        draw_Text(Third_LEVEL.first_level_surface, 'Fonts/MontserratAlternates-Regular-17.otf', 150,
                  str(spelling_countdown_number), (255, 0, 0), 880, 70)  # 将剩余的时间画到屏幕上

        if first_chance_spelling:  # 如果玩家已经有了拼写答案
            for i in used_chance:  # 将所有的答案画到表格对应的位置
                Third_LEVEL.indicator_Spelling(used_spelling[i], used_chance[i])
            # 如果是拼写正确，展示正确得单词5秒再切换到下一个单词，并将该reset的参数全部reset
            if first_chance_spelling == Third_LEVEL.current_word and g.gameplay_time > show_indicator_time + 5000:
                player_score += 10 * len(first_chance_spelling)  # 如果玩家拼写正确，那么每个字母10分
                player_spelling_show[Third_LEVEL.current_word] = used_spelling  # 记录玩家正确的拼写和玩家的拼写
                spelling_countdown_number += 30  # 到了下一个单词重新倒计时60秒
                Third_LEVEL.letter_coordinate = {}

                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    FIRST_LEVEL.third_level_running = False  # 结束第二关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示单词
                    SHOW_WORDS.show_all_words_countdown = 300  # 将倒计时的时间设置为5
                    current_task = 0

                else:
                    pass
                Third_LEVEL.split_Word(Third_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(Third_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []   # 记录玩家的拼写
                used_chance = []    # 记录玩家已经使用的机会
                Third_LEVEL.current_chance = 0  # 将机会回归到最开始

            # 如果拼写不正确，而且所有的机会都已经用完了
            if len(used_spelling) == 1 and used_spelling[Third_LEVEL.current_chance] != Third_LEVEL.current_word \
                    and g.gameplay_time > show_indicator_time + 5000:
                for letter_index in range(len(Third_LEVEL.current_word)):  # 循环单词
                    #  如果这个字母根本就不在单词的拼写中
                    if used_spelling[Third_LEVEL.current_chance][letter_index] not in Third_LEVEL.current_word:
                        player_score -= 10  # 如果玩家拼写正确，那么分数减10分
                    # 如果选对了字母，而且放对了位置
                    elif used_spelling[Third_LEVEL.current_chance][letter_index] == Third_LEVEL.current_word[letter_index]:
                        player_score += 10  # 如果玩家拼写正确，那么分数加10分
                    else:
                        player_score += 5  # 如果有这个字母，但是没放对位置，只加5分

                player_spelling_show[Third_LEVEL.current_word] = used_spelling  # 记录玩家正确的拼写和玩家的拼写
                spelling_countdown_number += 30  # 到了下一个单词重新倒计时60秒
                Third_LEVEL.letter_coordinate = {}
                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    FIRST_LEVEL.third_level_running = False  # 结束第二关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示单词
                    SHOW_WORDS.show_all_words_countdown = 300  # 将倒计时的时间设置为5
                    current_task = 0

                else:
                    pass
                Third_LEVEL.split_Word(Third_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(Third_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []  # 记录玩家的拼写
                used_chance = []    # 记录玩家已经使用的机会
                Third_LEVEL.current_chance = 0  # 将机会回归到最开始

        # 展示已经拼写完成的单词
        if player_spelling_show:
            show_history(Third_LEVEL.first_level_surface, player_spelling_show)
        Third_LEVEL.first_level_surface.blit(Third_LEVEL.Blocks_Surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
        Third_LEVEL.draw_Letters()  # 把本次所有用到的字母都画到屏幕上
        # 如果玩家答题超时，显示当前的单词并且直接切换到下一个任务

        if spelling_countdown_number < 0:
            Failure_surface = show_Failure(Third_LEVEL.current_words_list[current_task],
                                           Third_LEVEL.current_phonetic[current_task],
                                           Third_LEVEL.current_translation[current_task])
            Third_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上
            if spelling_countdown_number < -5:
                spelling_countdown_number = 30
                Third_LEVEL.letter_coordinate = {}

                if current_task < 9:  # 如果是除了最后一个单词的单词
                    current_task += 1  # 将移动到下一个字母
                elif current_task == 9:  # 如果已经是最后一个单词
                    player_score = player_score + spelling_countdown_number  # 每一秒都算1分，加到总分上
                    FIRST_LEVEL.third_level_running = False  # 结束第二关
                    SHOW_WORDS.show_all_words_running = True  # 开始展示单词
                    SHOW_WORDS.show_all_words_countdown = 300  # 将倒计时的时间设置为5
                    current_task = 0
                else:
                    pass
                Third_LEVEL.split_Word(Third_LEVEL.current_words_list[current_task])  # 肯定随着任务的移动而移动
                letter_original_coordinate = copy.deepcopy(Third_LEVEL.letter_coordinate)  # 复制一份保留原坐标
                used_spelling = []  # 记录玩家的拼写
                used_chance = []  # 记录玩家已经使用的机会
                Third_LEVEL.current_chance = 0  # 将机会回归到最开始

        #  当玩家三次机会都用完还拼写错误的时候
        if len(used_spelling) == 1 and used_spelling[Third_LEVEL.current_chance] != Third_LEVEL.current_word         :
            if play_pronunciation:
                game_Sound('Pronunciation/three_grade/' + Third_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
                game_Sound('game_sound/game_over.wav', 0.1)   # 游戏失败的声音
                play_pronunciation = False
            Failure_surface = show_Failure(Third_LEVEL.current_words_list[current_task],
                                           Third_LEVEL.current_phonetic[current_task],
                                           Third_LEVEL.current_translation[current_task])
            Third_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上

        # 当玩家回答正确了
        if first_chance_spelling == Third_LEVEL.current_word:
            if play_pronunciation:
                game_Sound('Pronunciation/three_grade/' + Third_LEVEL.current_words_list[current_task] + '.mp3', 1.0)
                game_Sound('game_sound/game_win.mp3', 0.2)  # 游戏成功的声音
                play_pronunciation = False
            Failure_surface = show_Success(Third_LEVEL.current_words_list[current_task],
                                           Third_LEVEL.current_phonetic[current_task],
                                           Third_LEVEL.current_translation[current_task])
            Third_LEVEL.first_level_surface.blit(Failure_surface, ((7 - 7) * 45, 200))  # 将表格画到屏幕上

        # 这个是画玩家的当前得分
        draw_Text(Third_LEVEL.first_level_surface, 'Fonts/STKAITI.TTF', 70,
                  '分数:'+str(player_score),
                  Third_LEVEL.WHITE, 880, 240)
        g.window.blit(Third_LEVEL.first_level_surface, (0, 0))  # 将该页面画到屏幕上

        if not letter_contact:  # 如果目前没有接触到字母
            for current_letter_key in Third_LEVEL.letter_coordinate.keys():  # 循环列表里所有的字母
                # 如果鼠标选中了这个字母，并且点击了鼠标

                if is_in_rect((g.mouse_x, g.mouse_y), (Third_LEVEL.letter_coordinate[current_letter_key][0],
                                                       Third_LEVEL.letter_coordinate[current_letter_key][1], 60,
                                                       60)) and g.click_event:
                    game_Sound('game_sound/mouse_click_1.mp3', 0.2)  # 游戏鼠标的声音
                    letter_contact = True  # 选中了这个单词
                    break  # 只要选中了就不循环了

        if letter_contact:  # 如果已经选择了一个单词，那么图片就要随着鼠标移动
            Third_LEVEL.letter_coordinate[current_letter_key][0] = g.mouse_x - 30 + g.mouse_rel_x  # 移动X坐标
            Third_LEVEL.letter_coordinate[current_letter_key][1] = g.mouse_y - 30 + g.mouse_rel_y  # 移动Y坐标

        if not g.click_event:  # 如果松开了鼠标
            letter_contact = False  # 就需要继续循环找下一个被选中的字母是什么
            # 看看单词有没有放到框框里
            contact_rect = letter_in_rect(Third_LEVEL.letter_coordinate[current_letter_key][0],
                                          Third_LEVEL.letter_coordinate[current_letter_key][1],
                                          Third_LEVEL.Blocks_Rect[Third_LEVEL.current_chance], (7 - 7) * 45, 200)

            if contact_rect:  # 如果放到框里面了，这时已经确定放进去了,那我要得到它得字母
                # 如果此时的列表为空,将这个框加进去
                if not contact_rect_list:
                    # 那么就将坐标改为框框里
                    Third_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                    Third_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                    contact_rect_list.append(contact_rect)  # 并将这个位置加到列表中
                # 已经是最后一个字母,只加一个
                elif current_letter_key == list(Third_LEVEL.letter_coordinate.keys())[-1]:  # 如果一直是最后一个字母
                    Third_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                    Third_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                    if contact_rect not in contact_rect_list:  # 别重复加坐标
                        contact_rect_list.append(contact_rect)
                else:  # 如果没有重复，那么就放进去
                    if pygame.Rect.collidelist(contact_rect, contact_rect_list) == -1:
                        Third_LEVEL.letter_coordinate[current_letter_key][0] = contact_rect.x + 15 + (7 - 7) * 45
                        Third_LEVEL.letter_coordinate[current_letter_key][1] = contact_rect.y + 15 + 200
                        contact_rect_list.append(contact_rect)
                    else:  # 如果坐标重复，就回到原来的位置
                        Third_LEVEL.letter_coordinate[current_letter_key][0] = \
                            letter_original_coordinate[current_letter_key][0]
                        Third_LEVEL.letter_coordinate[current_letter_key][1] = \
                            letter_original_coordinate[current_letter_key][1]
            else:  # 不在框框内就回到原来得坐标
                Third_LEVEL.letter_coordinate[current_letter_key][0] = letter_original_coordinate[current_letter_key][0]
                Third_LEVEL.letter_coordinate[current_letter_key][1] = letter_original_coordinate[current_letter_key][1]

        # 这个循环的目的是为了删除不在框中的坐标,并得到当前的拼写
        current_block_letter_rect = []
        current_spelling_dic = {}  # 记录玩家得单词拼写的字典
        current_spelling = ''  # 记录玩家当前的拼写
        for key, coordinate in Third_LEVEL.letter_coordinate.items():
            current_block_letter = letter_in_rect(coordinate[0], coordinate[1],
                                          Third_LEVEL.Blocks_Rect[Third_LEVEL.current_chance], (7 - 7) * 45, 200)
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

    pygame.display.update()  # 主函数程序

