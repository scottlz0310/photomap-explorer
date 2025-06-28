@echo off
REM PhotoMap Explorer v2.1.2 Build Script for Windows
REM Windows用スタンドアロン実行ファイル生成

echo PhotoMap Explorer v2.1.2 Build Script
echo ======================================

REM 仮想環境の確認
if not exist "venv" (
    echo エラー: 仮想環境が見つかりません。先にsetup_environment.batを実行してください。
    pause
    exit /b 1
)

REM 仮想環境のアクティベート
call venv\Scripts\activate.bat
echo 仮想環境をアクティベートしました

REM PyInstallerのインストール確認
echo PyInstallerのインストール確認...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstallerをインストール中...
    pip install pyinstaller
)

REM 古いビルドファイルのクリーンアップ
echo 古いビルドファイルをクリーンアップ中...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM PyInstallerでビルド実行
echo PyInstallerでビルド実行中...
pyinstaller photomap-explorer.spec

REM ビルド結果の確認
if exist "dist\photomap-explorer\photomap-explorer.exe" (
    echo.
    echo ✅ ビルドが正常に完了しました！
    echo 📁 実行ファイル: dist\photomap-explorer\photomap-explorer.exe
    echo.
    echo 配布用フォルダ: dist\photomap-explorer\
    echo このフォルダ全体をコピーして配布できます。
) else (
    echo.
    echo ❌ ビルドに失敗しました。
    echo エラーログを確認してください。
)

REM 仮想環境の無効化
call venv\Scripts\deactivate.bat
echo 仮想環境を無効化しました

pause
