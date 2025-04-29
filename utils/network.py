import os
import socket
import subprocess

def ping(host):
    """PINGでPCの状態を確認"""
    try:
        # Windowsとそれ以外でpingコマンドのオプションが異なる
        param = '-n' if os.name == 'nt' else '-c'
        # pingコマンドを実行
        result = subprocess.run(['ping', param, '1', host], 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               timeout=2)
        return result.returncode == 0
    except:
        return False

def wake_on_lan(mac_address):
    """Wake-on-LANパケットを送信"""
    if len(mac_address) == 17:
        # MACアドレスからコロン(:)を削除
        mac_address = mac_address.replace(':', '')
    elif len(mac_address) != 12:
        return False
    
    # マジックパケットの作成
    data = 'FF' * 6 + mac_address * 16
    send_data = b''
    
    # 16進数文字列をバイトに変換
    for i in range(0, len(data), 2):
        send_data += bytes([int(data[i:i+2], 16)])
    
    # ブロードキャストで送信
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, ('255.255.255.255', 9))
    sock.close()
    
    return True

def shutdown_pc(ip, username='user', timeout=5):
    """PCをシャットダウン（SSHを使用）"""
    try:
        # シャットダウンコマンドを実行（実際の環境に合わせて調整が必要）
        # 例: Windows PCの場合はリモートシャットダウンコマンド
        result = subprocess.run(['ssh', f'{username}@{ip}', 'shutdown', '/s', '/t', '0'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True,
                               timeout=timeout)
        return result.returncode == 0
    except:
        return False