# app.py - メインアプリケーションファイル
from flask import Flask, render_template, jsonify, request
import os
import time
import threading
from utils.network import ping, wake_on_lan, shutdown_pc
import config

app = Flask(__name__, template_folder='src')

# コンフィグからPC情報を読み込み
PCs = {pc_id: {**pc_info, 'status': 'unknown'} for pc_id, pc_info in config.PCS_CONFIG.items()}

# PC操作のロック状態
operation_locks = {pc_id: False for pc_id in PCs.keys()}

def update_pc_status():
    """全PCの状態を定期的に更新する"""
    while True:
        for pc_id, pc in PCs.items():
            try:
                is_online = ping(pc['ip'])
                PCs[pc_id]['status'] = 'online' if is_online else 'offline'
            except:
                PCs[pc_id]['status'] = 'unknown'
        time.sleep(config.APP_CONFIG['status_update_interval'])

@app.route('/')
def index():
    """メインページの表示"""
    return render_template('index.html', pcs=PCs)

@app.route('/status')
def status():
    """PCの状態をJSON形式で返す"""
    return jsonify(PCs)

@app.route('/wake/<pc_id>', methods=['POST'])
def wake(pc_id):
    """指定PCのWake-on-LAN実行"""
    if pc_id not in PCs or operation_locks[pc_id]:
        return jsonify({'success': False, 'message': '操作できません'})
    
    # ロックを設定
    operation_locks[pc_id] = True
    
    # ステータスを処理中に設定
    PCs[pc_id]['status'] = 'waking'
    
    # 別スレッドでWake-on-LANを実行
    def wake_task():
        success = wake_on_lan(PCs[pc_id]['mac'])
        time.sleep(config.APP_CONFIG['wakeup_wait_time'])
        
        # 状態を更新（起動処理後にping確認）
        is_online = ping(PCs[pc_id]['ip'])
        PCs[pc_id]['status'] = 'online' if is_online else 'offline'
        
        # ロックを解除
        operation_locks[pc_id] = False
    
    threading.Thread(target=wake_task).start()
    
    return jsonify({'success': True, 'message': 'Magic Packet送信中'})

@app.route('/shutdown/<pc_id>', methods=['POST'])
def shutdown(pc_id):
    """指定PCのシャットダウン実行"""
    if pc_id not in PCs or operation_locks[pc_id]:
        return jsonify({'success': False, 'message': '操作できません'})
    
    # ロックを設定
    operation_locks[pc_id] = True
    
    # ステータスを処理中に設定
    PCs[pc_id]['status'] = 'shuttingdown'
    
    # 別スレッドでシャットダウンを実行
    def shutdown_task():
        # コンフィグからSSH設定を取得してシャットダウン実行
        success = shutdown_pc(
            PCs[pc_id]['ip'], 
            username=config.SSH_CONFIG['username'],
            timeout=config.SSH_CONFIG['timeout']
        )
        time.sleep(config.APP_CONFIG['shutdown_wait_time'])
        
        # 状態を更新
        is_online = ping(PCs[pc_id]['ip'])
        PCs[pc_id]['status'] = 'online' if is_online else 'offline'
        
        # ロックを解除
        operation_locks[pc_id] = False
    
    threading.Thread(target=shutdown_task).start()
    
    return jsonify({'success': True, 'message': 'シャットダウン中'})

if __name__ == '__main__':
    # 状態更新スレッドの開始
    status_thread = threading.Thread(target=update_pc_status)
    status_thread.daemon = True
    status_thread.start()
    
    # コンフィグからサーバー設定を読み込んでFlaskアプリの起動
    app.run(
        host=config.SERVER_CONFIG['host'], 
        port=config.SERVER_CONFIG['port'], 
        debug=config.SERVER_CONFIG['debug']
    )