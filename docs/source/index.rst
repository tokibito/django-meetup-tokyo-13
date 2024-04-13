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

このシステムのほとんどの機能はログイン中のユーザーのみが利用できるようにします。

ユーザーの種別
~~~~~~~~~~~~~~~~~~~

このシステムを利用するユーザーの種別は以下の３種類を想定します。

* 一般ユーザー `UserType:1:normal`
    * 一般ユーザーが利用可能な会議室を予約できます。
* 上級ユーザー `UserType:2:advanced`
    * 一般ユーザーが利用可能な会議室に加えて、上級ユーザーが利用可能な会議室を予約できます。

会議室一覧
~~~~~~~~~~~~~

利用可能な会議室の一覧を表示します。ログイン中のユーザーの種別によって、表示する会議室を制御します。

会議室の予約フォームへのリンクが表示されます。

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

RoomListViewをurls.pyに登録します。

reservation/urls.py:

.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
       path("", views.RoomListView.as_view(), name="index"),
   ]

reservation/urls.pyをmyproject/urls.pyに登録します。

myproject/urls.py:

.. code-block:: python

   from django.urls import include, path

   urlpatterns = [
       # ...
       path("reservation/", include("reservation.urls")),
   ]

reservation/templates/base.html:

.. code-block:: html+django

   <html>
   <head>
     <title>{% block title %}{% endblock %}</title>
   </head>
   <body>
     {% block content %}{% endblock %}
   </body>

reservation/templates/reservation/index.html:

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}部屋一覧{% endblock %}

   {% block content %}
   <h1>部屋一覧</h1>
   <ul>
     {% for room in object_list %}
       <li>{{ room.name }}</li>
     {% endfor %}
   </ul>
   {% endblock %}

ログイン・ログアウト処理を作成
----------------------------------------

ログイン画面は、 ``django.contrib.auth.views.LoginView`` を利用できます。
ログアウト処理（表示するページは無し）は、 ``django.contrib.auth.views.LogoutView`` を利用できます。

ビューを利用するURLの追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

account/urls.py:

.. code-block:: python

   from django.urls import path
   from django.contrib.auth import views as auth_views

   urlpatterns = [
       path("login/", auth_views.LoginView.as_view(), name="login"),
       path("logout/", auth_views.LogoutView.as_view(), name="logout"),
   ]

LoginViewのデフォルトテンプレートはregistration/login.htmlです。

account/templates/registration/login.html:

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}ログイン{% endblock %}

   {% block content %}
   <h1>ログイン</h1>
   <form method="post">
     {% csrf_token %}
     {{ form.as_p }}
     <button type="submit">ログイン</button>
   </form>
   {% endblock %}

プロジェクトのURLに追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

myproject/urls.py:

.. code-block:: python

   from django.urls import include, path

   urlpatterns = [
       # ...
       path("account/", include("account.urls")),
   ]

ログイン・ログアウトに関する設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ログイン画面のURL、ログアウト処理のURLは ``settings.py`` で設定します。また、ログイン後、ログアウト後の遷移先のURLも設定します。

myproject/settings.py:

.. code-block:: python

   # ログインページのURL
   LOGIN_URL = "login"
   # ログイン後の遷移先のURL
   LOGIN_REDIRECT_URL = "index"
   # ログアウト処理のURL
   LOGOUT_URL = "logout"
   # ログアウト後の遷移先のURL
   LOGOUT_REDIRECT_URL = "login"

.. note::

   このURLの設定はパスを指定するか、URL nameを指定するかのどちらかです。

ログアウトのボタンを設置する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

base.htmlのcontentブロックの後ろに、ログアウトボタンを設置します。

reservation/templates/base.html:

.. code-block:: html+django

   <html>
   <head>
     <title>{% block title %}{% endblock %}</title>
   </head>
   <body>
     {% block content %}{% endblock %}
     <form action="{% url "logout" %}" method="post">
       {% csrf_token %}
       <button type="submit">ログアウト</button>
     </form>
   </body>

.. note::

   ログアウト処理を行うLogoutViewは、POSTメソッドでアクセスする必要があるため、formタグを使っています。

会議室一覧をログインユーザーのみに制限
--------------------------------------------

Viewクラスに対して、ログインを必須としたい場合、LoginRequiredMixinを多重継承で利用します。

reservation/views.py:

.. code-block:: python

   from django.contrib.auth.mixins import LoginRequiredMixin
   from django.views import generic
   from reservation import models

   class RoomListView(LoginRequiredMixin, generic.ListView):
       model = models.Room
       template_name = "reservation/index.html"

       def get_queryset(self):
           available_rooms = models.Room.objects.all()
           return available_rooms

