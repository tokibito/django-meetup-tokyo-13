from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils.decorators import method_decorator
from account import models as account_models
from account.decorators import user_profile_required
from . import models
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from account import models as account_models
from . import forms


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


@method_decorator([login_required, user_profile_required], name="dispatch")
class ReservationView(generic.CreateView):
    model = models.Reservation
    template_name = "reservation/reservation.html"
    # フォームクラスを指定
    form_class = forms.ReservationForm
    # 予約完了後の遷移先
    success_url = reverse_lazy("my_reservation")

    def get_context_data(self, **kwargs):
        # テンプレート上で利用するために、部屋情報をコンテキストに追加
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
        # 部屋IDが存在しない場合は404エラーを返す
        self.room = get_object_or_404(available_rooms, pk=room_id)
        return super().dispatch(request)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.room = self.room
        # ログイン中のユーザーを予約ユーザーとして登録
        instance.user = self.request.user
        # CreateViewのform_validメソッドで、instance.save()が呼ばれるので、ここでは呼び出さない
        return super().form_valid(form)


class MyReservationListView(LoginRequiredMixin, generic.ListView):
    model = models.Reservation
    template_name = "reservation/my_reservation_list.html"

    def get_queryset(self):
        # 自分の予約一覧を取得する
        return models.Reservation.objects.filter(user=self.request.user)
