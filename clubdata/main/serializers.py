from rest_framework import serializers

from .models import Club, Match

class ClubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Club
        fields = ['id', 'name']


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'date', 'home', 'away', 'home_goals', 'away_goals', 'result']

    home = ClubSerializer()
    away = ClubSerializer()