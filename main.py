import configparser
import serial
from serial.tools import list_ports
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

# 再設定用リスト表示
print("[LOG] List of serial ports:")
ports = list_ports.comports()
devices = [info.device for info in ports]
for i in range(len(devices)):
  print("[LOG] input %3d: open %s" % (i, devices[i]))

# 設定ファイル読み込み
print("[LOG] Loading settings.ini...")
inifile = configparser.ConfigParser()
inifile.read("settings.ini")
port = inifile.get("Proto1", "PORT")
print("[LOG] Success.")

# UPS電源のシリアルポートを確認、接続
print("[LOG] Connecting to UPS power unit...")
ser = serial.Serial(port, 9600, timeout=None)
print("[LOG] Success.")

# 接続確認テスト
print("[LOG] Testing the connection...")
ser.write(str.encode("TEST"))
print("[LOG] Success.")

# 接続失敗時エラー
# print("Connection failed.")

# セーフシャットダウン処理
print("[LOG] Listening...")
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
