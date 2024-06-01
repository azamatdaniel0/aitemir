from rest_framework.views import APIView
from rest_framework.response import Response
import os
from openai import OpenAI 
from .models import Instructions
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, ResetPasswordSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        token = RefreshToken.for_user(user).access_token

        reset_url = f"{request.scheme}://{request.get_host()}/reset-password-confirm/{user.pk}/{token}/"
        send_mail(
            "Password Reset Requested",
            f"Click the link below to reset your password:\n{reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(request.data['password'])
            user.save()
            return Response({"message": "Password has been reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)
        
        
class GetAnswerAPIView(APIView):
    def post(self, request, *args, **kwargs):
        transcription = request.data.get('text')

        if transcription is None:
            return Response({'error': 'Повторите попытку еще раз'}, status=400)

        MODEL="gpt-4o"
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))
        latest_instruction = Instructions.objects.first()
        if not latest_instruction:
            return Response({'error': 'Инструкция не найдена. Пожалуйста, добавьте инструкцию.'}, status=500)
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": latest_instruction.instruction},
                {"role": "user", "content": transcription}
            ]
        )
        answer = completion.choices[0].message.content
        total_tokens = str(completion.usage.total_tokens)
        completion_tokens = str(completion.usage.completion_tokens)
        prompt_tokens = str(completion.usage.prompt_tokens)
        return Response(data={"answer": answer, "prompt_tokens":prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": total_tokens})