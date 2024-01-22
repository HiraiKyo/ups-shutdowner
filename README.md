# ups-shutdowner

Safe-shutdowner for UPS power unit by Nipron.

# Arduino 側送信パラメータ

- `shutdowner=1` : 当プログラム動作中を通知

# 利用前設定方法

## USB ポート指定

1. `dmesg | grep tty`で`cp210x connverter`を探す
2. `settings.ini`の`PORT`にシリアルポートを入力

## スタートアップ登録

1. アプリケーション一覧の検索窓で`session`と検索
2. 自動実行アプリケーション
3. 追加を押して、`start.sh`をスタートアップに登録

### `start.sh`の編集

- `cd /home/USER/ups-shutdowner`でカレントディレクトリを移動しておかないと`settings.ini`を読み込めない
- `python`と`ups-shutdowner.py`を絶対パスで入力する必要があるかも？

PC 再起動テスト後、`ps -aux | grep ups`でプロセス要確認

# 開発環境

## Install & Run

```
./start.sh
```

## Requirements

- Pyserial

## Build

TODO:
