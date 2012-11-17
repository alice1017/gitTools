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

.. image:: https://www.evernote.com/shard/s14/sh/d6c51c36-33f6-4989-a291-823f4258cc3b/331c709c39691598a1e75107ce0e700e/res/0ce740e6-c347-4a32-bc17-cb01fea94bf6/skitch.png

.. sourcecode:: shellscript

    $ commithash get 2

　**get** オプションを指定して **コミットのインデックス** を指定すると、指定されたインデックスのhash値を取得することができます。
ここでいう **コミットのインデックス** とは、 *ls* オプションで黄色に表示された数字のことを指します。


　このgitToolsはこれからもっと増えていく予定です。

Copyright and License
#######################

Copyright Alice1017 All rights reserved.

License : MIT License

Author Info
############

:twitter id: `Alice1017 <http://twitter.com/alice1017>`_
:github id: `alice1017 <http://github.com/alice1017>`_
