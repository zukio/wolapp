import os
import socket
import subprocess
import platform


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


def shutdown_pc(ip, username='user', password=None, timeout=5):
    """PCをシャットダウン（Windows/Linuxに対応）"""
    try:
        is_windows = platform.system() == 'Windows'

        if is_windows:
            # Windowsの場合はnet use / shutdownコマンドを使用
            if password:
                # まずネットワーク共有に接続（認証が必要な場合）
                connect_cmd = ['net', 'use',
                               f'\\\\{ip}', f'/user:{username}', password]
                try:
                    subprocess.run(connect_cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   text=True,
                                   timeout=timeout)
                except:
                    pass  # 接続に失敗しても次の処理へ

            # リモートシャットダウンコマンドを実行
            shutdown_cmd = ['shutdown', '/s',
                            '/f', '/m', f'\\\\{ip}', '/t', '0']
            result = subprocess.run(shutdown_cmd,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    text=True,
                                    timeout=timeout)
        else:
            # Linux/Mac環境ではSSHを使用
            ssh_cmd = ['ssh']

            # パスワードがない場合は鍵認証を試みる
            if not password:
                ssh_cmd.extend(
                    [f'{username}@{ip}', 'sudo', 'shutdown', '-h', 'now'])
                result = subprocess.run(ssh_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        timeout=timeout)
            else:
                # パスワード認証の場合はsshpassを使う
                # 注: sshpassのインストールが必要
                ssh_cmd = ['sshpass', '-p', password, 'ssh',
                           f'{username}@{ip}', 'sudo', 'shutdown', '-h', 'now']
                result = subprocess.run(ssh_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True,
                                        timeout=timeout)

        return result.returncode == 0
    except Exception as e:
        print(f"シャットダウンエラー: {e}")
        return False
