import configparser
import serial
import subprocess

# UPS電源設定項目
## 電源からPCへの出力
TTL_OUTPUT_AC_FINE = "LOW" 
TTL_OUTPUT_AC_DOWN = "HIGH"
## PCから電源への入力
TTL_INPUT_DC_FINE = "HIGH"
TTL_INPUT_DC_DOWN = "LOW"

# スタートアップ処理
print("### Starting UPS Shutdowner... ###")

# 設定ファイル読み込み
print("[LOG] Loading settings.ini...")
inifile = configparser.SafeConfigParser()
inifile.read("settings.ini")
port = inifile.get("Proto1", "PORT")

# UPS電源のシリアルポートを確認、接続
print("[LOG] Connecting to UPS power unit...")
ser = serial.Serial(port, 9600, timeout=None)

# 接続確認テスト
print("[LOG] Checking the connection...")
ser.write(str.encode("TEST"))

# 接続失敗時エラー
# print("Connection failed.")

# セーフシャットダウン処理
while True:
  line = ser.readline()
  print("[LOG] From {}: {}".format(port, line))
  if line == TTL_OUTPUT_AC_DOWN:
    # バッテリー駆動への切り替え信号を受信
    print("[LOG] Switched to battery supply.")
    # 安全なPCシャットダウンリクエストの送信
    print("[LOG] Trying to shutdown this PC...")
    subprocess.call("shutdown -t 1")
    break

ser.close()
