from tkinter import *
from tkinter import ttk
import webbrowser
import sqlite3
import speech_recognition as sr
from datetime import datetime
import wave
import time
import pyaudio
import os
from PIL import Image, ImageTk

db = "./list.db"

conn = sqlite3.connect(db)

cur = conn.cursor()

root = Tk()

root.title("キーボードアプリ")
# root.geometry("1200x800")

root.state("zoomed")


# 見出し用フレーむ
head_frame = Frame(root)

# font=(フォント名, 文字サイズ, 太さ)
Label(head_frame, text="キーボードアプリ", font=("MSゴシック", 30, "bold"), height=2).pack()
# padxが横幅？でpadyが縦幅？
head_frame.pack()

select_frame = Frame(root)

engine = StringVar()
engine.set("Google")
Radiobutton(select_frame,text="Google", variable=engine, value="Google", width=10, font=("", 15, "bold")).grid(row=0, column=0, sticky="w")
Radiobutton(select_frame,text="Yahoo!", variable=engine, value="Yahoo!", width=10, font=("", 15, "bold")).grid(row=0, column=1, sticky="w")
Radiobutton(select_frame,text="bing", variable=engine, value="bing", width=10, font=("", 15, "bold")).grid(row=0, column=2, sticky="w")
Radiobutton(select_frame,text="Youtube", variable=engine, value="Youtube", width=10, font=("", 15, "bold")).grid(row=0, column=3, sticky="w")
select_frame.pack_propagate(False)
select_frame.pack()

input_frame = Frame(root)

def search(search_text):
    print(engine.get())
    
    select_engine = engine.get()
    
    if select_engine == "Google":
        webbrowser.open("https://google.com/search?q=" + search_text)
    elif select_engine == "Yahoo!":
        webbrowser.open("https://search.yahoo.co.jp/search?p=" + search_text)
    elif select_engine == "bing":
        webbrowser.open("https://www.bing.com/search?q=" + search_text)
    elif select_engine == "Youtube":
        webbrowser.open("https://www.youtube.com/results?search_query=" + search_text)
    else:
        print("error")



