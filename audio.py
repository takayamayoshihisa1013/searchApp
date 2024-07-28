# from datetime import datetime
# import wave
# import time

# import pyaudio


# # pyaudioのパラメータの設定
# FORMAT        = pyaudio.paInt16
# TIME          = 10           # 録音時間[s]
# SAMPLE_RATE   = 44100        # サンプリングレート
# FRAME_SIZE    = 1024         # フレームサイズ
# CHANNELS      = 1            # モノラルかバイラルか
# INPUT_DEVICE_INDEX = 0       # マイクのチャンネル
# NUM_OF_LOOP   = int(SAMPLE_RATE / FRAME_SIZE * TIME)

# FORMAT：pyaudioで録音、再生する時のフォーマットを指定しています。ここは、そういうものだと思って使う形で良いと思います。
# TIME：録音する時間です。単位は秒です。
# SAMPLE_RATE：サンプリングレートです。サンプリングレートについて説明するのはここの記事の本筋から外れてしまうのですが、コンピュータがアナログデータを取り扱うにあたってどのくらいの頻度でデータを取得するのか、を設定する数値です。大きくすればするほどより高音質に録音/再生できますが、ここをいじるのはあまりお勧めしません。
# FRAME_SIZE：pyaudioではFRAME_SIZE単位で録音を実行します。そのサイズを指定しています。
# CHANNELS：モノラルかバイラルかを設定します。
# INPUT_DEVICE_INDEX：ループバック録音のデバイスのインデックスです。これは利用している端末毎に違うため、自分で探す必要があります。詳細については後述します。
# NUM_OF_LOOP：FRAESIZEを何回ループさせればTIME秒の録音と一致するのかを計算しています。

from datetime import datetime
import wave
import time
import pyaudio
import speech_recognition as sr
import os 


FORMAT        = pyaudio.paInt16
TIME          = 10           # 録音時間[s]
SAMPLE_RATE   = 44100        # サンプリングレート
FRAME_SIZE    = 1024         # フレームサイズ
CHANNELS      = 1            # モノラルかバイラルか
INPUT_DEVICE_INDEX = 0       # マイクのチャンネル
NUM_OF_LOOP   = int(SAMPLE_RATE / FRAME_SIZE * TIME)



WAV_FILE = "./wav_voice/output.wav"


def look_for_audio_input():
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


def record_and_save():
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


def play_wav_file():
    """
    音声ファイルの再生
    """

    # 指定されたWAVファイルを読み込みモードで開く。
    wf = wave.open(WAV_FILE, 'rb')
    
    # pyaudioの(ry
    pa = pyaudio.PyAudio()

    # 再生する音声ファイルのフォーマット、チャンネル数、サンプリングレートを設定する
    # んだけどWAVファイルの情報を.get_format_from_width(wf.getsampwidth())、wf.getnchannels()で取得して設定できるっぽい
    stream = pa.open(format   = pa.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate     = wf.getframerate(),
                    output   = True)

    # ファイルの読み込み
    print("Read a file")
    
    # 指定されたフレームサイズ分の音声データを読み取る。
    data = wf.readframes(FRAME_SIZE)

    # 各バッファで再生はFRAME SIZE分だけ行われる
    print("play the flie")
    is_to_go = True
    while is_to_go:
        # data分バッファに音声データに書いていくっぽい
        stream.write(data)
        data = wf.readframes(FRAME_SIZE)
        # "data"がゼロになったらフラグをFalseにしてwhileループを抜ける
        is_to_go = len(data) != 0 

    # ストリームを閉じてオブジェクト解放
    stream.close()
    pa.terminate()

def voice_recognize():
        
    r = sr.Recognizer()

    audio_file = "./wav_voice/output.wav"

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio, language="ja-Jp")
        print(text, "recognize OK!")
        
        

    except sr.UnknownValueError:
        print("unknown")
    except sr.RequestError as e:
        print("request")

    os.remove("./wav_voice/output.wav")
    


def main():
    look_for_audio_input() # デバイス探し
    record_and_save()      # デバイスから出力される音声を録音する
    time.sleep(3)
    # play_wav_file()        # 録音した音声ファイルを再生する
    text = voice_recognize()
    print(text, "audio OK!")
    return text

if __name__ == '__main__':
    main()



