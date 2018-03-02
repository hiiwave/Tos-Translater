# Tos-Translator

A translation tool for [Tree of Savior](https://treeofsavior.com/page/main/) game by mapping language files from different clients. This tool makes it possible to enjoy your favorite language in your favorite game server. Currently playing [itos](https://treeofsavior.com/page/main/) in Chinese(zh-tw) and playing [tw-tos](http://tos.x2game.com.tw/) in English are supported.

To download the translated languaged files, please visit the [release page](https://github.com/hiiwave/Tos-Translater/releases).

To use this tool to generate translated language files, please read the followings.

## Usage:

Prepare [Python 3](https://www.python.org/) environment with [pandas](http://pandas.pydata.org/) installed, run
```
python main.py
```

The translated files will be in `output/` folder.

## Methodology

In fact, this tool does not do any *translation*; instead it *maps* the language files from different clients. 

In Tree of Savior game, there is a tricky part that the item ids in different client *mismatch*.
For example the item id of `Tea Set (茶果組合, 다과 세트)` is `ITEM_20170726_015270` in itos, but `ITEM_20170731_015184` in tw-tos.
It prevents us from using the English language files from itos directly into tw-tos, and vice versa.

Fortunately, the korean content is reserved in tw-tos language files, and there is a [group]((https://github.com/Treeofsavior/EnglishTranslation)) actively maintaining the mapping from Korean to English in itos.
Hence it's possible to use the Korean content to match language data from different clients, and this is what this project actually does.

## Other Language Support:
For Korean to English translation, there is already a group actively doing this. Please visit [here](https://github.com/Treeofsavior/EnglishTranslation).

Theoretically, it's possible to support more languages without difficulty, including:
- [ktos](http://tos.nexon.com) in Chinese
- [jtos](http://tos.nexon.co.jp/) in English
- [itos](https://treeofsavior.com/page/main/) in Japnese

Since I don't know if there is such demand, and I'm not familiar with those languages, the development of these language support is not done yet. Let me know if you're interested and want to contribute.

## Credits
This tool is open-sourced by player 波光粼粼 at guild [夏祭](https://forum.gamer.com.tw/C.php?bsn=19840&snA=29788) in tw-tos.

The Korean to English Translation is cloned from [here](https://github.com/Treeofsavior/EnglishTranslation). I really appreciate their efforts.

All of the original contents belong to Tree of Savior official group.

## Contribution
Any issue reporting or pull request is welcome. 

## LICENSE
[MIT](https://github.com/hiiwave/Tos-Translater/blob/master/LICENSE)