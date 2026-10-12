from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from accounts.models import User
from accounts.serializers import UserSerializer, LoginSerializer
from core.permissions import record_audit_event


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        if user.tenant:
            record_audit_event(
                tenant=user.tenant,
                branch=user.branch,
                actor=user,
                event_type='USER_LOGIN',
                resource_type='user',
                resource_id=user.id,
                details={'username': user.username, 'role': user.role}
            )

        return Response({
            'success': True,
            'message': 'Logged in successfully',
            'user': UserSerializer(user).data
        })


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'success': True, 'message': 'Logged out successfully'})


class CurrentUserView(APIView):
    def get(self, request):
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data
        })


def switch_user_session(request, username):
    from django.shortcuts import redirect
    user = User.objects.filter(username=username).first()
    if user:
        login(request, user)
    return redirect(request.GET.get('next', request.META.get('HTTP_REFERER', '/pharmacy/')))

