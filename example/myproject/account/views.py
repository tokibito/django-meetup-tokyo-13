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
