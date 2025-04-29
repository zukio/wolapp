# Wake On LAN & PC管理アプリケーション

複数のPCの状態監視と操作（起動・シャットダウン）を行うためのWebインターフェースを提供するFlaskアプリケーションです。Raspberry Pi上で動作させ、ネットワーク内のPCを管理できます。

## 機能

- **複数PC管理**: 複数のPCの状態監視と管理を一括で行えます
- **リアルタイム監視**: 定期的に各PCの状態をチェックし、UIに反映します
- **Wake On LAN**: マジックパケットを送信してリモートでPCを起動できます
- **リモートシャットダウン**: SSH経由でPCをシャットダウンできます
- **分かりやすいUI**: 各PCの状態をカラーコード付きで視覚的に表示します
- **操作ロック**: 処理中は他の操作をロックし、誤操作を防止します

## セットアップ

### 前提条件

- Python 3.6以上
- Flask
- Raspberry Pi（または任意のLinux/Windows/Macマシン）
- 操作対象PCのWake On LAN設定が有効化されていること
- シャットダウン機能を使用する場合はSSH接続が可能であること

### インストール手順

1. リポジトリをクローンするか、ソースコードをダウンロードします

```bash
git clone <repository-url>
cd wake-on-lan-app
```

2. 必要なパッケージをインストールします

```bash
pip install flask
```

3. `config.py`を編集し、あなたの環境設定とPC情報を入力します

```python
# PC情報を実際の値に変更してください
PCS_CONFIG = {
    'pc1': {
        'name': 'メインPC',
        'mac': '00:11:22:33:44:55',  # 実際のMACアドレス
        'ip': '192.168.1.100',       # 実際のIPアドレス
    },
    'pc2': {
        'name': 'サブPC',
        'mac': 'AA:BB:CC:DD:EE:FF',  # 実際のMACアドレス
        'ip': '192.168.1.101',       # 実際のIPアドレス
    }
}

# 必要に応じて他の設定も変更
```

4. アプリケーションを起動します

```bash
python app.py
```

5. ブラウザから`http://<あなたのラズパイのIP>:5000/`にアクセスします

## 設定ファイル詳細

`config.py`には以下の設定セクションがあります：

### SERVER_CONFIG

Flaskサーバーの動作設定です。

```python
SERVER_CONFIG = {
    'host': '0.0.0.0',  # すべてのネットワークインターフェースでリッスン
    'port': 5000,       # 使用するポート
    'debug': True       # デバッグモード（本番環境では False に設定）
}
```

### PCS_CONFIG

管理対象PCの情報です。必要な数だけ追加できます。

```python
PCS_CONFIG = {
    'pc_id': {          # PC識別子（一意）
        'name': '表示名',  # UI上での表示名
        'mac': 'XX:XX:XX:XX:XX:XX',  # MACアドレス（WOL用）
        'ip': '192.168.x.x',          # IPアドレス（状態確認用）
    },
    # 他のPCを追加...
}
```

### APP_CONFIG

アプリケーションの動作設定です。

```python
APP_CONFIG = {
    'status_update_interval': 10,  # PC状態更新間隔（秒）
    'wakeup_wait_time': 5,         # 起動処理後の待機時間（秒）
    'shutdown_wait_time': 5        # シャットダウン後の待機時間（秒）
}
```

### SSH_CONFIG

リモートシャットダウン機能のSSH設定です。

```python
SSH_CONFIG = {
    'username': 'user',  # SSHユーザー名
    'timeout': 5         # SSHコマンドタイムアウト（秒）
}
```

## 注意事項

- シャットダウン機能には対象PCへのSSHアクセス権限が必要です
- Windows PCをシャットダウンする場合は、対象PCでリモートシャットダウンを許可する設定が必要です
- 実際の環境に合わせて`utils/network.py`の`shutdown_pc`関数を調整してください

## フォルダ構造

```
/wake-on-lan-app
  ├── main.py          # メインアプリケーション
  ├── config.py       # 設定ファイル
  ├── /src
  │   └── index.html  # HTMLテンプレート
  ├── /static
  │   ├── /css
  │   │   └── style.css
  │   └── /js
  │       └── main.js
  └── /utils
      └── network.py  # ネットワーク関連ユーティリティ
```

## カスタマイズ

### 新しいPCの追加

`config.py`の`PCS_CONFIG`に新しいPCの情報を追加するだけです：

```python
PCS_CONFIG = {
    # 既存のPC設定...
    'pc3': {
        'name': '新しいPC',
        'mac': 'ZZ:ZZ:ZZ:ZZ:ZZ:ZZ',
        'ip': '192.168.1.102',
    }
}
```

### シャットダウン方法のカスタマイズ

異なるシャットダウン方法を使用するには、`utils/network.py`の`shutdown_pc`関数を修正します：

```python
def shutdown_pc(ip, username='user', timeout=5):
    """PCをシャットダウン（例: Windows PCの場合）"""
    try:
        # Windowsの場合
        result = subprocess.run(['net', 'rpc', 'shutdown', '-I', ip, '-U', f'{username}%password'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               timeout=timeout)
        return result.returncode == 0
    except:
        return False
```

## トラブルシューティング

### Wake On LANが動作しない

1. 対象PCのBIOS/UEFIでWake On LANが有効になっているか確認
2. ネットワークカードの設定でWake On LANが有効になっているか確認
3. MACアドレスが正確に設定されているか確認

### シャットダウンが動作しない

1. SSH接続が可能か確認（`ssh user@ip`で手動接続テスト）
2. シャットダウン権限があるか確認
3. `utils/network.py`のシャットダウンコマンドを対象OSに合わせて修正

### ステータスが更新されない

1. Pingがファイアウォールによってブロックされていないか確認
2. 正しいIPアドレスが設定されているか確認