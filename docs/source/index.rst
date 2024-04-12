DjangoMeetupTokyo #13 中級者向けハンズオン
==========================================

イベント概要
------------

https://django.connpass.com/event/312782/

中級者向けハンズオンについて
----------------------------

チュートリアルは理解できている、Djangoは使ったことあるけど、使いこなせてない～という人向けのハンズオンです。 用意した資料を見ながら課題を実装していきます。

会議室予約システムの実装を通じて、Djangoの認証機能、ユーザー機能などの使い方を学びます。

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

* 一般ユーザー `UserType:1:normal`
    * 一般ユーザーが利用可能な会議室を予約できます。
* 上級ユーザー `UserType:2:advanced`
    * 一般ユーザーが利用可能な会議室に加えて、上級ユーザーが利用可能な会議室を予約できます。

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

予約は、日付と日時を登録します。他の予約とのぶつかりはチェックしません。

自分の予約一覧
~~~~~~~~~~~~~~~~~

ログイン中のユーザーの予約の一覧を表示します。

ユーザー登録
~~~~~~~~~~~~~~~~~

ユーザー登録をする画面です。

プロジェクトの作成とセットアップ
--------------------------------

Djangoのプロジェクト作成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

今回は ``myproject`` という名前のプロジェクトで作成します。

.. code-block::

   (venv)$ django-admin startproject myproject
   (venv)$ cd myproject

**以降の説明は、このmyprojectディレクトリ以下を起点とします。**

言語とタイムゾーンの設定
~~~~~~~~~~~~~~~~~~~~~~~~

myproject/settings.py:

言語は日本語、タイムゾーンはAsia/Tokyoに設定します。

.. code-block:: python

   LANGUAGE_CODE = "ja"
   TIME_ZONE = "Asia/Tokyo"

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

これでdjango-debug-toolbarのセットアップまで完了です。

初回データベースマイグレーション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

初回のデータベースマイグレーションを行います。

.. code-block::

   (venv)$ python manage.py migrate

管理者ユーザーの作成
~~~~~~~~~~~~~~~~~~~~~~~~

Django管理サイト用のユーザーを作成しておきます。

.. code-block::

   (venv)$ python manage.py createsuperuser

セットアップ状態の動作確認
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

runserverで動作確認してください。

.. code-block::

   (venv)$ python manage.py runserver

http://127.0.0.1:8000/admin/ をブラウザで開いて確認します。Djangoの管理画面が表示されればOKです。

accountアプリケーションを作成
------------------------------------

ユーザーの種別と、ユーザープロフィールを先に定義するため、accountアプリケーションを作成します。

.. code-block::

   (venv)$ python manage.py startapp account

myproject/settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "account",
   ]

ユーザー種別の定義とユーザープロフィールのモデルを作成
--------------------------------------------------------

account/models.py:

.. code-block:: python

   from django.db import models
   from django.conf import settings


   class UserType(models.IntegerChoices):
       """ユーザー種別"""

       NORMAL = 1, "一般"
       ADVANCED = 2, "上級"


   class UserProfile(models.Model):
       """ユーザープロフィール"""
       user = models.OneToOneField(
           settings.AUTH_USER_MODEL,
           on_delete=models.CASCADE,
           verbose_name="ユーザー",
           related_name="user_profile",
       )
       user_type = models.PositiveSmallIntegerField(
           "ユーザー種別", default=0, choices=UserType.choices
       )

       def __str__(self):
           return str(self.user)

       class Meta:
           verbose_name = verbose_name_plural = "ユーザープロフィール"

account/admin.py:

.. code-block:: python

   from django.contrib import admin
   from . import models

   admin.site.register(models.UserProfile)

.. note::

   ユーザープロフィールは、ユーザーと1対1の関係であるため、OneToOneFieldを使っています。

   参考: `1対1のリレーションシップ <https://docs.djangoproject.com/ja/5.0/topics/db/examples/one_to_one/>`_

   AUTH_USER_MODELは、settings.pyで指定されたユーザーモデルです。

   デフォルト値: ``"auth.User"``

マイグレーション
~~~~~~~~~~~~~~~~~~~~~

.. code-block::

   (venv)$ python manage.py makemigrations account
   (venv)$ python manage.py migrate

reservationアプリケーションを作成
------------------------------------

予約機能のためのreservationアプリケーションを作成します。

.. code-block::

   (venv)$ python manage.py startapp reservation

myproject/settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "reservation",
   ]

会議室と予約のモデルを作成
-----------------------------------

reservation/models.py:

.. code-block:: python

   from django.db import models
   from django.contrib.auth.models import User
   from account.models import UserType


   class Room(models.Model):
       """会議室"""
       name = models.CharField("会議室名", max_length=50)
       available_user_type = models.PositiveSmallIntegerField(
           "利用可能ユーザー種別", default=0, choices=UserType.choices
       )

       def __str__(self):
           return str(self.name)

       class Meta:
           verbose_name = verbose_name_plural = "会議室"


   class Reservation(models.Model):
       """予約"""
       room = models.ForeignKey(Room, on_delete=models.CASCADE)
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       start = models.DateTimeField()
       end = models.DateTimeField()

       def __str__(self):
           return f"{self.room} {self.start} - {self.end} by {self.user}"

       class Meta:
           verbose_name = verbose_name_plural = "予約"

ユーザーに紐づくデータは、ForeignKeyでUserモデルを参照しています。

reservation/admin.py:

.. code-block:: python

   from django.contrib import admin
   from . import models

   admin.site.register(models.Room)
   admin.site.register(models.Reservation)

マイグレーション
~~~~~~~~~~~~~~~~~~~~~

.. code-block::

   (venv)$ python manage.py makemigrations reservation
   (venv)$ python manage.py migrate

会議室一覧ページを作成
--------------------------------

reservation/views.py:

.. code-block:: python

   from django.views import generic
   from . import models


   class RoomListView(generic.ListView):
       model = models.Room
       template_name = "reservation/index.html"

       def get_queryset(self):
           available_rooms = models.Room.objects.all()
           return available_rooms

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
