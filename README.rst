What's gitTools?
###################

**gitTools** はコマンドラインで動かせるgitの少し使いにくいところを使いやすくするために開発されたものです。


What Tools?
------------

commandhash
^^^^^^^^^^^^

　これはgitのコミットキー(hash)を扱うことに便利なツールです。

.. sourcecode:: shellscript

    $ commithash

　このようにオプション無しで起動させると、現在のgitリポジトリの **最後のコミットのhash値** を取得できます。

.. sourcecode:: shellscript

    $ commithash ls

　**ls** オプションを指定すると、 現在のgitリポジトリのコミットの一覧を見ることができます。

.. image:: https://raw.github.com/alice1017/gitTools/master/ss/commithash.png

.. sourcecode:: shellscript

    $ commithash get 2

　**get** オプションを指定して **コミットのインデックス** を指定すると、指定されたインデックスのhash値を取得することができます。
ここでいう **コミットのインデックス** とは、 *ls* オプションで黄色に表示された数字のことを指します。

commithashの便利な使い方
~~~~~~~~~~~~~~~~~~~~~~~~

たとえば、 *git ls-tree* コマンドを使うとき等。

.. sourcecode:: shellscript

    $ git ls-tree `commithash get 4`

このようにすると、 **HEAD^^^** こんなことしなくてもよくなるし、 **古いコミットの参照がよりやりやすくなります** 。


　このgitToolsはこれからもっと増えていく予定です。

git-ref
^^^^^^^^^^^

　これはgitのreferenceにおけるハッシュ操作を便利にするスクリプトです。

.. sourcecode:: shell 

    usage: git ref [-h] [-l] [-t] [-f FILE] [-p FILE] reference

    This script can show reference hash or files easyly.

    positional arguments:
      reference             Please set hash of reference. If you not set other
                            options, script show full hash value.

    optional arguments:
      -h, --help            show this help message and exit
      -l, --ls              Show all files with hash in commit.
      -t, --type            Show type of hash.
      -f FILE, --file FILE  Show file object hash in commit.
      -p FILE, --pretty-print FILE
                            Show file contents.

*reference* を引数に取ります。 `reference` はハッシュ値でも、タグ名でも、gitで使えるリファレンスならなんでも可能です。

*--ls* オプションを `reference` につけると、リファレンスのタイプが *tree* であった場合、 `git ls-tree` を実行します。

*--type* オプションをつけると、リファレンスのタイプを出力します。

*--file* オプションをつけてファイル名をセットすると、 *リファレンスにおけるファイルのハッシュ値* を出力します。

*--pretty-print* オプションをつけてフィアル名をセットすると、 *リファレンスにおけるファイルの中身* を出力します。



Copyright and License
#######################

Copyright Alice1017 All rights reserved.

License : MIT License

TODO
#########

`こちらを参照 <https://github.com/alice1017/gitTools/blob/rewrite-parser/TODO>`_

ChangeLog
##########

:ver 1.0.1: *ls* オプションでの出力形式を変更。hash値の緑をなくし、hash値も10文字に制限して、シンプルにみやすさを追求しました。

Author Info
############

:twitter id: `Alice1017 <http://twitter.com/alice1017>`_
:github id: `alice1017 <http://github.com/alice1017>`_
