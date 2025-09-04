# slack-langchain-app
ChatGPT/LangChainによるチャットシステム構築実践入門のChapter 7

## 開発環境の構築

### 前提条件
- Python 3.10以上
- PyEnv（推奨）
- Node.js（Serverless Framework用）

### セットアップ手順

1. **リポジトリのクローン**
```bash
git clone <repository-url>
cd slack-langchain-app
```

2. **Python仮想環境の作成**
```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate
```

3. **Python依存関係のインストール**
```bash
# requirements.txtからインストール
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

4. **Node.js依存関係のインストール**
```bash
# Serverless Frameworkプラグインをインストール
npm install --save-dev serverless-python-requirements serverless-dotenv-plugin
```

5. **環境変数の設定**
```bash
# .envファイルを作成（.env.exampleを参考）
cp .env.example .env
# 必要な認証情報を設定
```

### 動作確認

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# アプリのインポートテスト
python -c "import app; print('✅ 依存関係チェック完了')"
python -c "from app import app, handler; print('✅ Lambda関数準備完了')"
```

### クリーンインストール（依存関係のリセット）

既存の環境をリセットしてクリーンインストールする場合：

```bash
# 1. 仮想環境を削除
rm -rf venv

# 2. 新しい仮想環境を作成
python -m venv venv

# 3. 仮想環境をアクティベート
source venv/bin/activate

# 4. requirements.txtからインストール
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### ローカル実行

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# ローカルでSlackアプリを実行
python app.py
```

### AWS Lambdaデプロイ

```bash
# Serverless Frameworkでデプロイ
npx serverless deploy --verbose
```
