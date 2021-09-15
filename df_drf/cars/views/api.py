from cars.models import *
from cars.serializers import *
from django.utils import timezone
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import viewsets,status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.none()
    serializer_class = BrandSerializer
    authentication_classes = (BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Brand.objects.all()
        if self.request.method == 'GET':
            try:
                if self.request.GET.get('id', u''):
                    queryset = queryset.filter(id=self.request.GET['id'])
                if self.request.GET.get('name', u''):
                    queryset = queryset.filter(name=self.request.GET['name'])
                if self.request.GET.get('created_gt', u''):
                    datetmp = timezone.datetime.strptime(self.request.GET['created_gt'], '%Y%m%d%H%M%S')
                    queryset = queryset.filter(created__gt=datetmp)
                if self.request.GET.get('created_lt', u''):
                    datetmp = timezone.datetime.strptime(self.request.GET['created_lt'], '%Y%m%d%H%M%S')
                    queryset = queryset.filter(created__lt=datetmp)
            except:
                queryset = []
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.num_of_cars == 0:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('{"error":"That Brand have cars, You only can delete Brands wihout cars."}', status=status.HTTP_403_FORBIDDEN)


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.none()
    serializer_class = CarSerializer
    authentication_classes = (BasicAuthentication, OAuth2Authentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Car.objects.all()
        if self.request.method == 'GET':
            try:
                if self.request.GET.get('id', u''):
                    queryset = queryset.filter(id=self.request.GET['id'])
                if self.request.GET.get('name', u''):
                    queryset = queryset.filter(name=self.request.GET['name'])
                if self.request.GET.get('created_gt', u''):
                    datetmp = timezone.datetime.strptime(self.request.GET['created_gt'], '%Y%m%d%H%M%S')
                    queryset = queryset.filter(created__gt=datetmp)
                if self.request.GET.get('created_lt', u''):
                    datetmp = timezone.datetime.strptime(self.request.GET['created_lt'], '%Y%m%d%H%M%S')
                    queryset = queryset.filter(created__lt=datetmp)
            except:
                queryset = []
        return queryset