.. note::

   関数ビューの場合、 ``@login_required`` デコレータを利用できます。

これで、会議室一覧にアクセスするためにはログインが必要になります。
ログインしていない場合は、ログイン画面にリダイレクトされます。

会議室一覧でユーザー種別による表示制御
--------------------------------------------

ログインユーザーのユーザー種別によって、表示する会議室を制御します。

ログインユーザーのユーザープロフィールを取得する関数を作成します。

account/models.py:

.. code-block:: python

   # ...
   def get_user_profile(user):
       """ユーザープロフィールを取得する"""
       try:
           return user.user_profile
       except user.__class__.user_profile.RelatedObjectDoesNotExist:
           pass

.. note::

   OneToOneFieldで参照先のレコードが存在しない場合は、RelatedObjectDoesNotExist例外が発生します。
   ここでは、例外をキャッチして ``None`` を返すようにしています。

ユーザープロファイルが取得できない場合にエラーを表示するデコレーターを作成します。

account/decorators.py:

.. code-block:: python

   from django.http import HttpResponseForbidden
   from .models import get_user_profile


   def user_profile_required(view_func):
       def _wrapped_view_func(request, *args, **kwargs):
           user_profile = get_user_profile(request.user)
           if not user_profile:
               return HttpResponseForbidden("ユーザープロフィールがありません")
           return view_func(request, *args, **kwargs)

       return _wrapped_view_func

.. note::

   デコレーターは、関数を引数に取り、新しい関数を返す関数です。ビュー関数に対して使用するデコレーターは、ビュー関数を引数に取り、新しいビュー関数を返す関数です。

作成したuser_profile_requiredデコレーターをRoomListViewに適用します。このとき、ログインを必須とするチェックはプロファイルのチェックよりも先に行う必要があります。

LoginRequiredMixinでは先に処理を実施できないため、method_decoratorを使ってlogin_requiredデコレーターとuser_profile_requiredデコレーターを適用します。

reservation/views.py:

.. code-block:: python

   from django.contrib.auth.decorators import login_required
   from django.views import generic
   from django.utils.decorators import method_decorator
   from account import models as account_models
   from account.decorators import user_profile_required
   from . import models


   @method_decorator([login_required, user_profile_required], name="dispatch")
   class RoomListView(generic.ListView):
       model = models.Room
       template_name = "reservation/index.html"

       def get_queryset(self):
           user_profile = self.request.user.user_profile
           # ユーザー種別によって利用可能な部屋を絞り込む
           if user_profile.user_type == account_models.UserType.NORMAL:
               available_rooms = models.Room.objects.filter(
                   available_user_type=account_models.UserType.NORMAL
               )
           else:
               available_rooms = models.Room.objects.all()
           return available_rooms

.. note::

   Viewクラスは、dispatchメソッドを持っています。dispatchメソッドは、リクエストを処理する前に、各種の処理を行うためのメソッドです。

予約フォームを作成する
--------------------------------

フォームの定義
~~~~~~~~~~~~~~~~~~

予約データを作成するフォームは、 ``forms.ModelForm`` を使います。

reservation/forms.py:

.. code-block:: python

   from django import forms

   from . import models


   class ReservationForm(forms.ModelForm):
       class Meta:
           model = models.Reservation
           fields = ["start", "end"]
           widgets = {
               "start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
               "end": forms.DateTimeInput(attrs={"type": "datetime-local"}),
           }

.. note::

    ``DateTimeInput`` は日時の入力を受け付けるウィジェットです。閲覧したブラウザのローカル日時を使用したブラウザの日時入力を使うため、 ``type`` 属性に ``datetime-local`` を指定しています。

予約フォームを表示するビューを作成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

reservation/views.py:

.. code-block:: python

   # ...
   from django.urls import reverse_lazy
   from django.shortcuts import get_object_or_404
   from account import models as account_models
   from . import forms

   # ...

   @method_decorator([login_required, user_profile_required], name="dispatch")
   class ReservationView(generic.CreateView):
       model = models.Reservation
       template_name = "reservation/reservation.html"
       form_class = forms.ReservationForm
       success_url = reverse_lazy("my_reservation")

       def get_context_data(self, **kwargs):
           kwargs["room"] = self.room
           return super().get_context_data(**kwargs)

       def dispatch(self, request, room_id: int):
           user_profile = self.request.user.user_profile
           # ユーザー種別によって利用可能な部屋を絞り込む
           if user_profile.user_type == account_models.UserType.NORMAL:
               available_rooms = models.Room.objects.filter(
                   available_user_type=account_models.UserType.NORMAL
               )
           else:
               available_rooms = models.Room.objects.all()
           self.room = get_object_or_404(available_rooms, pk=room_id)
           return super().dispatch(request)

       def form_valid(self, form):
           instance = form.save(commit=False)
           instance.room = self.room
           instance.user = self.request.user
           return super().form_valid(form)

