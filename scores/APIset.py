from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import TrainingResult,EventResult
from .serializers import TrainingResultSerializer,EventResultSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
class TrainingResultViewSet(viewsets.ModelViewSet):
    queryset = TrainingResult.objects.all()
    serializer_class = TrainingResultSerializer
    permission_classes = (AllowAny,)



class EventResultViewSet(viewsets.ModelViewSet):
    queryset = EventResult.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


from django.contrib.auth.models import User
from welcome.models import Account
class LoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        users = User.objects.filter(username=username)
        # 使用authenticate函數驗證用戶名和密碼

        if len(users) == 0:
            return Response({'result': False, 'pkid': 0, 'nickname': 'False'}, status=status.HTTP_200_OK)
        user = authenticate(username=username, password=password)
        nickname = Account.objects.filter(userID=user)
        if len(nickname) == 0:
            nickname = username
        else:
            try:
                nickname = nickname[0].u_name
            except:
                nickname = username

        if user is not None:
            # 如果驗證成功，返回用戶的PKID
            return Response({'result': True, 'pkid': user.pk, 'nickname': f'{nickname}'}, status=status.HTTP_200_OK)
        else:
            # 如果驗證失敗，返回錯誤信息
            return Response({'result': False, 'pkid': 0, 'nickn ame': 'False'}, status=status.HTTP_200_OK)