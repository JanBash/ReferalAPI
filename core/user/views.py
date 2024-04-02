# Imports
from rest_framework.views import (
    APIView, 
    Response, 
    status
)

from rest_framework.generics import (
    CreateAPIView, 
    DestroyAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView
)

from. models import MyUser, Refer

from .serializers import (
    UserCreateSerializer,
    ReferCreateSerializer,
    UserDetailSerializer,
    EmailSerializer,
    ReferDeleteSerializer,
    ReferDetailSerializer
)

from .utils import send_email

from rest_framework.permissions import IsAuthenticated

# Views
class UserCreateView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserCreateSerializer

class ReferCreateView(CreateAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferCreateSerializer

class ReferDeleteView(RetrieveDestroyAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferDeleteSerializer
    
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReferDetailSerializer
        elif self.request.method == 'DELETE':
            return ReferDeleteSerializer
    
    def delete(self, request, pk):
        user = MyUser.objects.get(id = request.user.id)
        
        refer = Refer.objects.filter(id = pk).first()
        
        if refer.user.id == user.id:
            refer.delete()
            
            return Response({"status": "Deleted succesfully"}, status = status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You can't delete other user's referal codes"}, status = status.HTTP_405_METHOD_NOT_ALLOWED)
    
class UserDetailView(RetrieveAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserDetailSerializer

class EmailView(APIView):
    # Email send logic
    def post(self, request):
        user = MyUser.objects.get(id = request.user.id)
        serializer = EmailSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            receiver = serializer.validated_data['receiver']
            
            send_email(receiver = [receiver], pk = user.id)
            return Response({'message': 'Email sent succesfully'}, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
