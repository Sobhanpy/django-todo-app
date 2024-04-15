from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from mail_templated import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from accounts.api.V1.serializer import (
    ResetPasswordEmailSerializer,
    ResetPasswordSerializer
)              

from accounts.api.V1.celery_task import SendEmailWithCelery

class ResetPasswordEmailView(GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user)
        SendEmailWithCelery.delay(
            "email/email.html",
            token,
            "sobhan@gmail.com",
             [user.email]
             )
        return Response({"detail": "email Resend for you..."})

    def get_tokens_for_user(self, user):

        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_data = AccessToken(kwargs.get("token"))
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.set_new_password(request, serializer.validated_data)
            token = serializer.create_new_token(request, serializer.validated_data)

            return Response(
                data={"detail": "password change successfully.", "token": token.key},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {
                    "detail": "your token may be expired or changed structure...",
                    "resend email": "http://127.0.0.1:8000/accounts/api/V1/resend",
                }
            )