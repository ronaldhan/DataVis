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

    def get_dict_xy(self):
        result = dict()
        result['lng'] = self.x
        result['lat'] = self.y
        result['count'] = self.pntcnt
        return result

    def __unicode__(self):
        return "coordinates: %s,%s " (str(self.x), str(self.y))


class Grid(models.Model):
    rid = models.IntegerField()
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
    ctime = models.TimeField()
    point = models.PointField()
    objects = models.GeoManager()

    def __unicode__(self):
        return "source: %s" % self.source


class UserCount(models.Model):
    uid = models.BigIntegerField()
    count = models.IntegerField()

    def __unicode__(self):
        return "%s : %s" % (self.uid, self.count)


class WbPointPop(models.Model):
    created_at = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    cdate = models.DateField()
    ctime = models.TimeField()
    point = models.PointField()
    uid = models.BigIntegerField()
    objects = models.GeoManager()

    def __unicode__(self):
        return "source: %s" % self.source


class SystemModule(models.Model):
    gid = models.IntegerField()
    mcode = models.CharField(max_length=4)
    mparent = models.CharField(max_length=2)
    morder = models.CharField(max_length=2)
    mname = models.CharField(max_length=20)

    def __unicode__(self):
        return "module code: %s" % self.mcode


class SystemRole(models.Model):
    gid = models.IntegerField()
    rname = models.CharField(max_length=20)
    rnote = models.CharField(max_length=20)
    rpermission = models.CharField(max_length=100)
    rtype = models.CharField(max_length=2)

    def get_permission(self):
        return str(self.rpermission).split(',')

    def __unicode__(self):
        return "role name: %s, role permission" % (self.rname, self.rpermission)


class SystemUser(models.Model):
    uid = models.IntegerField()
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=50)
    rtype = models.CharField(max_length=2)

    def __unicode__(self):
        return "user name: %s, user role type" % (self.uname, self.rtype)