import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import chardet
import os

##### 関数 #####
def set_input_file_func():
    # ファイルダイアログメニューの設定
    file_type = [("text","*.txt"), ("text","*.text")]
    file_path = filedialog.askopenfilename(filetypes = file_type)
    if not file_path:
        input_path_box.insert(tk.END, file_path)
    # 読み込みファイルサイズチェック
    elif os.path.getsize(file_path) == 0:
        pop_warn_message_window("", "読み込みファイルが空です。別のファイルを選択してください。")
    else:
        input_path_box.delete(0, tk.END)
        input_path_box.insert(tk.END, file_path)
        output_file_name = file_path.rsplit('/', 1)[-1].rsplit('.', 1)[-2]
        output_file_name_box.delete(0, tk.END)
        output_file_name_box.insert(tk.END, f'{output_file_name}_加工後')

def set_output_file_func():
    # フォルダダイアログメニューの設定
    folder_path = filedialog.askdirectory()
    if not folder_path:
        output_path_box.insert(tk.END, folder_path)
    else:
        output_path_box.delete(0, tk.END)
        output_path_box.insert(tk.END, folder_path)

def set_output_file_checkbox_func():
    # 書き出しフォルダダイアログメニューの有効無効切り替え
    if output_check_value.get():
        output_path_box["state"] = "disable"
        output_button["state"] = "disable"
    else:
        output_path_box["state"] = "normal"
        output_button["state"] = "normal"

def pop_warn_message_window(title, message):
    messagebox.showwarning(title, message)

def run_func():
    # 読み込みファイルの空白チェック
    if not input_path_box.get():
        pop_warn_message_window("", "読み込みファイルを選択してください。")
    elif not output_file_name_box.get():
        pop_warn_message_window("", "書き出し後ファイル名を入力してください。")
    else:
        # 書き出しチェックボックス判定
        if output_check_value.get():
            # 書き出し先フォルダは読み込みファイルと同階層とする
            output_file_path = input_path_box.get().rsplit('/', 1)[-2]
            statusbar["text"] = "Running"
            original_to_web(input_path_box.get(), output_file_path, output_file_name_box.get())
            statusbar["text"] = "Finish"
        elif not output_path_box.get():
            pop_warn_message_window("", "書き出しフォルダを選択するか、書き出しチェックボックスをチェックしてください。")
        else:
            statusbar["text"] = "Running"
            original_to_web(input_path_box.get(), output_path_box.get(), output_file_name_box.get())
            statusbar["text"]="Finish"

def original_to_web(input_file_path, output_folder_path, output_file_name):
    # 台詞判定　文頭が「か『か（で開始、文末が」か』か）で終了していればTrue）
    def is_dialogue(line):
        if line.startswith('「') and line.endswith('」\n'):
            return True
        elif line.startswith('（') and line.endswith('）\n'):
            return True
        elif line.startswith('『') and line.endswith('』\n'):
            return True
        else:
            return False

    # 空行と台詞行以外全角スペースの追加
    def add_full_space(line):
        if is_dialogue(line):
            return line
        elif len(line.strip()) == 0:
            return line
        else:
            return '　' + line

    # 改行の追加
    def add_return(line, before_line):
        if is_dialogue(line) == is_dialogue(before_line):
            return line
        else:
            return '\n' + line

    # 文字コード判定
    def set_charset():
        with open(input_file_path, mode = 'rb') as for_encoding:
            binary = for_encoding.read()
        return chardet.detect(binary)["encoding"]

    try:
        # ファイルの取得
        encoding_type = set_charset()
        file_extension = input_file_path.rsplit('.', 1)[-1]
        with open(input_file_path, encoding = encoding_type, mode='r') as input_file, open(f'{output_folder_path}/{output_file_name}.{file_extension}', encoding = encoding_type, mode='w') as output_file:
            # ファイルの書き出し
            input_string_list = input_file.readlines()
            before_line = input_string_list[0]
            for line in input_string_list:
                add_full_space_line = add_full_space(line)
                processed_line = add_return(add_full_space_line, before_line)
                output_file.write(processed_line)
                before_line = line
    except FileNotFoundError as e:
        print(e)
        pop_warn_message_window("", "読み込みファイル、もしくは書き出しディレクトリが存在しません。\nファイルパスを確認してください。")
    except UnicodeEncodeError as e:
        print(e)
        pop_warn_message_window("文字コードエラー", e)
#####  #####

# クラスをインスタンス化
root = tk.Tk()

# ウインドウのサイズ指定
root.geometry("800x400")
# ウインドウのタイトル指定
root.title("テキスト整形くん")

# inputテキストボックス設置
input_path_box_label = tk.Label(root, text = "読み込みファイルパス")
input_path_box_label.place(x = 10, y = 5)
input_path_box = tk.Entry(width = 110)
input_path_box.place(x = 10, y = 30)
# inputボタン設置
input_button = tk.Button(root, text = "読込ファイル設定", command = set_input_file_func)
input_button.place(x = 690, y = 27)

# outputテキストボックス設置
output_path_box_label = tk.Label(root, text = "書き出しフォルダパス")
output_path_box_label.place(x = 10, y = 55)
output_path_box = tk.Entry(width = 110)
output_path_box.place(x = 10, y = 100)
# outputボタン設置
output_button = tk.Button(root, text = "書出フォルダ設定", command = set_output_file_func)
output_button.place(x = 690, y = 97)
# outputチェック設置
output_check_value = tk.BooleanVar()
output_check_value.set(False)
output_checkbox = tk.Checkbutton(root, text='書き出しファイルを読み込みファイルと同じ階層に配置する', var = output_check_value, command = set_output_file_checkbox_func)
output_checkbox.place(x = 7, y = 72)
# outputファイル接尾句テキストボックス設置
output_file_name_box_label = tk.Label(root, text = "書き出し後ファイル名")
output_file_name_box_label.place(x = 10, y = 125)
output_file_name_box = tk.Entry(width = 50)
output_file_name_box.place(x = 10, y = 145)
output_file_extention_label = tk.Label(root, text = ".txt")
output_file_extention_label.place(x = 300, y = 145)

# 実行ボタン設置
run_button = tk.Button(root, text = "実行", command = run_func)
run_button.place(x = 10, y = 250)

# ステータスバー設置
statusbar = tk.Label(root, text = "No action", bd = 1, relief = tk.SUNKEN ,anchor = tk.W)
#statusbar.place(x = 10, y = 500)
statusbar.pack(side = tk.BOTTOM, fill = tk.X)

# ウインドウ状態の維持
root.mainloop()