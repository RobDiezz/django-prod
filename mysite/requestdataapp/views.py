"""Модуль для обработки представлений приложения requestdataapp."""

from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    """Обрабатывает GET-запрос и возвращает результат сложения параметров."""
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {"a": a, "b": b, "result": result}
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    """Отображает форму для ввода биографической информации пользователя."""
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    """Обрабатывает загрузку файлов через POST-запрос."""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        http_status = 201
        if form.is_valid():
            # myfile = request.FILES["myfile"]
            myfile = form.cleaned_data["file"]
            max_size: int = 1 * 1024 * 1024
            if myfile.size > max_size:
                return render(
                    request,
                    "requestdataapp/file-upload.html",
                    {"error": "File size exceeds the limit of 1 MB"},
                )

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print(f"Saved file: {filename}")
    else:
        form = UploadFileForm()
        http_status = 200

    context = {
        "form": form,
    }

    return render(request, "requestdataapp/file-upload.html", context=context, status=http_status)
