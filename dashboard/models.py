from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.urls import reverse


class Zone(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TerritorialDivision(models.Model):
    zone = models.OneToOneField(Zone, on_delete=models.PROTECT)
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return str(self.zone)


class SiteController(models.Model):
    name = models.CharField(max_length=5, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class HwType(models.Model):
    name = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hw_type = models.ForeignKey(HwType, null=True, on_delete=models.PROTECT)
    oss = models.IntegerField()
    site_controller = models.ForeignKey(SiteController, null=True, on_delete=models.PROTECT)
    territorial_division = models.ForeignKey(TerritorialDivision, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class Cell(models.Model):
    name = models.CharField(max_length=10, unique=True, )
    site = models.ForeignKey(Site, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class AlarmType(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class NotAckAlarm(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(ack=False)


class Alarm(models.Model):
    class Priority(models.TextChoices):
        CRITICAL = 'CR', 'Critical'
        MAJOR  = 'MJ', 'Major'
        MINOR = 'MN', 'Minor'

    type = models.ForeignKey(AlarmType, null=True, on_delete=models.PROTECT, related_name='alarm_type')
    check_result = models.BooleanField()
    ack = models.BooleanField()
    created_at = models.DateTimeField()
    cell = models.ForeignKey(Cell, null=True, blank=True, on_delete=models.PROTECT, related_name='alarm_cell')
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.PROTECT, 
                             related_name='alarm_site', verbose_name='Site/Object')
    priority = models.CharField(max_length=2, choices=Priority.choices, default=Priority.MAJOR)

    objects = models.Manager()
    not_ack_alarm = NotAckAlarm()

    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['created_at'])]

    def __str__(self):
        return str(self.type)
    
    # canonical URL
    def get_absolute_url(self):
        return reverse('dashboard:alarm_detail', args=[self.id])
    
    def get_priority_css_class(self):
        css_classes = {
            self.Priority.CRITICAL: 'badge text-bg-danger',
            self.Priority.MAJOR: 'badge text-bg-warning',
            self.Priority.MINOR: 'badge text-bg-info',
        }
        return css_classes.get(self.priority, 'badge text-bg-primary')
    

class Comment(models.Model):
    alarm = models.ForeignKey(Alarm, null=True, on_delete=models.PROTECT, related_name="comments")
    text = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
            ]
    
    def __str__(self):
        return f'Comment by {self.user} on {self.alarm}'
