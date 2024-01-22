import configparser
import serial
from serial.tools import list_ports
import subprocess
import time

# UPS電源設定項目
## 電源からPCへの出力
CTS_OUTPUT_AC_FINE = True
CTS_OUTPUT_AC_DOWN = False
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
  print("[LOG]   input %3d: open %s" % (i, devices[i]))

# 設定ファイル読み込み
print("[LOG] Loading settings.ini...")
inifile = configparser.ConfigParser()
inifile.read("settings.ini")
port = inifile.get("Proto1", "PORT")
timeout = int(inifile.get("Proto1", "TIMEOUT"))
baudrate = int(inifile.get("Proto1", "BAUDRATE"))
mode = inifile.get("Proto1", "MODE") # デバッグモード: debug, 通常:normal
arduino_port = inifile.get("Proto1", "ARDUINO_PORT")
print("[LOG] Success.")

# UPS電源のシリアルポートを確認、接続
print("[LOG] Connecting to UPS power unit...")
ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
ser.close()
ser.open() # 下で受信できないので、再オープン処理を入れてみる
print("[LOG] Success.")

# 接続確認テスト
# TODO: 接続確認テストをしたいけど、うまくいかない
# print("[LOG] Testing the connection...")
# ser.write(str.encode("TEST"))
# print(ser.readline())
# print("[LOG] Success.")

# 接続成功時、Arduinoに成功通知
arduino_serial = serial.Serial(arduino_port, baudrate=baudrate, timeout=timeout)
arduino_serial.write("TEST")

# セーフシャットダウン処理
print("[LOG] Listening...")
while True:
  # CTSピンが電源接続の状態を示す
  is_powered = ser.cts
  print("[LOG] Power State(CTS) : {}".format(is_powered))
  if is_powered == CTS_OUTPUT_AC_DOWN:
    # バッテリー駆動への切り替え信号を受信
    print("[LOG] Switched to battery supply.")
    # 安全なPCシャットダウンリクエストの送信
    print("[LOG] Trying to shutdown this PC...")
    ser.close()
    if(mode == "debug"):
      subprocess.call(["shutdown", "-t", "1"])
    else:
      subprocess.call(["shutdown", "-h", "now"])
    break
  time.sleep(5)

ser.close()    