def audio():
    
    
    # 新しいウィンドウ
    process_window = Tk()
    process_window.title("音声処理中")
    process_window.geometry("400x200")
    
    # ラベルの初期値の設定（後で変更するため）
    # label_text = StringVar()
    # label_text.set("音声取得中。")
    
    process_label = Label(process_window, text="音声取得中",font=("MSゴシック", 20, "bold"))
    process_label.pack()
    
    process_window.grab_set()
    
    process_window.update()
    process_window.after(100)
    
    
    
    # audio
    
    FORMAT        = pyaudio.paInt16
    TIME          = 10           # 録音時間[s]
    SAMPLE_RATE   = 44100        # サンプリングレート
    FRAME_SIZE    = 1024         # フレームサイズ
    CHANNELS      = 1            # モノラルかバイラルか
    INPUT_DEVICE_INDEX = 0       # マイクのチャンネル
    NUM_OF_LOOP   = int(SAMPLE_RATE / FRAME_SIZE * TIME)



    WAV_FILE = "./wav_voice/output.wav"
    
    """
    デバイス上でのオーディオ系の機器情報を表示する
    """
    # pyaudio起動。オブジェクトの作成。
    pa = pyaudio.PyAudio()
    
    # pa.get_device_count()... オーディオの数。ここでやっていることはとりあえず使えるオーディオを列挙してつける奴を選ぶみたいな感じ？
    for i in range(pa.get_device_count()):
        
        # pa.get_device_info_by_index()... 使えるオーディオの詳細を辞書型で返すもの。print(pa.get_device_info_by_index(i))で一個ずつ出力してる。
        print(pa.get_device_info_by_index(i))
        print()
        
    # pyaudioのオブジェクトの終了。リソースの解放。
    pa.terminate()
    
    
    """
    デバイスから出力される音声の録音をする
    """
    
    # pyaudioの起動。オブジェクトの(ry
    pa = pyaudio.PyAudio()

    # 上で設定した録音の設定
    stream = pa.open(format   = FORMAT,
                    channels = CHANNELS,
                    rate     = SAMPLE_RATE,
                    # input    = Trueはマイクを使うことを示すらしい
                    input    = True,
                    input_device_index = INPUT_DEVICE_INDEX,
                    frames_per_buffer  = FRAME_SIZE)

    # レコーディング開始の出力
    print("RECORDING...")

    # 録音された音声データを入れるリスト
    list_frame = []

    # FRAME_SIZEバイトごとに録音されたデータをlist_frameの中に追加してる。正直詳しくはわからん。
    for i in range(NUM_OF_LOOP):
        data = stream.read(FRAME_SIZE)
        list_frame.append(data)

    # 録音成功しましたよの出力。
    print("RECORDING DONE!")


    # close and terminate stream object "stream"
    # 録音が完了したらオーディオストリームを停止して、
    stream.stop_stream()
    # ストリームを閉じて、
    stream.close()
    # pyaudioのオブジェクトの解放する。
    pa.terminate()

    # WAVファイルをバイナリ書き込みモードで開く。
    wf = wave.open(WAV_FILE, 'wb')
    
    # WAVファイルのチャンネル数、サンプル幅、サンプリングレートを設定する。
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pa.get_sample_size(FORMAT))
    wf.setframerate(SAMPLE_RATE)
    
    # list_frameに格納された音声データをWAVファイルに書き込む。コード見た感じlist_frameに格納した音声データをくっつけて書き込んでるっぽい。
    wf.writeframes(b''.join(list_frame))
    
    # 書き込みが終わったらWAVファイルを閉じる
    wf.close()
    
    
    
    
    
    
    
    r = sr.Recognizer()

    audio_file = "./wav_voice/output.wav"

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
        
    text = ""
    
    try:
        text = r.recognize_google(audio, language="ja-Jp")
        print(text, "recognize OK!")
        

    except sr.UnknownValueError:
        print("unknown")
    except sr.RequestError as e:
        print("request")

    os.remove("./wav_voice/output.wav")
    
    
    
    
    try:
        print(text, "keyboard OK!")
        entry.insert(END, text)
        process_label.config(text="音声解析完了")
        process_window.update()
    except:
        process_label.config(text="読み取れませんでした")
        process_window.update()
        print("読み取れませんでした。")
    
    
    process_window.after(2000)
    process_window.destroy()
    
    # 3秒間待ってやる
    # time.sleep(3)
    # ウィンドウ削除
    



entry = Entry(input_frame, width=50,font=("MSゴシック", 25, ""))
entry.grid(row=0,column=0,pady=50)
Button(input_frame, text="検索", command=lambda: search(entry.get())).grid(row=0, column=1)

Button(input_frame, image="",font=("MSゴシック", 12, ""), command=lambda: audio()).grid(row=0, column=2)
input_frame.pack()

# キーボードフレーム
keyboard_frame = Frame(root, width=800)


change_list = []