テンプレートの作成
~~~~~~~~~~~~~~~~~~~~

reservation/templates/reservation/reservation.html:

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}{{ room.name }} の予約{% endblock %}

   {% block content %}
   <h1>{{ room.name }} の予約</h1>
   <form method="post">
     {{ form.as_p }}
     {% csrf_token %}
     <button type="submit">送信</button>
   </form>
   {% endblock %}

URLを追加
~~~~~~~~~~~~

reservation/urls.py:

.. code-block:: python

   # ...
   urlpatterns = [
       # ...
       path(
           "<int:room_id>/",
           views.ReservationView.as_view(),
           name="reservation",
       ),
   ]

予約フォームへのリンクを会議室一覧に追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

reservation/templates/reservation/index.html:

.. code-block:: html+django

   {% for room in object_list %}
     <li>{{ room.name }} <a href="{% url "reservation" room_id=room.id %}">予約する</a></li>
   {% endfor %}

自分の予約一覧
--------------------

ビューとテンプレートの実装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

reservation/views.py:

.. code-block:: python

   class MyReservationListView(LoginRequiredMixin, generic.ListView):
       model = models.Reservation
       template_name = "reservation/my_reservation_list.html"

       def get_queryset(self):
           return models.Reservation.objects.filter(user=self.request.user)

reservation/templates/reservation/my_reservation_list.html:

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}{{ user.username }} さんの予約{% endblock %}

   {% block content %}
   <h1>{{ user.username }} さんの予約</h1>
   <ul>
     {% for reservation in object_list %}
     <li>
       {{ reservation.room.name }}
       （{{ reservation.start }} - {{ reservation.end }}）
     </li>
     {% endfor %}
   </ul>
   <div>
     <a href="{% url "index" %}">部屋一覧</a>
   </div>
   {% endblock %}

URLを追加
~~~~~~~~~~~~

reservation/urls.py:

.. code-block:: python

   # ...
   urlpatterns = [
       # ...
       path(
           "my_reservation/", views.MyReservationListView.as_view(), name="my_reservation"
       ),
   ]

ユーザー登録画面
--------------------

ユーザー登録のフォーム
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

account/forms.py:

.. code-block:: python

   from django import forms
   from django.contrib.auth import get_user_model
   from .models import UserType
   
   
   class UserRegisterForm(forms.ModelForm):
       user_type = forms.ChoiceField(
           label="ユーザー種別", choices=UserType.choices, required=True
       )
       password = forms.CharField(label="パスワード", widget=forms.PasswordInput)
   
       class Meta:
           model = get_user_model()
           fields = ["username", "password", "user_type"]

ビューとテンプレートの実装
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

account/views.py:

.. code-block:: python

   from django.views.generic import CreateView
   from django.conf import settings
   from django.urls import reverse_lazy
   from .forms import UserRegisterForm
   from .models import UserProfile


   class UserRegisterView(CreateView):
       model = settings.AUTH_USER_MODEL
       form_class = UserRegisterForm
       template_name = "account/register.html"
       success_url = reverse_lazy("login")

       def form_valid(self, form):
           response = super().form_valid(form)
           self.object.set_password(form.cleaned_data["password"])
           self.object.save()
           # ユーザープロフィールを作成する
           UserProfile.objects.create(
               user=self.object, user_type=form.cleaned_data["user_type"]
           )
           return response

account/templates/account/register.html:

.. code-block:: html+django

   {% extends "base.html" %}
   
   {% block title %}ユーザー登録{% endblock %}
   
   {% block content %}
   <h1>ユーザー登録</h1>
   <form method="post">
     {{ form.as_p }}
     {% csrf_token %}
     <button type="submit">登録</button>
   </form>
   {% endblock %}

URLを追加
~~~~~~~~~~~~

account/urls.py:

.. code-block:: python

   # ...
   from . import views
   # ...
   urlpatterns = [
       # ...
       path("register/", views.UserRegisterView.as_view(), name="register"),
   ]

ログイン画面にユーザー登録へのリンクを追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

account/templates/registration/login.html:

.. code-block:: html+django

   # ...
   <div>
     <a href="{% url "register" %}">新規登録</a>
   </div>
   {% endblock %}

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
