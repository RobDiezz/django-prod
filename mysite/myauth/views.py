"""Модуль для представлений аутентификации и взаимодействия с пользователем."""

from random import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    ListView,
    DetailView,
)
from django.utils.translation import gettext_lazy as _, ngettext

from .form import ProfileForm, UserForm, AvatarUpdateForm
from .models import Profile


class HelloView(View):
    """Представление для отображения приветственного сообщения и количества продуктов."""

    welcome_message = _("welcome hello word")

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Обрабатывает GET-запрос и возвращает приветственное сообщение.

        Извлекает количество продуктов из параметров запроса и формирует строку
        с количеством продуктов в зависимости от их числа.
        """
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(f"<h1>{self.welcome_message}</h1>" f"\n<h2>{products_line}</h2>")


class MyAboutView(TemplateView):
    """Представление для отображения информации о пользователе и редактирования профиля."""

    template_name = "myauth/about-me.html"
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        """
        Добавляет данные в контекст для шаблона.

        Если пользователь аутентифицирован, добавляет форму профиля в контекст.
        """
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["profile_form"] = self.form_class
            return context

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для обновления профиля пользователя."""
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect("myauth:about-me", pk=request.user.pk)
        return self.get_context_data()


class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    """Представление для обновления профиля пользователя."""

    model = User
    form_class = UserForm
    template_name = "myauth/profile-update.html"

    def test_func(self):
        """Проверяет, имеет ли текущий пользователь доступ к обновлению профиля."""
        user = self.get_object()
        return self.request.user.is_staff or self.request.user == user

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст для шаблона."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile_form"] = ProfileForm(
                instance=self.request.user.profile
            )  # Передаем форму профиля в контекст

        return context

    def form_valid(self, form):
        """Обрабатывает валидную форму обновления профиля."""
        profile_form = ProfileForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return super().form_valid(form)
        return super().form_invalid(form)

    def get_success_url(self):
        """Возвращает URL для перенаправления после успешного обновления профиля."""
        return reverse("myauth:about-me", kwargs={"pk": self.object.pk})


class RegisterView(CreateView):
    """Представление для регистрации нового пользователя."""

    form_class = UserCreationForm
    template_name = "myauth/register.html"
    # success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        """Обрабатывает валидную форму регистрации."""
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)

        return response

    def get_success_url(self):
        """Возвращает URL для перенаправления после успешной регистрации."""
        return reverse("myauth:about-me", kwargs={"pk": self.object.pk})


# def login_view(request: HttpRequest):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect("/admin/")
#
#         return render(request, "myauth/login.html")
#
#     username = request.POST["username"]
#     password = request.POST["password"]
#
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect("/shop/products")
#
#     return render(
#         request, "myauth/login.html", {"error": "Invalid username or password."}
#     )


def is_ajax(request):
    """Определяет, является ли запрос AJAX-запросом."""
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def login_view(request):
    """Обрабатывает вход пользователя в систему."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_ajax(request):
                return JsonResponse({"success": True, "redirect_url": "/shop/products"})  # Укажите нужный URL
            else:
                return redirect("/shop/products")
        else:
            if is_ajax(request):
                return JsonResponse({"success": False, "message": "Неверный логин или пароль."})
            else:
                return render(
                    request,
                    "myauth/login.html",
                    {"error": "Invalid username or password."},
                )

    return render(request, "myauth/login.html")


# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse("myauth:login"))


class MyLogoutView(View):
    """Представление для выхода пользователя из системы."""

    def post(self, request):
        """Обрабатывает POST-запрос для выхода пользователя."""
        logout(request)
        next_url = request.POST.get("next", "myauth:login")
        return redirect(next_url)


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Устанавливает cookie для текущего запроса.

    Эта функция устанавливает cookie с именем "fizz" и значением "buzz" на 1 час (3600
    секунд).
    """
    response = HttpResponse("Cookies set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Возвращает значение cookie для текущего запроса.

    Если cookie с именем "fizz" не установлено, возвращает значение по умолчанию.
    """
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    """
    Устанавливает значение в сессии для текущего пользователя.

    Эта функция устанавливает значение "spameggs" в сессии под ключом "foobar".
    """
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    """
    Возвращает значение из сессии.

    Если значение не найдено, возвращает значение по умолчанию.
    """
    value = request.session.get("foobar", "default value")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    """Представление для возврата JSON-ответа с фиксированными данными."""

    def get(self, request: HttpRequest) -> JsonResponse:
        """Обрабатывает GET-запрос и возвращает JSON-ответ."""
        return JsonResponse({"foo": "bar", "spam": "eggs"})


class UserListView(ListView):
    """Представление для отображения списка пользователей."""

    model = User
    template_name = "myauth/user_list.html"
    context_object_name = "users"


class UserDetailView(UserPassesTestMixin, DetailView):
    """Представление для отображения и редактирования профиля пользователя."""

    model = User
    template_name = "myauth/user_profile.html"
    context_object_name = "user"
    form_class = AvatarUpdateForm

    def test_func(self):
        """Проверяет, имеет ли текущий пользователь доступ к просмотру профиля."""
        return self.request.user.is_staff or self.request.user == self.get_object()

    def post(self, request, *args, **kwargs):
        """Обрабатывает POST-запрос для обновления профиля пользователя."""
        user = get_object_or_404(User, pk=kwargs["pk"])
        profile = get_object_or_404(Profile, user=user)

        profile_form = AvatarUpdateForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(self.request.path)
        return self.get_context_data()

    def get_context_data(self, **kwargs):
        """Добавляет дополнительные данные в контекст для шаблона."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["profile_form"] = self.form_class(instance=self.request.user)
            #     AvatarUpdateForm(
            #     instance=self.request.user.profile
            # ))  # Передаем форму профиля в контекст

        return context
