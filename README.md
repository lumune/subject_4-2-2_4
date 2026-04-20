# YouTube Data API 動画検索ツール

Python + `requests` で YouTube Data API を呼び出し、動画を検索するサンプルです。  
検索結果から「動画タイトル」と「URL」を取得し、上位5件を表示します。

## 機能

- `.env` から API キー（`YOUTUBE_API_KEY`）を読み込み
- 検索キーワードを指定して動画検索
- 並び替えオプションを選択可能
  - 再生回数順
  - 最新動画順
  - 指定なし
- 結果を上位5件表示（タイトル + URL）

## 動作環境

- Python 3.9 以上
- `requests`

## セットアップ

### 1. ライブラリのインストール

```bash
pip install requests
```

### 2. API キーの設定

`.env.example` を参考に、プロジェクト直下に `.env` を作成して以下を設定してください。

```env
YOUTUBE_API_KEY=YOUR_YOUTUBE_DATA_API_KEY
```

## 実行方法

### 対話式（おすすめ）

引数なしで実行すると、ターミナルで順番に入力できます。

1. 検索キーワード  
2. 並び替えオプション（1/2/3）

```bash
python3 youtube_search.py
```

### 引数指定

```bash
python3 youtube_search.py "Python 入門" --sort views
```

`--sort` は以下から選べます。

- `views` : 再生回数順
- `latest` : 最新動画順
- `none` : 指定なし

## 出力例

```text
検索キーワード: "Python 入門"
上位5件の結果:

1. タイトル: 〇〇〇
   URL: https://www.youtube.com/watch?v=xxxxxxxxxxx
```

## よくあるエラー

### `.env に YOUTUBE_API_KEY を設定してください。`

`.env` が存在しない、または `YOUTUBE_API_KEY` が未設定です。  
`.env` の内容を確認してください。

### `TypeError: unsupported operand type(s) for | ...`

Python 3.9 で `str | None` 記法を使った場合に出るエラーです。  
現在のコードは `Optional[str]` を使用しているため、同エラーは解消済みです。

## ファイル構成

- `youtube_search.py` : メインスクリプト
- `.env.example` : 環境変数設定のサンプル
