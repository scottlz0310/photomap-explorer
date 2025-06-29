#!/bin/bash
# PhotoMap Explorer v2.1.2 Build Script
# Windows用スタンドアロン実行ファイル生成

echo "PhotoMap Explorer v2.1.2 Build Script"
echo "======================================"

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "エラー: 仮想環境が見つかりません。先にsetup_environment.batを実行してください。"
    exit 1
fi

# 仮想環境のアクティベート
source venv/Scripts/activate

echo "仮想環境をアクティベートしました"

# PyInstallerのインストール確認
echo "PyInstallerのインストール確認..."
pip show pyinstaller > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "PyInstallerをインストール中..."
    pip install pyinstaller
fi

# 古いビルドファイルのクリーンアップ
echo "古いビルドファイルをクリーンアップ中..."
if [ -d "build" ]; then
    rm -rf build
fi
if [ -d "dist" ]; then
    rm -rf dist
fi

# PyInstallerでビルド実行
echo "PyInstallerでビルド実行中..."
pyinstaller photomap-explorer.spec

# ビルド結果の確認
if [ -f "dist/photomap-explorer/photomap-explorer.exe" ]; then
    echo ""
    echo "✅ ビルドが正常に完了しました！"
    echo "📁 実行ファイル: dist/photomap-explorer/photomap-explorer.exe"
    echo ""
    echo "配布用フォルダ: dist/photomap-explorer/"
    echo "このフォルダ全体をコピーして配布できます。"
else
    echo ""
    echo "❌ ビルドに失敗しました。"
    echo "エラーログを確認してください。"
fi

# 仮想環境の無効化
deactivate
echo "仮想環境を無効化しました"
