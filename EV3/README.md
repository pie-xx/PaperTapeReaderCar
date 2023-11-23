# EV3のMicropython開発環境とシリアル通信について

　もともとはLEGO Mindstorms EV3に紙テープリーダーを接続してMakerFairで走らせたいという話だったので、続いてpicoの代わりにEV3を使うことをやりはじめた。ケーブル作ればなんとかなるっしょ、くらいの簡単なお仕事と思ってたら、意外に難しかった。

1. LEGO本社からMindstormsの製品ページがなくなっている。
2. BricsCCというLEGO Mindstroms界隈でよく使われてる開発環境を入れようしたら、SygwinだのGitだのEV3のソースだのいろいろ必要で、最終的にクロスコンパイラが配布終了になっているのが分かってお手上げ。
3. EV3のOS (なんとLinux) を置き換えて、Micropythonを使って開発できる環境がVS Code の拡張機能にあるのでインストール。picoのMicropythonではUARTオブジェクトでシリアル通信できたから、EV3のMicropythonにそれらしきオブジェクトがないかダンプしてみたが出力にでてこない。
4. 私の作ったPythonのオブジェクトダンプは、importしないと対象が出てこないものだった。UART関連オブジェクト名をマニュアル見てimportしたらちゃんと出力された。

## EV3の環境設定

1. 公式ページからMicropythonの使えるEV3のsdcardイメージをダウンロードする。
2. sdcardイメージをEtherというツールでsdcardに焼く。
3. EV3のサイドスロットにsdcardを挿入して電源を入れると、そっちから起動する。

https://pybricks.com/ev3-micropython/startinstall.html

LEGO educationページには動画の説明がある

https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3/

## VS CodeにEV3開発環境を導入

https://pybricks.com/ev3-micropython/startrun.html
https://pybricks.com/ev3-micropython/startlinux.html


## クロスケーブル作成

1. LEGO純正EV3接続ケーブルか、6芯モジュラーケーブルをぶった斬る。6芯モジュラーケーブルはそのままではLEGOに刺さらないので、爪のでっぱりを削り取る。

2. 以下のように接続する。

PCと接続するとき

|PC用USBシリアル変換|EV3|
|--|--|
|GND|3 赤(GND)|
|RX|5 黄(TX)|
|TX|6 青(RX)|

紙テープリーダーと接続するとき

|紙テープリーダー|EV3|
|--|--|
|TX|6(RX)|
|GND|3 赤(GND)|


## Micropythonでのシリアル通信のやり方

|プロジェクト|内容|
|--|--|
|[comtest](./EV3/comtest/README.md)|PCにターミナルで接続し、PCから送信された文字列を行ごとに音声出力する|
|[tapereader](./EV3/tapereader/README.md)|紙テープリーダと接続し、なんかする|


Micropythonマニュアルとサンプルコード

https://pybricks.com/ev3-micropython/iodevices.html#uart-device
