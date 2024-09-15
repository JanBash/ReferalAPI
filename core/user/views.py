# Imports
from rest_framework.views import (
    APIView, 
    Response, 
    status
)

from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    ListAPIView
)

from .models import MyUser, Refer

from .serializers import (
    UserCreateSerializer,
    ReferCreateSerializer,
    UserDetailSerializer,
    EmailSerializer,
    ReferDeleteSerializer,
    ReferDetailSerializer,
    ReferListSerializer
)

from .utils import send_email

from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .filters import ReferFilter

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
            
            send_email(receiver = receiver, pk = user.id)
            return Response({'message': 'Email sent succesfully'}, status = status.HTTP_200_OK)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class ReferListPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class ReferListView(ListAPIView):
    queryset = Refer.objects.all()
    serializer_class = ReferListSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__username']
    ordering_fields = ['created_date', 'expire_date', 'user']
    filterset_class = ReferFilter
    pagination_class = ReferListPagination
    
