## このリポジトリについて
SwitchBotハブ無しにAmazon AlexaからSwitchBotをコントロールするためのアプリです。

詳細は以下のQiitaにまとめています。

[ラズパイをハブとしてアレクサからSwitchBotを操作する](https://qiita.com/quotto/items/dbe7d87c471282abe95d)

アプリはPubSubモデルで構成しています。

### Publisher
[publisher](./publisher)
アレクサからの命令を受けてSwitchBotへの命令を発信するアレクサスキル。

### Subscriber
[subscriber](./subscriber/)
Publisherからのを受け取ってSwitchBotにBluetoothの命令を飛ばすPythonスクリプト
