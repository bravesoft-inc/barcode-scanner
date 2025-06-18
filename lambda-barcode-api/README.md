# AWS Lambda バーコードスキャナー API

React + AWS Lambda を使用したマルチフォーマットバーコード読み取りシステムのバックエンドAPIです。

## 機能

- 📷 単一画像バーコードスキャン
- 📁 複数画像バッチスキャン
- 🎫 複数のチケット会社対応
- 📊 複数のバーコード形式対応
- 🔍 プロバイダー自動検出
- 📈 信頼度スコアリング
- 💾 DynamoDB保存機能

## 対応バーコード形式

- CODE128
- CODE39
- EAN13
- ITF
- CODABAR
- CODE93

## 対応チケット会社

- セブンチケット
- チケットぴあ
- ローソンチケット
- イープラス
- CNプレイガイド

## 技術スタック

- **AWS Lambda**: Python 3.11
- **API Gateway**: REST API
- **DynamoDB**: データ保存
- **S3**: MLモデル保存
- **SAM**: インフラストラクチャ
- **OpenCV**: 画像処理
- **PyZBar**: バーコード読み取り
- **Pillow**: 画像操作

## プロジェクト構造

```
lambda-barcode-api/
├── src/
│   ├── handlers/          # Lambdaハンドラー
│   │   ├── scan.py       # スキャン機能
│   │   ├── validate.py   # バリデーション
│   │   └── tickets.py    # チケット情報
│   ├── services/         # ビジネスロジック
│   │   ├── barcode_scanner.py
│   │   ├── image_processor.py
│   │   └── provider_parser.py
│   ├── utils/           # ユーティリティ
│   │   ├── response.py
│   │   ├── validation.py
│   │   └── constants.py
│   └── models/          # データモデル
├── layers/
│   └── python-libs/     # Lambda Layer
├── tests/               # テスト
├── template.yaml        # SAMテンプレート
├── requirements.txt     # 依存関係
└── deploy.sh           # デプロイスクリプト
```

## セットアップ

### 前提条件

- AWS CLI が設定済み
- AWS SAM CLI がインストール済み
- Python 3.11
- Docker（ローカルテスト用）

### インストール

```bash
# 依存関係をインストール
pip install -r requirements.txt

# Lambda Layer用の依存関係を準備
cd layers/python-libs
pip install -r requirements.txt -t python/
cd ../..
```

### ローカルテスト

```bash
# SAMローカルAPIを起動
sam local start-api

# 別のターミナルでテスト
curl -X POST http://localhost:3000/api/v1/scan \
  -F "image=@test-image.jpg" \
  -F "provider_hint=seven_ticket"
```

## デプロイ

### 開発環境

```bash
./deploy.sh dev ap-northeast-1
```

### 本番環境

```bash
./deploy.sh prod ap-northeast-1
```

### 手動デプロイ

```bash
# ビルド
sam build

# デプロイ
sam deploy \
  --stack-name barcode-scanner-api-dev \
  --region ap-northeast-1 \
  --parameter-overrides Environment=dev \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --confirm-changeset
```

## API エンドポイント

### 単一画像スキャン

```http
POST /api/v1/scan
Content-Type: multipart/form-data

Parameters:
- image: 画像ファイル
- provider_hint: プロバイダーヒント（オプション）
- format_hint: フォーマットヒント（オプション）
- enable_ml: ML予測有効化（デフォルト: true）
```

### バッチスキャン

```http
POST /api/v1/scan/batch
Content-Type: multipart/form-data

Parameters:
- images: 複数画像ファイル
- provider_hint: プロバイダーヒント（オプション）
- format_hint: フォーマットヒント（オプション）
```

### バーコード検証

```http
POST /api/v1/validate/{format}
Content-Type: application/json

Body:
{
  "barcode_data": "123456789",
  "provider": "seven_ticket"
}
```

### チケット情報取得

```http
GET /api/v1/tickets/{barcode}
```

## レスポンス形式

### 成功レスポンス

```json
{
  "success": true,
  "barcode_data": "23XXXXXX XXXXXXXX XXX",
  "detected_format": "CODE128",
  "confidence": 0.95,
  "provider": "seven_ticket",
  "parsed_data": {
    "provider": "seven_ticket",
    "provider_name": "セブンチケット",
    "ticket_number": "23XXXXXX",
    "serial_number": "XXXXXXXX",
    "check_digit": "XXX"
  },
  "processing_info": {
    "total_time_ms": 150,
    "preprocessing_variants": ["standard", "high_contrast"],
    "engines_tried": ["pyzbar", "opencv"],
    "ml_prediction_used": true
  }
}
```

### エラーレスポンス

```json
{
  "success": false,
  "error": {
    "message": "No barcode detected",
    "code": "HTTP_404"
  }
}
```

## 環境変数

| 変数名 | 説明 | デフォルト |
|--------|------|------------|
| `DYNAMODB_TABLE` | DynamoDBテーブル名 | 自動設定 |
| `LOG_LEVEL` | ログレベル | INFO |
| `PYTHONPATH` | Pythonパス | 自動設定 |

## 開発

### テスト実行

```bash
# ユニットテスト
pytest tests/

# カバレッジ付きテスト
pytest --cov=src tests/

# 型チェック
mypy src/
```

### コードフォーマット

```bash
# コードフォーマット
black src/

# リント
flake8 src/
```

## トラブルシューティング

### よくある問題

1. **依存関係エラー**
   ```bash
   # Lambda Layerを再構築
   cd layers/python-libs
   rm -rf python/
   pip install -r requirements.txt -t python/
   ```

2. **メモリ不足**
   - `template.yaml`で`MemorySize`を増加
   - 画像サイズを制限

3. **タイムアウト**
   - `template.yaml`で`Timeout`を増加
   - 画像前処理を最適化

### ログ確認

```bash
# CloudWatchログを確認
aws logs tail /aws/lambda/barcode-scan-dev --follow
```

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。 