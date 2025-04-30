# config.py - コンフィグファイル
"""
Wake On LANアプリの設定ファイル
"""

# サーバー設定
SERVER_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}

# PC情報の設定
PCS_CONFIG = {
    'pc1': {
        'name': 'PC 1',
        'mac': 'XX:XX:XX:XX:XX:XX',  # PC1のMACアドレスを設定
        'ip': '192.168.1.100',       # PC1のIPアドレスを設定
        'username': 'user1',         # PC1のユーザー名
        'password': 'password1',     # PC1のパスワード
    },
    'pc2': {
        'name': 'PC 2',
        'mac': 'YY:YY:YY:YY:YY:YY',  # PC2のMACアドレスを設定
        'ip': '192.168.1.101',       # PC2のIPアドレスを設定
        'username': 'user2',         # PC2のユーザー名
        'password': 'password2',     # PC2のパスワード
    }
}

# アプリ設定
APP_CONFIG = {
    'status_update_interval': 10,  # PCステータス更新間隔（秒）
    'wakeup_wait_time': 5,         # Wake on LAN後の待機時間（秒）
    'shutdown_wait_time': 5        # シャットダウン後の待機時間（秒）
}

# SSHシャットダウン設定
SSH_CONFIG = {
    'username': 'user',            # デフォルトSSHユーザー名
    'password': None,              # デフォルトパスワード（Noneの場合は鍵認証を試みる）
    'timeout': 5                   # SSHコマンドタイムアウト（秒）
}
