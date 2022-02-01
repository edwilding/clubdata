from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
#router.register(r'clubs', views.ClubViewSet)
#router.register(r'matches', views.MatchViewSet)

urlpatterns = [
    path(r'clubs/', views.ClubListView.as_view(), name='clubs'),
    path(r'matches/', views.MatchListView.as_view(), name='matches'),
    path('', include(router.urls)),
]