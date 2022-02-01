from __future__ import annotations

from django.db import models
from django.db.models import Count

from model_utils import Choices


class Club(models.Model):
    name = models.CharField('Club Name', null=False, blank=False, max_length=256)


class MatchQuerySet(models.QuerySet):

    def _get_record(self, team1, team2):
        ret = {
            'wins': 0,
            'draws': 0,
            'losses': 0
        }

        for info in self.filter(home=team1, away=team2).values('result').annotate(win_draw_loss=Count('result')):
            if info['result'] == 'w':
                ret['wins'] += info['win_draw_loss']
            elif info['result'] == 'd':
                ret['draws'] += info['win_draw_loss']
            elif info['result'] == 'l':
                ret['losses'] += info['win_draw_loss']

        #reverse the maths for away games, as results are stored from perspective of the home team
        for info in self.filter(home=team2, away=team1).values('result').annotate(win_draw_loss=Count('result')):
            if info['result'] == 'w':
                ret['losses'] += info['win_draw_loss']
            elif info['result'] == 'd':
                ret['draws'] += info['win_draw_loss']
            elif info['result'] == 'l':
                ret['wins'] += info['win_draw_loss']

        return ret


class MatchManager(models.Manager):

    def get_queryset(self):
        return MatchQuerySet(self.model, using=self._db)


class Match(models.Model):
    
    objects = MatchManager()

    RESULTS = Choices(
        ('l', 'Lose'),
        ('d', 'Draw'),
        ('w', 'Win'),
    )

    date = models.DateField(null=False, blank=False)
    home = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='home_games')
    away = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='away_games')
    home_goals = models.IntegerField(default=0)
    away_goals = models.IntegerField(default=0)
    result = models.CharField(choices=RESULTS, default=RESULTS.d, max_length=2)