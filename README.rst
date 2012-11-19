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

.. image:: http://d3j5vwomefv46c.cloudfront.net/photos/full/689490316.png?key=1064649&Expires=1353307504&Key-Pair-Id=APKAIYVGSUJFNRFZBBTA&Signature=FQsSpPgG8LpymcNcSuEKUiWrduN5ckQITeol6qpyq6whFAqt2x-GrJj4bu0uQE0gtiQMFSkLat3BsW-qcKMH2~Au8qGRKa1w5eZJXboGkvKlk3LvpLSbSofkfTWbNlAK15J3gWR0eNPMaKCoB0sHePnNul8bI5NUFH0pb85Uu0M_

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

Author Info
############

:twitter id: `Alice1017 <http://twitter.com/alice1017>`_
:github id: `alice1017 <http://github.com/alice1017>`_
