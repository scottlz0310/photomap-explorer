# VS Code フリーズ復帰マニュアル

## AIチャット・GitHub Copilotフリーズ時の復帰手順

### 段階的復帰方法（効果の低い順から高い順）

#### 1. 軽度なフリーズ（推奨：最初に試す）

- ***先ず、ターミナルコンソールでエンターキーを押す。これで回復することが多い。***
- 以降の対策は上記で回復しない場合に行う。

```
Ctrl + Shift + P → "Developer: Restart Extension Host"
```
- 拡張機能ホストのみリスタート
- データ・作業内容は保持される
- 最も軽量で安全な方法

#### 2. 中度なフリーズ
```
Ctrl + Shift + P → "Developer: Reload Window"
```
- ウィンドウ全体をリロード
- 一部の未保存データが失われる可能性
- 設定・拡張機能は保持

#### 3. 重度なフリーズ
```
VS Code完全終了 → 再起動
```
- タスクマネージャーで「Code.exe」プロセス強制終了
- 最も確実だが、未保存データは失われる

### GitHub Copilot特有の対処法

#### コマンドパレット操作
```
Ctrl + Shift + P → "GitHub Copilot: Restart Language Server"
Ctrl + Shift + P → "GitHub Copilot: Reset Auth"
```

#### Copilotチャット特有
```
Ctrl + Shift + P → "GitHub Copilot Chat: Clear Session"
Ctrl + Shift + P → "GitHub Copilot Chat: Reset Conversation"
```

### 予防策・設定最適化

#### timeout設定の調整
```json
{
    "github.copilot.advanced": {
        "timeout": 30000,      // 30秒（デフォルト10秒より長く）
        "retries": 3,          // リトライ回数
        "debug": false         // デバッグログ無効でパフォーマンス向上
    }
}
```

#### メモリ使用量の制限
```json
{
    "extensions.autoUpdate": false,
    "workbench.settings.enableNaturalLanguageSearch": false,
    "editor.suggest.showWords": false  // 単語提案を無効化
}
```

### フリーズの原因と対策

#### 1. ネットワーク遅延
- **原因**: Copilotサーバーとの通信タイムアウト
- **対策**: timeout値を増加、VPN使用時は一時的に無効化

#### 2. メモリ不足
- **原因**: 大量のコンテキスト処理
- **対策**: 不要な拡張機能無効化、ファイル監視除外設定

#### 3. 拡張機能競合
- **原因**: 他のAI拡張機能との競合
- **対策**: 類似機能の拡張機能を一時的に無効化

### 緊急時のキーボードショートカット

```
Ctrl + Alt + Delete     → タスクマネージャー起動
Alt + F4               → アクティブウィンドウ強制終了
Ctrl + Shift + Esc     → タスクマネージャー直接起動
Windows + R, taskmgr   → タスクマネージャー起動
```

### プロセス終了手順

#### タスクマネージャーでの対象プロセス
1. `Code.exe` - VS Code本体
2. `Code.exe --type=extensionHost` - 拡張機能ホスト
3. `Code.exe --type=renderer` - レンダラープロセス

#### PowerShellでの一括終了
```powershell
# VS Code関連プロセス一括終了
Get-Process | Where-Object {$_.ProcessName -like "*Code*"} | Stop-Process -Force
```

### 作業データ保護

#### 自動保存設定
```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000,
    "workbench.editor.enablePreview": false
}
```

#### セッション復元設定
```json
{
    "window.restoreWindows": "all",
    "workbench.editor.restoreViewState": true
}
```

### 定期メンテナンス

#### 週次チェック項目
- [ ] 拡張機能の更新確認
- [ ] VS Code本体のアップデート
- [ ] 一時ファイルのクリーンアップ
- [ ] 設定ファイルのバックアップ

#### ログファイル確認
```
%APPDATA%\Code\logs\
%APPDATA%\Code\User\workspaceStorage\
```

### トラブルシューティングログ

#### 問題発生時の記録項目
1. 発生時刻
2. 実行していた操作
3. エラーメッセージ
4. 使用していた拡張機能
5. システムリソース使用状況

#### ログコマンド
```bash
# システムリソース確認
wmic process where name="Code.exe" get processid,workingsetsize,cpuusage
```

---

**注意**: フリーズが頻繁に発生する場合は、ハードウェア（RAM、ストレージ）の確認も推奨します。
