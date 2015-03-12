from django.db import models


# Create your models here.
# weibo data in one month
class StatsData(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    pntcnt = models.IntegerField()

    def get_dict(self):
        result = dict()
        result['name'] = self.id
        result['value'] = self.pntcnt
        result['geoCoord'] = [self.x, self.y]
        return result

    def get_value(self):
        return self.pntcnt

    def __unicode__(self):
        return "coordinates: %s,%s " (str(self.x), str(self.y))