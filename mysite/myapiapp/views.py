"""Модуль для определения представлений API в приложении myapiapp."""

from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin

from .serializers import GroupSerializer


@api_view()
def hello_world_view(request: Request) -> Response:
    """Возвращает приветственное сообщение."""
    return Response({"message": "Hello World!"})


# TODO 2 варианта как можно отобразить все группы
# class GroupsListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         # data = [group.name for group in groups]
#         serializer = GroupSerializer(groups, many=True)
#         return Response({"groups": serializer.data})


# class GroupsListView(ListModelMixin, GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)


class GroupsListView(ListCreateAPIView):
    """Представление для отображения и создания групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