def insert_entry_hiragana(entry_number):
    global change_count
    global change_list
    
    number = int(entry_number.split("_")[0])
    mode = entry_number.split("_")[1]
    
    entry_text = entry.get()
    
    cur.execute("""
                SELECT *
                FROM hiragana
                """)

    text_list = cur.fetchall()
    # print(change_list)
    # print(change_count)
    if mode == "change":
        print(change_count)
        change_list.append(number)
        change_count += 1
        
        print(change_list)
        if change_count >= 2:
            # print("222222222222222222222222222222222",change_count)
            # 最初の更新
            
            print("sssssssssssssss", change_count)
            
            print(change_list)
            
            cur.execute("""
                        SELECT value
                        FROM hiragana
                        WHERE id = ?
                        """, (change_list[0],))
            
            change_keyword1 = cur.fetchone()
            
            cur.execute("""
                        SELECT value
                        FROM hiragana
                        WHERE id = ?
                        """, (change_list[1],))
            
            change_keyword2 = cur.fetchone()
            
            print(change_keyword1[0], change_keyword2[0])
            
            
            
            cur.execute("""
                            UPDATE hiragana 
                            SET value = ?
                            WHERE id = ?;
                        """, (change_keyword2[0], change_list[0]))
            # 二番目の更新
            cur.execute("""
                            UPDATE hiragana
                            SET value = ?
                            WHERE id = ?;
                        """, (change_keyword1[0], change_list[1]))
            conn.commit()
            print(change_count)
            
            change_count = 0
            print("change_count", change_count)
            change_list = []
            
            for widget in position_change_keyboard.winfo_children():
                widget.grid_forget()
                
            keyboard("hiragana", "small", "_change")
            
            
        
    else:
        for data in text_list:
            if number == int(data[0]):
                text = data[1]
                if text == "小" and mode != "read":
                    if entry_text and (entry_text[-1] == "あ" or entry_text[-1] == "い" or entry_text[-1] == "う" or entry_text[-1] == "え" or entry_text[-1] == "お" or entry_text[-1] == "や" or entry_text[-1] == "ゆ" or entry_text[-1] == "よ" or entry_text[-1] == "つ"):
                        change_text = entry_text[-1]
                        entry.delete(len(entry_text) - 1, END)
                        if change_text == "あ":
                            text = "ぁ"
                        elif change_text == "い":
                            text = "ぃ"
                        elif change_text == "う":
                            text = "ぅ"
                        elif change_text == "え":
                            text = "ぇ"
                        elif change_text == "お":
                            text = "ぉ"
                        elif change_text == "や":
                            text = "ゃ"
                        elif change_text == "ゆ":
                            text = "ゅ"
                        elif change_text == "よ":
                            text = "ょ"
                        elif change_text == "つ":
                            text = "っ"
                        else:
                            print("error")
                    else:
                        print("小文字にできない文字です")
                        text = ""
                else:
                    pass
            else:
                pass
        if mode == "input" and text != None:
            entry.insert(END, text)
        else:
            return text

def insert_entry_katakana(entry_number):
    global change_count
    global change_list
    
    number = int(entry_number.split("_")[0])
    mode = entry_number.split("_")[1]
    
    entry_text = entry.get()
    
    cur.execute("""
                SELECT *
                FROM katakana
                """)
    
    text_list = cur.fetchall()
    
    if mode == "change":
        print(change_count)
        change_list.append(number)
        change_count += 1
        
        print(change_list)
        if change_count >= 2:
            # print("222222222222222222222222222222222",change_count)
            # 最初の更新
            
            print("sssssssssssssss", change_count)
            
            print(change_list)
            
            cur.execute("""
                        SELECT value
                        FROM katakana
                        WHERE id = ?
                        """, (change_list[0],))
            
            change_keyword1 = cur.fetchone()
            
            cur.execute("""
                        SELECT value
                        FROM katakana
                        WHERE id = ?
                        """, (change_list[1],))
            
            change_keyword2 = cur.fetchone()
            
            print(change_keyword1[0], change_keyword2[0])
            
            cur.execute("""
                            UPDATE katakana
                            SET value = ?
                            WHERE id = ?;
                        """, (change_keyword2[0], change_list[0]))
            # 二番目の更新
            cur.execute("""
                            UPDATE katakana
                            SET value = ?
                            WHERE id = ?;
                        """, (change_keyword1[0], change_list[1]))
            conn.commit()
            print(change_count)
            
            change_count = 0
            print("change_count", change_count)
            change_list = []
            
            for widget in position_change_keyboard.winfo_children():
                widget.grid_forget()
                
            keyboard("katakana", "small", "_change")
            
            
        
    else:
        for data in text_list:
            if number == int(data[0]):
                text = data[1]
                if text == "小" and mode != "read":
                    if entry_text and (entry_text[-1] == "ア" or entry_text[-1] == "イ" or entry_text[-1] == "ウ" or entry_text[-1] == "エ" or entry_text[-1] == "オ" or entry_text[-1] == "ユ" or entry_text[-1] == "ヤ" or entry_text[-1] == "ヨ" or entry_text[-1] == "ツ"):
                        change_text = entry_text[-1]
                        entry.delete(len(entry_text) - 1, END)
                        if change_text == "ア":
                            text = "ァ"
                        elif change_text == "イ":
                            text = "ィ"
                        elif change_text == "ウ":
                            text = "ゥ"
                        elif change_text == "エ":
                            text = "ェ"
                        elif change_text == "オ":
                            text = "ォ"
                        elif change_text == "ヤ":
                            text = "ャ"
                        elif change_text == "ユ":
                            text = "ュ"
                        elif change_text == "ヨ":
                            text = "ョ"
                        elif change_text == "ツ":
                            text = "ッ"
                        else:
                            print("error")
                    else:
                        print("小文字にできない文字です")
                        text = ""
                else:
                    pass
            else:
                pass
        if mode == "input" and text != None:
            entry.insert(END, text)
        else:
            return text

