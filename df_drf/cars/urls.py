import oauth2_provider.views as oauth2_views
from django.urls import include, re_path
from rest_framework import routers

from cars.views import api as views_api

app_name = 'cars'

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'carbrands', views_api.BrandViewSet)
router.register(r'carmodels', views_api.CarViewSet)

router_slash = routers.DefaultRouter()
router_slash.register(r'carbrands', views_api.BrandViewSet)
router_slash.register(r'carmodels', views_api.CarViewSet)

oauth2_endpoint_views = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    re_path(r'^access_token/$', oauth2_views.TokenView.as_view(), name="access_token"),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'', include(router_slash.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^oauth2/', include((oauth2_endpoint_views, 'oauth2_provider'), namespace='oauth2_provider')),
    ]
