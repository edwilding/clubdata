from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .serializers import ClubSerializer, MatchSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

from django_filters import rest_framework as filters

from .models import Club, Match


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ClubListView(ListAPIView):
    queryset = Club.objects.all().order_by('name')
    serializer_class = ClubSerializer


class MatchListView(ListAPIView):
    serializer_class = MatchSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Match.objects.all().order_by('-date')
        team1_id = self.request.query_params.get('team1')
        team2_id = self.request.query_params.get('team2')
        if team1_id and team2_id and team1_id.isdigit() and team2_id.isdigit():
            self.team1 = get_object_or_404(Club, pk=int(team1_id))
            self.team2 = get_object_or_404(Club, pk=int(team2_id))
            return queryset.filter(Q(home=self.team1, away=self.team2)|Q(home=self.team2, away=self.team1))
        return Match.objects.none()

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        if hasattr(self, 'team1') and hasattr(self, 'team2'):
            results = self.get_queryset()._get_record(self.team1, self.team2)
            response.data.update(results)
        return response