# Zenn CLI

* [📘 How to use](https://zenn.dev/zenn/articles/zenn-cli-guide)

---

# Zenn 執筆ワークフロー in Neovim

## 0. 事前準備

執筆を始める前に、プロジェクトのルートで以下の準備が必要です。

```bash
# Zenn CLIのセットアップ
npm init zenn
# プレビュー用のディレクトリ作成
mkdir -p articles/images

```

## 1. 執筆フロー

### ステップ1: 記事の新規作成

1. `<leader>e` で **Neo-tree** を開きます。
2. `articles` ディレクトリを選択し、**`A`** キーを叩きます。 or  npx zenn new:article でファイルを初期化する。
3. カスタムスクリプト `randomfilename.lua` が起動し、Zennの仕様に最適なランダムなファイル名（スラッグ）が自動入力されます。

### ステップ2: Front Matter の挿入

1. 作成したファイルを開き、**`zenn`** と入力して `Tab` キー（LuaSnip）を叩きます。
2. 以下のテンプレートが挿入されます。タイトルや絵文字を順次入力してください。
```yaml
---
title: "タイトル"
emoji: "😺"
type: "tech"
topics: ["tags"]
published: false
---

```

### ステップ3: 画像の貼り付け

1. ブラウザやツールで画像をコピーします。
2. Neovim上で **`<leader>p`** を押すと、`articles/images/` に画像が自動保存され、Markdown用のリンクが挿入されます（`img-clip.nvim`）。

### ステップ4: AIによる推敲と構成

1. **`<leader>aa`** で `CodeCompanion` チャットを開きます。
2. 日本語に最適化されたシステムプロンプトを使用して、「技術的な誤りのチェック」や「構成案の作成」を依頼できます。
3. 特定の段落を選択して **`<leader>ai`** を押せば、その場で文章の推敲が可能です。

### ステップ5: ローカルプレビュー

1. **`<leader>zp`** を押して、`ToggleTerm` 経由で `npx zenn preview` を起動します。
2. ブラウザで `http://localhost:8000` を開き、リアルタイムで仕上がりを確認します。

## 2. セキュリティと公開

### 機密情報のチェック

コミット時に `pre-commit` が走り、`detect-secrets` が記事内に誤ってAPIキーやパスワードを記述していないか自動チェックします。

### 公開

1. `published: false` を `true` に書き換えます。
2. `vim-fugitive` を使用して、Neovim内からコミット・プッシュします。
```vim
:Git add .
:Git commit -m "Add new article"
:Git push

```



## 3. 主なキーマッピング一覧

| キー | 機能 | 備考 |
| --- | --- | --- |
| `<leader>e` | Neo-tree開閉 |  |
| `A` (in Neo-tree) | ランダム名でファイル作成 |  |
| `zenn` + `Tab` | Zennテンプレート挿入 | LuaSnip |
| `<leader>p` | クリップボードから画像貼付 | img-clip |
| `<leader>aa` | AIチャット (CodeCompanion) |  |
| `<leader>ai` | インラインAI編集 |  |
| `<leader>zp` | Zennプレビュー起動/停止 |  |
| `<leader><leader>` | 汎用ターミナル (dstask等) |  |

