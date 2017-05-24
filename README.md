想定しているデータフォーマット
------------------------------

    Header
    31                 0
    +----+----+----+----+
    |'H' |'E' |'A' |'D' | Magic 'HEAD'
    +----+----+----+----+
    |0xfe|0xed|0xfe|0xed| Magic 0xfeedfeed
    +----+----+----+----+
    |  Mod_ID | DataLen | Mod_ID:  0 - 65535 Network Byte Order
    +----+----+----+----+ DataLen: Data Lengty (bytes)
    |'D' |'A' |'T' |'A' | Magic 'DATA'
    +----+----+----+----+
    | DATA #1 | DATA #2 | One Data size = 2 bytes
    +----+----+----+----+
              :
    +----+----+----+----+
    |DATA #N-1| DATA #N | N = DataLen / 2
    +----+----+----+----+

データエミュレータ
------------------

1プロセスで1リードアウトモジュールをエミュレートする。
複数のリードアウトモジュールを模擬するには複数のPCで
走らせるかポート番号を変えるなどする。

    valren-emulator.py2 [-m mod_id] [-p port] [-s sleep_sec]

    デフォルト値:
    mod_id:    0
    port:      2222
    sleep_sec: 0

sleep_secを指定すると1回データを送ったらsleep_sec秒スリープ
してから次のデータを送る。データレートを小さくするのに使う。

データサイズは4kB〜16kBまで16バイト単位で変化する。大きさは
一様乱数を使って決めている。


変数など
--------

    const static int MAX_EVENT_DATA_BYTE_SIZE = 65536; // 64kB
    const static int HEADER_BYTE_SIZE         = 16;    // ヘッダ長(バイト)
    const static int DATA_LEN_INDEX           = 10;    // データ長があるインデックス

読み取り方式
------------

Gathererコンポーネントは1つで複数のリードアウトモジュールを読む。
多重読みだしにはepollを使う。

epoll_wait()から返ってくると読めるソケットが存在するのでその
ソケットを、HEADER_LENバイト読み、データ長をとりだす。続けて
データ部分を読み出す。
読んだらすぐ後段のコンポーネントに送る。

epoll_wait()のタイムアウトはデフォルト値の2秒になっている。このあいだ
データがこなければ、daq_run()を抜けて、再びepoll_wait()で待つ。

