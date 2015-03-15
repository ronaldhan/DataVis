from django.contrib.gis.db import models


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


class Grid(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    geom = models.PolygonField()
    objects = models.GeoManager()

    def __unicode__(self):
        return "coordinates: %s,%s " (str(self.x), str(self.y))

    def get_dict(self):
        result = dict()
        result['name'] = self.id
        result['geoCoord'] = [self.x, self.y]
        return result


class WbPoint(models.Model):
    created_at = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    cdate = models.DateField()
    ctime = models.CharField(max_length=8)
    point = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return "source: %s" % self.source