def insert_entry_english(entry_number, big_or_small):
    
    global change_count
    global change_list
    
    number = int(entry_number.split("_")[0])
    mode = entry_number.split("_")[1]
    
    
    cur.execute("""
                SELECT *
                FROM english
                """)
    
    text_list = cur.fetchall()
    
    
    entry_text = entry.get()
    cur.execute("""
                SELECT *
                FROM english
                """)
    
    text_list = cur.fetchall()
    
    if mode == "change":
        print(change_count)
        change_list.append(number)
        change_count += 1
        
        print(change_list)
        if change_count >= 2:
            # print("222222222222222222222222222222222",change_count)
            # 最初の更新
            
            print("sssssssssssssss", change_count)
            
            print(change_list)
            
            cur.execute("""
                        SELECT small_value, big_value
                        FROM english
                        WHERE id = ?
                        """, (change_list[0],))
            
            change_keyword1 = cur.fetchone()
            
            cur.execute("""
                        SELECT small_value, big_value
                        FROM english
                        WHERE id = ?
                        """, (change_list[1],))
            
            change_keyword2 = cur.fetchone()
            
            print(change_keyword1, change_keyword2)
            
            
            
            cur.execute("""
                            UPDATE english
                            SET small_value = ?,
                                big_value = ?
                            WHERE id = ?;
                        """, (change_keyword2[0], change_keyword2[1], change_list[0]))
            # 二番目の更新
            cur.execute("""
                            UPDATE english
                            SET small_value = ?,
                                big_value = ?
                            WHERE id = ?;
                        """, (change_keyword1[0], change_keyword1[1], change_list[1]))
            conn.commit()
            # print(change_count)
            
            change_count = 0
            # print("change_count", change_count)
            change_list = []
            
            for widget in position_change_keyboard.winfo_children():
                widget.grid_forget()
                
            keyboard("english", "small", "_change")
    # 文字が入っているかの確認
    # if entry_text:
    #     change_text = entry_text[-1]
    else:
        text = ""
        
        for data in text_list:
            
            
            
            if number == int(data[0]):
                print(data)
                if data[1] or data[2]:
                    if big_or_small == "big":
                        text = data[1]
                    else:
                        text = data[2]
                    
                    root.update()

                print(mode)
                
                if mode == "input" and text == "⇧":
                    keyboard("english", "big", "_input")
                    print(big_or_small)
                    text = ""
                    
                elif mode == "input" and text == "⇩":
                    keyboard("english", "small", "_input")
                    text = ""
                
                root.update()
        
        
        if mode == "input":
            entry.insert(END, text)
        else:
            return text

