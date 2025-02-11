"""Модуль для определения middleware в приложении requestdataapp."""

import time

from django.http import HttpRequest, JsonResponse
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    """Middleware для установки пользовательского агента на запрос."""
    # print("Initial call")

    def middleware(request: HttpRequest):
        """Обрабатывает входящий запрос и устанавливает пользовательский агент."""
        # print("before get response")
        request.user_agent = request.META.get("HTTP_USER_AGENT", "test-agent")
        response = get_response(request)
        # print("after get response")

        return response

    return middleware


class CountRequestMiddleware:
    """Middleware для подсчета количества запросов, ответов и исключений."""

    def __init__(self, get_response):
        """Инициализирует middleware."""
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        """Обрабатывает входящий запрос и увеличивает счетчик запросов."""
        self.requests_count += 1
        # print(f"requests count {self.requests_count}")
        response = self.get_response(request)
        self.responses_count += 1
        # print(f"responses count {self.responses_count}")
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        """
        Обрабатывает исключения и увеличивает счетчик исключений.

        Увеличивает счетчик исключений при возникновении ошибки.
        """
        self.exceptions_count += 1
        # print(f"exceptions count {self.exceptions_count}")


class ThrottlingRequestMiddleware:
    """Middleware для ограничения частоты запросов по IP-адресу."""

    def __init__(self, get_response):
        """Инициализирует middleware."""
        self.get_response = get_response
        self.last_request = {}
        self.time_limit = 0.00001

    def __call__(self, request: HttpRequest):
        """Обрабатывает входящий запрос и применяет ограничения на частоту."""
        ip = request.META["REMOTE_ADDR"]

        if ip not in self.last_request:
            self.last_request[ip] = time.time()
        else:
            current_time_limit = time.time() - self.last_request[ip]
            if current_time_limit < self.time_limit:
                return render(
                    request,
                    "requestdataapp/base.html",
                    {"error": "Limit rate requests"},
                    status=429,
                )
            else:
                self.last_request[ip] = time.time()

        response = self.get_response(request)

        return response
