# ups-shutdowner

Safe-shutdowner for UPS power unit by Nipron.

# 利用前設定方法

## USB ポート指定

1. `dmesg | grep tty`で`cp210x connverter`を探す
2. `settings.ini`の`PORT`にシリアルポートを入力

## スタートアップ登録

TODO:

# 開発環境

## Install & Run

```
./start.sh
```

## Requirements

- Pyserial

## Build

TODO:
