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

.. sourcecode:: shellscript

    $ git ref 334a7dbbd5
    334a7dbbd5e32f5216aed0686642bb0992dc1b13

    $ git ref 1.0.3b
    dddcdb490a053897d3e193ddfe6b3c68ebaa3676

    $ git ref git ref refs/remotes/github/rewrite-parser
    6e79abd9c7a5ffd4876455aea0b751a8d457cb47

*--ls* オプションを `reference` につけると、リファレンスのタイプが *tree* であった場合、 `git ls-tree` を実行します。

.. sourcecode:: shellscript

    $ git ref --ls "HEAD^"
    100644 blob 6eb1b3968e50be8911ab440d809dbcd5c0eb42f8    .gitignore
    100644 blob 0be10ab5ed6ae100f249cddbaf6391f880d11cc7    LICENSE
    100644 blob 1f4a0dda59c4cb2954b96ce3a31951d269bf657c    README.rst
    100644 blob 375c486ceb657a1197806dee39f1583a497ac132    TODO
    100644 blob 5d44657229010a20e3a7deddeea99360958e9b43    commithash.py
    100644 blob 9cf656cb3b7b4d6ab76be914135e8fb6a397a7cf    git-todo2.py
    ----- (以下略) ----

*--type* オプションをつけると、リファレンスのタイプを出力します。

.. sourcecode:: shellscript

    $ git ref --type c2d6c39c3fb49563aac2b2013b56e41d70a8f509
    tree

*--file* オプションをつけてファイル名をセットすると、 *リファレンスにおけるファイルのハッシュ値* を出力します。

.. sourcecode:: shellscript

    $ git ref 334a7dbbd5 --file setup.py 
    8e722b2d697b472390f2c5a40a2d8422281fe868

*--pretty-print* オプションをつけてフィアル名をセットすると、 *リファレンスにおけるファイルの中身* を出力します。

.. sourcecode:: shellscript

    $ git ref 334a7dbbd5 --pretty-print setup.py 
    #!/usr/bin/env python
    #coding: utf-8

    import os
    from distutils.core import setup


    class Information(object):
        version = "1.0.2.1"
        author = "alice1017"
        author_github = "http://github.com/alice1017"
    
    ----- (以下略) ----
                 

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
