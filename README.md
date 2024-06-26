# AICommentaryVision

AICommentaryVisionは、AIを使用してゲーム実況や物語の朗読動画を自動生成するPythonプロジェクトです。このプロジェクトでは、OpenAI APIとClaude APIを使用して、実況者や朗読者のセリフを生成し、VOICEVOXやStyle-Bert-VITS2を使用して音声を合成します。生成された動画は、YouTubeやニコニコ動画などのプラットフォームにアップロードすることができます。

## 注意事項

このプロジェクトは現在開発中であり、まだ一般のユーザーが使用することを前提としていません。プロジェクトの構造や機能は変更される可能性があり、一部の機能は未実装または不完全な状態です。このREADMEは、開発者向けの情報提供を目的としており、一般のユーザーによる使用を推奨するものではありません。

以下に、現在の主な未実装ポイントや注意事項を記載します。

- 番組情報の編集をGUI上からできず、直接ハードコードする必要があります。
- ゲーム実況動画の自動生成は未実装です。
- Style-Bert-VITS2 を使用した音声合成は未検証です。
- 動画のアップロード機能は未実装です。
- Claude3への対応を行ったあとGPT-4側をメンテしていないので動作しない可能性があります。
- このプロジェクトではOpenAI APIとClaude APIを使用するため、それぞれのサービスの料金が発生します。APIの使用量に応じた課金にご注意ください。


## 主な機能

- ゲーム実況動画の自動生成（未実装）
- 物語の朗読動画の自動生成
- 複数の実況者や朗読者のセリフ生成
- VOICEVOXとStyle-Bert-VITS2による音声合成
- 動画の自動生成
- 動画の自動アップロード（未実装）

## 必要な環境

- Python 3.7以上
- VOICEVOX Engine
- Style-Bert-VITS2
- OpenAI API キー
- Claude API キー

## インストール

1. このリポジトリをクローンします。

git clone https://github.com/yourusername/AICommentaryVision.git


2. 必要なPythonパッケージをインストールします。

pip install -r requirements.txt


3. VOICEVOX EngineとStyle-Bert-VITS2をインストールし、起動します。

4. `.env`ファイルを作成し、APIキーを設定します。

OPENAI_API_KEY=your_openai_api_key
CLAUDE_API_KEY=your_claude_api_key


## 使用方法

1. `webui.py`を実行して、Gradioのウェブインターフェースを起動します。

python src/webui.py

2. ウェブブラウザで`http://localhost:7860`にアクセスします。

3. ストリーマーと番組の情報を編集し、動画作成セクションで必要な情報を入力します。

4. ストリーマーと番組の情報に設定した、立ち絵、背景、BGMをdataフォルダに入力します。

5. デバッグモードのチェックボックスを外します（外さずに実行すると外部APIを使用せず、動作確認用のダミーテキストが使用されます。）

4. 「動画作成開始」ボタンをクリックすると、動画の生成が開始されます。

5. 生成された動画は、output/(動画タイトル)_(日時)ディレクトリに保存されます。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、`LICENSE`ファイルを参照してください。

## 謝辞

このREADMEは、[generate-project-summary](https://github.com/Olemi-llm-apprentice/generate-project-summary)とClaude3を使用して作成されました。これらのツールを提供してくださった開発者の方々に感謝いたします。

## 免責事項

このプロジェクトは、AIを使用して動画を自動生成するためのサンプルコードです。生成された動画の内容や品質、著作権については、使用者の責任において確認と管理を行ってください。
