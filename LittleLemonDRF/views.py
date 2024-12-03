from rest_framework import generics
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.decorators import api_view,permission_classes,throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from .throttles import TenCallsPerMinute

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"Message": "some secret message "})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"Message": "Only manager can see this "})
    else:
        return Response({"Message": "You are not authorized to view this"})
    

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"Message": "successfully throttled"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"Message": "successfully throttled"})
