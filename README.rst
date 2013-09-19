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


Copyright and License
#######################

Copyright Alice1017 All rights reserved.

License : MIT License

TODO
#########

.. include:: TODO
    :literal:

ChangeLog
##########

:ver 1.0.1: *ls* オプションでの出力形式を変更。hash値の緑をなくし、hash値も10文字に制限して、シンプルにみやすさを追求しました。

Author Info
############

:twitter id: `Alice1017 <http://twitter.com/alice1017>`_
:github id: `alice1017 <http://github.com/alice1017>`_
