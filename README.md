# バーコードスキャナー

React + AWS Lambda を使用したマルチフォーマットバーコード読み取りシステムです。

## 機能

- 📷 リアルタイムカメラスキャン
- 📁 ファイルアップロードスキャン
- 🎫 複数のチケット会社対応
- 📊 複数のバーコード形式対応
- 🎨 モダンなMaterial-UIデザイン
- 📱 レスポンシブデザイン

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

- **フロントエンド**: React 19, Material-UI 7
- **バーコード読み取り**: ZXing Library
- **HTTP通信**: Axios
- **ルーティング**: React Router DOM
- **カメラ**: WebRTC MediaDevices API

## セットアップ

### 前提条件

- Node.js 18以上
- npm または yarn

### インストール

```bash
# 依存関係をインストール
npm install

# 開発サーバーを起動
npm start
```

### 環境変数

`.env`ファイルを作成して以下の環境変数を設定してください：

```env
REACT_APP_API_URL=https://your-lambda-api.amazonaws.com/api/v1
REACT_APP_ENABLE_DEBUG=false
REACT_APP_MAX_FILE_SIZE=10485760
```

## 使用方法

1. **カメラモード**: リアルタイムでカメラを使用してバーコードをスキャン
2. **ファイルモード**: 画像ファイルをアップロードしてバーコードをスキャン
3. **設定**: チケット会社やバーコード形式を事前に指定可能
4. **結果表示**: スキャン結果を詳細に表示し、コピー機能も利用可能

## プロジェクト構造

```
src/
├── components/
│   ├── BarcodeScanner/     # メインスキャナーコンポーネント
│   ├── common/             # 共通コンポーネント
│   └── layout/             # レイアウトコンポーネント
├── hooks/                  # カスタムフック
├── services/               # APIサービス
├── utils/                  # ユーティリティ・定数
└── styles/                 # スタイル定義
```

## 開発

```bash
# 開発サーバー起動
npm start

# テスト実行
npm test

# 本番ビルド
npm run build

# 本番環境用ビルド
npm run build:prod

# ビルド結果の分析
npm run analyze
```

## ライセンス

MIT License

## 貢献

プルリクエストやイシューの報告を歓迎します。

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
