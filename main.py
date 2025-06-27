"""
PhotoMap Explorer メインエントリーポイント

Usage:
    python main.py              # デフォルト（レガシーUI）
    python main.py --ui=new     # 新UI（Clean Architecture）
    python main.py --ui=legacy  # レガシーUI（従来版）
    python main.py --ui=hybrid  # ハイブリッド（両方表示）
"""

import sys
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)


def parse_arguments():
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(
        description="PhotoMap Explorer - 写真地図表示アプリケーション",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
UI選択例:
  python main.py --ui=new     # 新しいClean ArchitectureUI
  python main.py --ui=legacy  # 従来のレガシーUI
  python main.py --ui=hybrid  # ハイブリッド比較表示
        """
    )
    
    parser.add_argument(
        '--ui', 
        choices=['new', 'legacy', 'hybrid'], 
        default='legacy',
        help='使用するUIアーキテクチャ (default: legacy)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='デバッグモードで実行'
    )
    
    return parser.parse_args()


def launch_new_ui(debug=False):
    """新UI（Clean Architecture）を起動"""
    try:
        from presentation.views.simple_main_view import SimpleNewMainWindow
        
        window = SimpleNewMainWindow()
        window.show()
        
        if debug:
            print("✅ 新UI（Clean Architecture）起動成功")
            window.show_status_message("新UI（Clean Architecture）で起動しました")
        
        return window
        
    except Exception as e:
        if debug:
            print(f"❌ 新UI起動エラー: {e}")
            import traceback
            traceback.print_exc()
        
        # フォールバック：レガシーUIで起動
        print("⚠️ 新UIでエラーが発生しました。レガシーUIで起動します。")
        return launch_legacy_ui(debug)


def launch_legacy_ui(debug=False):
    """レガシーUI（従来版）を起動"""
    try:
        from window.main_window import MainWindow
        
        window = MainWindow()
        window.show()
        
        if debug:
            print("✅ レガシーUI（従来版）起動成功")
        
        return window
        
    except Exception as e:
        if debug:
            print(f"❌ レガシーUI起動エラー: {e}")
            import traceback
            traceback.print_exc()
        raise


def launch_hybrid_ui(debug=False):
    """ハイブリッドUI（両方表示）を起動"""
    try:
        # Phase 4で作成したハイブリッドアプリケーションを使用
        from test_phase4_final import FinalIntegrationWindow
        
        window = FinalIntegrationWindow()
        window.setWindowTitle("PhotoMap Explorer - ハイブリッド統合版")
        window.show()
        
        if debug:
            print("✅ ハイブリッドUI起動成功")
        
        return window
        
    except Exception as e:
        if debug:
            print(f"❌ ハイブリッドUI起動エラー: {e}")
            import traceback
            traceback.print_exc()
        
        # フォールバック：レガシーUIで起動
        print("⚠️ ハイブリッドUIでエラーが発生しました。レガシーUIで起動します。")
        return launch_legacy_ui(debug)


def main():
    """メインエントリーポイント"""
    args = parse_arguments()
    
    if args.debug:
        print(f"🚀 PhotoMap Explorer 起動中... (UI: {args.ui}, Debug: {args.debug})")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("PhotoMap Explorer Project")
    
    # UIアーキテクチャに応じて起動
    try:
        if args.ui == 'new':
            window = launch_new_ui(args.debug)
        elif args.ui == 'hybrid':
            window = launch_hybrid_ui(args.debug)
        else:  # legacy (default)
            window = launch_legacy_ui(args.debug)
        
        if args.debug:
            print("📋 使用方法:")
            print("  --ui=new     新しいClean ArchitectureUI")
            print("  --ui=legacy  従来のレガシーUI")
            print("  --ui=hybrid  ハイブリッド比較表示")
            print("  --debug      デバッグ情報表示")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()