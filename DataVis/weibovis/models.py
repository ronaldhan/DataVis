from django.db import models


# Create your models here.
# weibo data in one month
class StatsData(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    pntcnt = models.IntegerField()

    def __unicode__(self):
        result = dict()
        result['name'] = self.id
        result['value'] = self.pntcnt
        result['geoCoord'] = [self.x, self.y]
        return result