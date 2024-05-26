import datetime
import random

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from config.permissions import IsSuperUserOrAdminUser
from .models import PasswordResetModel
from .serializers import UserCreateSerializer, ChangePasswordSerializer, UserSerializer


class RegisterView(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
    http_method_names = ('post', )

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        res = {
            'variant': 'success',
            'msg': 'User is successfully created',
            'innerData': serializer.data,
            'totalCount': self.queryset.count()
            }

        return Response(res, status=status.HTTP_201_CREATED, headers=headers)


@api_view(["GET", "POST"])
def reset_password(request):
    if request.method == 'GET':
        user = get_user_model().objects.filter(username=request.data.get('username')).first()
        if user:
            num1 = random.randint(100, 999)
            num2 = random.randint(100, 999)
            code = PasswordResetModel.objects.create(user_id=user, reset_code=f'{num1}{num2}')
            code.save()
            send_mail(
                subject="Reset Password",
                message=f"Your confirm code {num1}-{num2}",
                from_email="forlesson02@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response(data={"status": "success", "code": status.HTTP_200_OK,
                                  "message": "Code sent successfully."
                                             "The code is valid for 10 minutes",
                                  "email": user.email})
        else:
            return Response(data={"status": "filed", "code": status.HTTP_404_NOT_FOUND,
                                  "message": "Username not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        if code is None or new_password is None:
            return Response(
                data={
                    'status': 'failed',
                    'reuired fileds': {
                        'code': int,
                        'new_password': str
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            reset_user = PasswordResetModel.objects.filter(reset_code=code, is_valid=True).last()
            if reset_user is None:
                return Response(
                    data={
                        'status': 'failed',
                        'message': 'invalid code'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user = get_user_model().objects.filter(pk=reset_user.user_id)
                user.set_password(new_password)
                user.save()
                return Response(
                    data={
                        'status': 'success',
                        'message': 'Password successfully changed'
                    },
                    status=status.HTTP_200_OK
                )
    else:
        return Response(
            data={
                'status': 'fail',
                'message': 'This method is not allowed'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUserOrAdminUser, ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(is_superuser=False))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={'Error': 'Token has not found.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def update_user(request, pk):
    try:
        if request.user.is_superuser:
            try:
                user = get_user_model().objects.get(pk=pk)
            except:
                return Response(data={"msg": "User was not found"}, status=status.HTTP_404_NOT_FOUND)
            user.is_staff = not user.is_staff
            user.updatedAt = datetime.datetime.now()
            user.save()
            serializer = UserSerializer(instance=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": "You don't have permission"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(data={"msg": "International server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def error_404(request, pk=None):
    return Response(data={'message': "Page not found"}, status=status.HTTP_404_NOT_FOUND)
