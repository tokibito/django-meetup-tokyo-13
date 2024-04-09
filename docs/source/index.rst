DjangoMeetupTokyo #13 中級者向けハンズオン
==========================================

イベント概要
------------

https://django.connpass.com/event/312782/

中級者向けハンズオンについて
----------------------------

チュートリアルは理解できている、Djangoは使ったことあるけど、使いこなせてない～という人向けのハンズオンです。 用意した資料を見ながら課題を実装していきます。

ショッピングカート、注文フォームの実装を通じて、Djangoのセッション、フォーム、汎用ビューなどの使い方を学びます。

作業環境の準備
--------------

* Python 3.12（Python3.10以上）
    * venvモジュールが使える状態にしてください。Ubuntuなどの環境では ``python3.12-venv`` のようなパッケージを入れる必要があるかもしれません。
    * ``python3.12 -m venv venv``
* Django 5.0系（最新 5.0.4）
    * venv環境にインストールしておいてください。
* VisualStudioCodeまたは、使い慣れたエディター
    * Python, Djangoで開発できる状態にしておいてください。

このハンズオンの完成形のコード
------------------------------

GitHub上に完成形のコードがあります。コードを書き進めていて、うまく動かない場合に参考にしてみてください。

https://github.com/tokibito/django-meetup-tokyo-13/

資料
----

https://tokibito.github.io/django-meetup-tokyo-13/

作成するアプリケーションについて
--------------------------------

会議室の予約システムを想定したアプリケーションを作成します。

ユーザーの種別
~~~~~~~~~~~~~~~~~~~

このシステムを利用するユーザーの種別は以下の３種類を想定します。

* 一般ユーザー `user_type:general` 
    * 一般ユーザーが利用可能な会議室を予約できます。
* 特別ユーザー `user_type:special` 
    * 一般ユーザーが利用可能な会議室に加えて、特別ユーザーが利用可能な会議室を予約できます。
* 管理者ユーザー `user_type:superuser` 
    * 管理者ユーザーのみが利用できる会議室を含む、すべての会議室を予約できます。

会議室一覧
~~~~~~~~~~~~~

利用可能な会議室の一覧を表示します。ログインしていない場合でも閲覧できるページです。

ログインしている場合は、会議室の予約フォームへのリンクが表示されます。

ログイン
~~~~~~~~~~~~~

ユーザーアカウントを使ってログインします。

ログアウト
~~~~~~~~~~~~~

ログイン中のユーザーをログアウトします。

予約フォーム
~~~~~~~~~~~~~~~

ログイン中のユーザーで、会議室を予約します。

自分の予約一覧
~~~~~~~~~~~~~~~~~

ログイン中のユーザーの予約の一覧を表示します。

ユーザー登録
~~~~~~~~~~~~~~~~~

ユーザー登録をする画面です。

プロジェクトの作成とセットアップ
--------------------------------

Djangoのプロジェクト作成
~~~~~~~~~~~~~~~~~~~~~~~

今回は ``myproject`` という名前のプロジェクトで作成します。

.. code-block::

   (venv)$ django-admin startproject myproject
   (venv)$ cd myproject

**以降の説明は、このmyprojectディレクトリ以下を起点とします。**

管理者ユーザーの作成
~~~~~~~~~~~~~~~~~~~

Django管理サイト用のユーザーを作成しておきます。

.. code-block::

   (venv)$ python manage.py createsuperuser

django-debug-toolbarのセットアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-debug-toolbarをインストール、セットアップしておきます。

.. code-block::

   (venv)$ pip install django-debug-toolbar

.. note::

   - `django-debug-toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_
   - `はじめてのDjangoアプリ作成、その8 | Django ドキュメント <https://docs.djangoproject.com/ja/5.0/intro/tutorial08/>`_

myproject/settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "debug_toolbar",
   ]

.. code-block:: python

   INTERNAL_IPS = [
       "127.0.0.1",
   ]

.. code-block:: python

   MIDDLEWARE = [
       "debug_toolbar.middleware.DebugToolbarMiddleware",
       # ...
   ]

.. note::

   ``DebugToolbarMiddleware`` は、なるべく外側に配置したほうがよいとドキュメントに書かれています。
   GZipMiddlewareのように、レスポンスボディを加工するミドルウェアを使っている場合は、それよりも後に配置する必要があります。
   DebugToolbarMiddlewareは、レスポンスのHTMLにscriptタグを差し込む処理を行っているためです。

myproject/urls.py:

.. code-block:: python

   from django.urls import include, path  # includeを追加しています

   urlpatterns = [
       # ...
       path("__debug__/", include("debug_toolbar.urls")),
   ]

これでdjango-debug-toolbarのセットアップまで完了です。初回のDBマイグレーションとrunserverで動作確認してください。

.. code-block::

   (venv)$ python manage.py migrate
   (venv)$ python manage.py runserver

http://127.0.0.1:8000/ をブラウザで開いて確認します。

reservationアプリケーションを作成
------------------------------------

.. code-block::

   (venv)$ python manage.py startapp reservation

myproject/settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "reservation",
   ]

TODO: ...


追加課題
--------------------------------

時間に余裕のある人向けの追加課題です。

- ログイン中のユーザーのパスワードを変更する画面を作る
    - パスワード変更を行う画面（フォーム）を作ってみましょう。
    - パスワードを変更するAPIがあります。
    - https://docs.djangoproject.com/ja/5.0/topics/auth/default/#changing-passwords
    - もしくは、 `django.contrib.auth.forms.PasswordChangeForm` や `django.contrib.auth.views.PasswordChangeView` を利用することもできます。
- ユーザー登録にメールアドレスの確認を必須とする
    - メールアドレスを登録していない場合、パスワードリセット等で困る場合があります。
    - django-registrationを使って実装することもできます。
        - https://pypi.org/project/django-registration/
- パスワードリセット画面を実装する
    - 「パスワードを忘れてしまった場合」に対応する画面を作ってみましょう。
    - メールを送信して、メールに書かれたURLからパスワードを設定する画面を造ります。
    - または、 `django.contrib.auth.views.PasswordResetView` を利用することもできます。
- 指定のユーザーに成り代わってログインする
    - Djangoの管理画面から特定のユーザーに成り代わってログインをする機能が欲しい場合、django-hijackを利用できます。試してみましょう。
- 外部の認証プロバイダーによるログインを実現する
    - django-allauthを使うと、XやGoogle、Facebookなどのアカウントを使ったログインを実現できます。
    - SNS等の場合は、OAuthというプロトコルで外部の認証プロバイダーを利用できます。認証プロトコルはOAuth以外にSAMLなどがあります。
