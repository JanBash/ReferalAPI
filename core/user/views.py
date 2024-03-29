from rest_framework.views import (
    APIView, 
    Response, 
    status
)

from rest_framework.generics import (
    CreateAPIView, 
    DestroyAPIView,
    RetrieveAPIView,
)

from. models import MyUser, Refer

from .serializers import (
    UserCreateSerializer, 
    UserListSerializer, 
    ReferCreateSerializer,
    UserDetailSerializer,
    EmailSerializer
)

from .utils import send_email

from rest_framework.permissions import IsAuthenticated

class UserCreateView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserCreateSerializer

class ReferCreateView(CreateAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferCreateSerializer

class ReferDeleteView(DestroyAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferCreateSerializer
    
class UserDetailView(RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserDetailSerializer

# class ReferReceiveView(APIView):
    
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             print(request.data)
            
#             send_email()
            
#             return Response({'message': 'Email sent with referral code'}, status=status.HTTP_200_OK)
#         except Refer.DoesNotExist:
#             return Response({'error': 'Referal code does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EmailView(APIView):
    def post(self, request):
        user = MyUser.objects.get(id = request.user.id)
        serializer = EmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            receiver = serializer.validated_data['receiver']
            
            send_email(receiver = [receiver], pk = user.id)
            return Response({'message': 'Email sent succesfully'}, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        