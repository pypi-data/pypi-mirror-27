from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Label(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    auto = models.BooleanField(default=False)

    def __unicode__(self):
        return "{}:{}:{}".format(self.type, self.name, "auto" if self.auto else "manual")

    @staticmethod
    def autocomplete_search_fields():
        return 'name', 'type'

    class Meta:
        unique_together = (('type', 'name', 'auto'), )


class App(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Video(models.Model):
    app = models.ForeignKey(App, null=True)

    hash = models.CharField(max_length=40, db_index=True)

    title = models.CharField(max_length=255)
    url = models.URLField(null=True, max_length=500)
    file = models.FileField(upload_to='library')

    duration = models.FloatField(null=True, blank=True)
    dimension = models.CharField(max_length=255, blank=True)

    date = models.DateField(null=True, blank=True)
    text = models.TextField(blank=True)

    def __unicode__(self):
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return 'title',


class Clip(models.Model):
    video = models.ForeignKey(Video)
    start_time = models.FloatField()
    end_time = models.FloatField()
    duration = models.FloatField(null=True)

    hash = models.CharField(max_length=40, db_index=True)

    labels = models.ManyToManyField(Label, blank=True)

    file = models.FileField(upload_to='library/clip')
    wav = models.FileField(upload_to='library/wav')

    description = models.TextField(null=True)

    class Meta:
        unique_together = (('video', 'start_time', 'end_time'), )

    def __unicode__(self):
        return "%s(%s-%s)" % (self.video, self.start_time, self.end_time)

    @staticmethod
    def autocomplete_search_fields():
        return 'video__name'


class Image(models.Model):
    video = models.ForeignKey(Video)
    clip = models.ForeignKey(Clip, null=True)
    second = models.IntegerField()
    thumbnail = models.ImageField(upload_to="library/images")

    hash = models.CharField(max_length=40, db_index=True)

    labels = models.ManyToManyField(Label, blank=True)

    class Meta:
        unique_together = (('video', 'second'), )

    def __unicode__(self):
        return "%s(%s)" % (self.video, self.second)

    @staticmethod
    def autocomplete_search_fields():
        return 'clip__video__name',
