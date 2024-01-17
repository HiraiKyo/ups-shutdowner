import configparser
import serial
import subprocess

# スタートアップ処理
print("### Starting UPS Shutdowner... ###")

# 設定ファイル読み込み
print("Loading settings.ini...")
inifile = configparser.SafeConfigParser()
inifile.read("settings.ini")
port = inifile.get("Proto1", "PORT")

# UPS電源のシリアルポートを確認、接続
print("Connecting to UPS power unit...")
ser = serial.Serial(port, 9600, timeout=None)

# 接続確認テスト
print("Checking the connection...")
ser.write("TEST")

# 接続失敗時エラー
# print("Connection failed.")

# セーフシャットダウン処理
while True:
  line = ser.readline()
  print(line)
  if line == "HIGH":
    # バッテリー駆動への切り替え信号を受信
    print("Switched to battery supply.")
    # 安全なPCシャットダウンリクエストの送信
    print("Trying to shutdown this PC...")
    subprocess.call("shutdown -t 1")
    break

ser.close()
