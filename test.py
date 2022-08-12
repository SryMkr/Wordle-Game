import tkinter as tk
from tkinter import filedialog
from audioandprocess import Audio_model


au_model = Audio_model("", False)  # 现在才选择文件了 没有开始记录

#file_dict = []  # 这个是为了实现多个文件打分


def get_file():
    file = filedialog.askopenfilename(filetypes=[('text files', '.txt')])  # 选择一个txt文件
    au_model.current_file = file  # 将这个文件给函数处理
    text1.delete('1.0', tk.END)  # 可以删除文本框的内容
    text1.insert(tk.END, file)  # 可以删除文本框的内容
    file_content = au_model.get_content(file)  # 读取文件中的内容
    text2.delete('1.0', tk.END)
    text2.insert(tk.END, file_content)


def set_result_path():
    result_path = filedialog.askdirectory()
    au_model.audio_path = result_path
    text1.insert(tk.END, result_path)


def start_rec():
    lb_Status['text'] = '正在录音'
    au_model.record_and_save()


def stop_rec():
    global file_dict
    text1.delete('1.0', tk.END)
    #text2.delete('1.0', tk.END)
    lb_Status['text'] = '录音结束'
    file_dict = []  # 这个是为了实现多个文件打分
    file_dict.append(au_model.current_file)  # 这个是实现多个音频文件统一发送打分，而我一次只要一个
    au_model.is_recording = False


def start_score():
    result = au_model.get_score(file_dict)
    for r in result:
        text3.insert(tk.END, r)


# 设置一个清空记录的按钮
def reset():
    text3.delete('1.0', 'end')


root = tk.Tk()  # 作用是创建一个窗口
root.resizable(width=False, height=False)  # 控制玩家不可以改变窗口的大小
root.title("score pronunciation")  # 这个框架的名字
frm = tk.Frame(root)  # 相当于在主屏幕上弄一个框架
frm.grid(padx='100', pady='100')  # 相当于自动布局整个页面
# 选择一个按钮 参数1： 在哪个框架： 参数2 按钮的题目 参数三：要调什么函数 参数四：字体和字体的大小
btn_get_file_path = tk.Button(frm, text='选择单词库 ：', command=get_file, font=('Helvetica', '15'))
btn_get_file_path.grid(row=0, column=0)  # 放在第一行第一列
text1 = tk.Text(frm, width='100', height='5', font=('Helvetica', '15'))  # 创建一个文本框 宽度 高度
text1.grid(row=0, column=1)  # 这个文本框在的位置

btn_get_file_content = tk.Button(frm, text='单词内容 ：', font=('Helvetica', '15'))
btn_get_file_content.grid(row=1, column=0)  # 放在第二行第一列
text2 = tk.Text(frm, width='100', height='5', font=('Helvetica', '15'))  # 创建一个文本框 宽度 高度
text2.grid(row=1, column=1)  # 这个文本框在的位置

btn_start_rec = tk.Button(frm, text='录音', command=start_rec, width=10, font=('Helvetica', '15'))
btn_start_rec.grid(row=2, column=0)
lb_Status = tk.Label(frm, text='准备录音', anchor='w', fg='green', font=('Helvetica', '15'))
lb_Status.grid(row=2, column=1)

btn_stop_rec = tk.Button(frm, text="结束录音", command=stop_rec, font=('Helvetica', '15'))
btn_stop_rec.grid(row=2, column=2)

btn_score = tk.Button(frm, text="点击评分", command=start_score, width=10, font=('Helvetica', '15'))
btn_score.grid(row=3, column=0)

text3 = tk.Text(frm, width='100', height='18', font=('Helvetica', '15'))
text3.grid(row=3, column=1)

btn_score = tk.Button(frm, text="清空得分", command=reset, width=10, font=('Helvetica', '15'))
btn_score.grid(row=3, column=2)


root.mainloop()




















