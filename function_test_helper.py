#!/usr/bin/env python3
"""
PhotoMap Explorer 機能確認ヘルパー

修正後のアプリケーションの機能を確認するためのスクリプト
"""

import subprocess
import time

def check_application_status():
    """アプリケーションの状態を確認"""
    print("🔍 PhotoMap Explorer 機能確認開始")
    print("="*60)
    
    # プロセス確認
    try:
        result = subprocess.run(['pgrep', '-f', 'python main.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            pid = result.stdout.strip()
            print(f"✅ アプリケーション実行中 (PID: {pid})")
            
            # CPU・メモリ使用率確認
            ps_result = subprocess.run(['ps', '-p', pid, '-o', '%cpu,%mem,etime'], 
                                     capture_output=True, text=True)
            if ps_result.returncode == 0:
                lines = ps_result.stdout.strip().split('\n')
                if len(lines) >= 2:
                    stats = lines[1].strip().split()
                    if len(stats) >= 3:
                        cpu, mem, etime = stats[0], stats[1], stats[2]
                        print(f"📊 リソース使用状況:")
                        print(f"   CPU: {cpu}%, メモリ: {mem}%, 稼働時間: {etime}")
            
            return True
        else:
            print("❌ アプリケーションが実行されていません")
            return False
            
    except Exception as e:
        print(f"❌ プロセス確認エラー: {e}")
        return False

def display_updated_test_checklist():
    """更新された手動テストチェックリストを表示"""
    print("\n" + "="*60)
    print("📋 修正後 PhotoMap Explorer 手動テストチェックリスト")
    print("="*60)
    print("🔧 修正内容:")
    print("   ✅ フォルダイベントハンドラー接続")
    print("   ✅ テーマイベントハンドラー接続")
    print("   ✅ 画像イベントハンドラー接続")
    print("   ✅ メソッド名修正 (initialize_theme)")
    print("")
    
    checklist = [
        ("🔍 基本動作 - 再テスト推奨", [
            "ウィンドウが正常に表示される",
            "タイトルバーに適切なタイトルが表示される",
            "ツールバーにフォルダ選択とテーマボタンが表示される",
            "左右のパネルが表示される"
        ]),
        ("🗂️ フォルダ選択機能 - 修正済み", [
            "「📁 フォルダ選択」ボタンがクリック可能",
            "フォルダ選択ダイアログが開く", 
            "選択したフォルダの内容が処理される",
            "画像ファイルの検出が動作する"
        ]),
        ("🎨 テーマ機能 - 修正済み", [
            "「🌙 ダーク」ボタンがクリック可能",
            "ライト/ダークテーマの切り替えができる",
            "テーマ変更が即座に反映される",
            "設定が正しく保存される"
        ]),
        ("🖼️ 画像機能 - イベントハンドラー接続済み", [
            "画像選択時のイベント処理が動作する",
            "画像プレビューが表示される（実装状況による）",
            "EXIF情報の読み取りが動作する",
            "GPS情報の抽出が動作する"
        ]),
        ("🗺️ 地図機能 - 基盤整備済み", [
            "地図パネルが表示される",
            "GPS情報を持つ画像のマーカー表示準備完了",
            "地図の基本操作が可能",
            "マーカークリック時のイベント処理準備完了"
        ])
    ]
    
    for category, items in checklist:
        print(f"\n{category}:")
        for item in items:
            print(f"   □ {item}")
    
    print(f"\n{'='*60}")
    print("💡 優先テスト項目 (修正済み機能):")
    print("   1. 📁 フォルダ選択ボタンのクリック")
    print("   2. 🌙 テーマ切り替えボタンのクリック")
    print("   3. フォルダ選択ダイアログの動作確認")
    print("   4. テーマ変更の視覚的確認")
    print("")
    print("🔍 確認方法:")
    print("   - アプリケーションウィンドウで実際にボタンをクリック")
    print("   - ダイアログが開くか、テーマが変わるかを確認")
    print("   - 問題があればコンソール出力を確認")

def main():
    """メイン実行関数"""
    if check_application_status():
        display_updated_test_checklist()
        
        print(f"\n{'='*60}")
        print("🎉 アプリケーションは修正され、手動テストの準備が整いました！")
        print("上記のチェックリストに従って機能を確認してください。")
        
    else:
        print("⚠️ アプリケーションが実行されていません。")
        print("まず 'python main.py' でアプリケーションを起動してください。")

if __name__ == "__main__":
    main()
