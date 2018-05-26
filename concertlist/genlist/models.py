from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django import forms
from django.utils.html import conditional_escape as esc
from django.utils.safestring import mark_safe
from itertools import groupby
from calendar import HTMLCalendar, monthrange


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Event(models.Model):
    # day = models.DateField(u'Day of the event', help_text=u'Start Date')
    # subject = models.TextField(u'Band Name', help_text=u'Band Name', blank=True, null=True)
    day = models.DateField(help_text=u'Start Date')
    # day = models.DateField(u'End Date', help_text=u'End Date')
    start_time = models.TimeField(help_text=u'Starting time')
    end_time = models.TimeField(help_text=u'Ending time')
    # all_day_event = models.BooleanField(initial=False)
    notes = models.TextField(blank=True, null=True)
    # private = models.BooleanField(initial=False)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Scheduling'
        verbose_name_plural = 'Scheduling'

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:  # edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (
                new_end >= fixed_start and new_end <= fixed_end):  # innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end:  # outter limits
            overlap = True

        return overlap

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return u'<a href="%s">%s at %s</a>' % (url, str(self.notes), str(self.start_time))

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('Cant End before it Starts!')

        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

class searchBandSugg(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100)
    username = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True, blank=True)

    def __str__(self):
        return self.name +" added."

    def get_absolute_url(self):
        return reverse('shows')