def insert_entry_symbol(entry_number):
    global change_count
    global change_list
    
    number = int(entry_number.split("_")[0])
    mode = entry_number.split("_")[1]
    
    entry_text = entry.get()
    # 文字が入っているかの確認
    if entry_text:
        change_text = entry_text[-1]
    
    text = ""
    
    cur.execute("""
                SELECT *
                FROM symbol
                """)
    
    symbol_data = cur.fetchall()
    
    if mode == "change":
        print(change_count)
        change_list.append(number)
        change_count += 1
        
        print(change_list)
        if change_count >= 2:
            # print("222222222222222222222222222222222",change_count)
            # 最初の更新
            
            print("sssssssssssssss", change_count)
            
            print(change_list)
            
            cur.execute("""
                        SELECT value
                        FROM symbol
                        WHERE id = ?
                        """, (change_list[0],))
            
            change_keyword1 = cur.fetchone()
            
            cur.execute("""
                        SELECT value
                        FROM symbol
                        WHERE id = ?
                        """, (change_list[1],))
            
            change_keyword2 = cur.fetchone()
            
            print(change_keyword1, change_keyword2)
            
            
            
            cur.execute("""
                            UPDATE symbol
                            SET value = ?
                            WHERE id = ?;
                        """,  (change_keyword2[0], change_list[0]))
            # 二番目の更新
            cur.execute("""
                            UPDATE symbol
                            SET value = ?
                            WHERE id = ?;
                        """, (change_keyword1[0],  change_list[1]))
            conn.commit()
            # print(change_count)
            
            change_count = 0
            # print("change_count", change_count)
            change_list = []
            
            for widget in position_change_keyboard.winfo_children():
                widget.grid_forget()
                
            keyboard("symbol", "small", "_change")
    
    else:
        for data in symbol_data:
            if number == int(data[0]):
                text = data[1]
        
        if mode == "input":
            entry.insert(END, text)
        else:
            return text



def operation(control):
    if control == "delete":
        entry_text = entry.get()
        entry.delete(len(entry_text) - 1, END)

# def keyboard_size(string_size):

#     if string_size == "小":
#         s_size = 15
#         print("小")
#     elif string_size == "中":
#         s_size = 17
#         print("中")
#     elif string_size == "大":
#         s_size=19
#         print("大")
#     else:
#         s_size=17
    

# 新しいウィンドウ
first_click = True
position_change_window = None
position_change_window = Toplevel(root)
position_change_window.title("文字配置変更")
position_change_window.state("zoomed")
position_change_window.protocol("WM_DELETE_WINDOW", lambda: "pass")
position_change_text = Frame(position_change_window)
Label(position_change_text, text="文字配置変更", font=("", 30, "")).pack(pady=50)
    
position_change_text.pack()
    
position_change_keyboard = Frame(position_change_window, width=800)
position_change_keyboard_change = Frame(position_change_window)
position_change_window.withdraw()
change_count = 0

first_click = True

# 最後に選択されていたキーボード
last_keyboard = ""

def position_change():
    global last_keyboard
    
    position_change_window.deiconify()
    keyboard(last_keyboard, "small", "_change")
    change("_change")
    position_change_window.grab_set()
    position_change_keyboard.pack(padx=240, fill="x")
    position_change_keyboard_change.pack()
    

def position_decision():
    global last_keyboard
    
    print("閉じられた")
    for widget in keyboard_frame.winfo_children():
                widget.grid_forget()
    keyboard(last_keyboard, "small", "_input")
    print("再鼓動")
    position_change_window.grab_release()
    position_change_window.withdraw()
    root.wait_window(position_change_window)
    

# キーボード
def keyboard(keyboard, big_or_small, mode):
    global last_keyboard
    last_keyboard = keyboard
    # print(mode, "mode")
    


    if mode == "_input":
        for widget in keyboard_frame.winfo_children():
            widget.grid_forget()
            # print("change", mode)
    
    else:
        for widget in position_change_keyboard.winfo_children():
            widget.grid_forget()
            # print("change", mode)
    
    if keyboard == "hiragana":
        cur.execute("""
                    SELECT value
                    FROM hiragana
                    """)
        hiragana_data = cur.fetchall()
        print(hiragana_data)
        for i in range(0, 5):
            for j in range(0, 11):
                if hiragana_data[(11 * i) + j][0] != None and mode == "_input":
                    
                    Button(keyboard_frame, text=insert_entry_hiragana(str((11 * i) + j) + "_read"), width=5, height=2, font=("", 17, ""), command=lambda i=i, j=j : insert_entry_hiragana(str((11 * i) + j) + mode)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                else:
                    Button(position_change_keyboard, text=insert_entry_hiragana(str((11 * i) + j) + "_read"), width=5, height=2, font=("", 17, ""), command=lambda i=i, j=j : insert_entry_hiragana(str((11 * i) + j) + mode)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                    # print("change")
                
                    
    elif keyboard == "katakana":
        cur.execute("""
                    SELECT value
                    FROM katakana
                    """)
        katakana_data = cur.fetchall()
        print(katakana_data)
        for i in range(0, 5):
            for j in range(0, 11):
                if katakana_data[(11 * i) + j][0] != None and mode == "_input":
                
                    Button(keyboard_frame, text=insert_entry_katakana(str((11 * i) + j) + "_read"), width=5, height=2, font=("", 17, ""), command=lambda i=i, j=j : insert_entry_katakana(str((11 * i) + j) + mode)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                else:
                    Button(position_change_keyboard, text=insert_entry_katakana(str((11 * i) + j) + "_read"), width=5, height=2, font=("", 17, ""), command=lambda i=i, j=j : insert_entry_katakana(str((11 * i) + j) + mode)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                        
                



    elif keyboard == "english":
        cur.execute("""
                    SELECT small_value
                    FROM english
                    ORDER BY id ASC
                    """)
                
        english_data = cur.fetchall()
                
        print(english_data, "data")
        
        
        for i in range(0, 4):
            for j in range(0, 10):
                # print(english_data[1][0], "value")
                if english_data[(10 * i) + j][0] != None and mode == "_input":
                    Button(keyboard_frame, text=insert_entry_english(str((10 * i) + j) + "_read", big_or_small), width=5, height=2, font=("", 19, ""), command=lambda i=i, j=j : insert_entry_english(str((10 * i) + j) + mode, big_or_small)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                else:
                    Button(position_change_keyboard, text=insert_entry_english(str((10 * i) + j) + "_read", big_or_small), width=5, height=2, font=("", 19, ""), command=lambda i=i, j=j : insert_entry_english(str((10 * i) + j) + mode, big_or_small)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                

    elif keyboard == "symbol":
        for i in range(0, 5):
            for j in range(0, 10):
                if mode == "_input":
                    Button(keyboard_frame, text=insert_entry_symbol(str((10 * i) + j) + "_read"), width=5, height=2, font=("", 17, ""), command=lambda i=i, j=j : insert_entry_symbol(str((10 * i) + j) + mode)).grid(row=i, column=j, padx=5, pady=5, sticky="w")
                else:
                    Button(position_change_keyboard, text=insert_entry_symbol(str((10 * i) + j) + "_read"), width=5, height=2, font=("", 17, ""), command=lambda i=i, j=j : insert_entry_symbol(str((10 * i) + j) + mode)).grid(row=i, column=j, padx=5, pady=5, sticky="w")

    
    
    print(keyboard)
    
    # print(mode)
    
    # Button(keyboard_frame, image=r"").grid(row=0, column=12, padx=5, pady=5, sticky="w")
    Button(keyboard_frame, text="文字を1つ消す", width=12, height=2, font=("", 17, ""), command=lambda : operation("delete")).grid(row=0, column=11, padx=5, pady=5, sticky="w")
    # Button(keyboard_frame, text="文字サイズ大",width=12, height=2, font=("", 17, ""), command=lambda : keyboard_size("大")).grid(row=1, column=11,padx=5, pady=5, sticky="w")
    # Button(keyboard_frame, text="文字サイズ中",width=12, height=2, font=("", 17, ""), command=lambda : keyboard_size("中")).grid(row=2, column=11,padx=5, pady=5, sticky="w")
    # Button(keyboard_frame, text="文字サイズ小",width=12, height=2, font=("", 17, ""), command=lambda : keyboard_size("小")).grid(row=3, column=11,padx=5, pady=5, sticky="w")
    root.update()




keyboard("hiragana", "small", "_input")



keyboard_frame.pack(padx=240, fill="x")



keyboard_change = Frame(root)

def change(mode):
    if mode == "_input":
        Button(keyboard_change, text="ひらがな", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("hiragana", "small", mode)).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        Button(keyboard_change, text="カタカナ", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("katakana", "small", mode)).grid(row=0, column=1, padx=20, pady=20, sticky="w")
        Button(keyboard_change, text="英数字", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("english", "small", mode)).grid(row=0, column=2, padx=20, pady=20, sticky="w")
        Button(keyboard_change, text="記号", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("symbol", "small", mode)).grid(row=0, column=3, padx=20, pady=20, sticky="w")
        Button(keyboard_change, text="配置変更", width=15, height=2, font=("", 17, ""), command=lambda : position_change()).grid(row=0, column=4, padx=20, pady=20, sticky="w")
    
    else:
        mode == "_change"
        Button(position_change_keyboard_change, text="ひらがな", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("hiragana", "small", mode)).grid(row=0, column=0, padx=20, pady=20, sticky="w")
        Button(position_change_keyboard_change, text="カタカナ", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("katakana", "small", mode)).grid(row=0, column=1, padx=20, pady=20, sticky="w")
        Button(position_change_keyboard_change, text="英数字", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("english", "small", mode)).grid(row=0, column=2, padx=20, pady=20, sticky="w")
        Button(position_change_keyboard_change, text="記号", width=15, height=2, font=("", 17, ""), command=lambda : keyboard("symbol", "small", mode)).grid(row=0, column=3, padx=20, pady=20, sticky="w")
        Button(position_change_keyboard_change, text="配置確定", width=15, height=2, font=("", 17, ""), command=lambda : position_decision()).grid(row=0, column=4, padx=20, pady=20, sticky="w")

change("_input")

keyboard_change.pack()

# ウィンドウの表示
root.mainloop()

# from tkinter import *
# from tkinter import ttk

# # ウィジェットと説明の情報をリストで定義
# widgets_info = [
#     ("Button", "クリック可能なボタンです。"),
#     ("Label", "テキストや画像を表示するためのウィジェットです。"),
#     ("Entry", "1行のテキスト入力フィールドです。"),
#     ("Checkbutton", "チェックボックスです。"),
#     ("Menubutton", "ボタンを押すと選択肢が表示されます。"),
#     ("Radiobutton", "ラジオボタンです。"),
#     ("Scale", "スライダーバーです。"),
#     ("Scrollbar", "スクロールバーです。"),
#     ("Spinbox", "スピンボックスです。数値を入力するためのボックスです。")
# ]

# root = Tk()
# root.title("Tkinter ウィジェット一覧")

# #見出し用フレーム
# head_frame = Frame(root)
# Label(head_frame, text="ウィジェット一覧", font=("", 18, "")).pack()
# head_frame.pack()

# #メインフレーム
# main_frame = Frame(root)
# main_frame.pack()

# # ウィジェット名を配置
# for i, (widget_name, _) in enumerate(widgets_info):
#     Label(main_frame, text=widget_name).grid(row=i, column=0, padx=5, pady=5, sticky="w")

# # ウィジェットを配置
# Button(main_frame, text="Button").grid(row=0, column=1, padx=5, pady=5, sticky="w")
# Label(main_frame, text="Label").grid(row=1, column=1, padx=5, pady=5, sticky="w")
# Entry(main_frame).grid(row=2, column=1, padx=5, pady=5, sticky="w")
# Checkbutton(main_frame).grid(row=3, column=1, padx=5, pady=5, sticky="w")
# ttk.Menubutton(main_frame, text="Menubutton").grid(row=4, column=1, padx=5, pady=5, sticky="w")
# ttk.Radiobutton(main_frame).grid(row=5, column=1, padx=5, pady=5, sticky="w")
# ttk.Scale(main_frame).grid(row=6, column=1, padx=5, pady=5, sticky="w")
# ttk.Scrollbar(main_frame).grid(row=7, column=1, padx=5, pady=5, sticky="w")
# ttk.Spinbox(main_frame).grid(row=8, column=1, padx=5, pady=5, sticky="w")

# # 説明を配置
# for i, (_, description) in enumerate(widgets_info):
#     Label(main_frame, text=description, wraplength=300, justify="left").grid(row=i, column=2, padx=5, pady=5, sticky="w")

# root.mainloop()

# main_frame では、各ウィジェットを pack() ではなく grid で表の中に配置しています。