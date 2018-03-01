from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Customer(models.Model):
    location = models.CharField(max_length=60)
    Prefix = models.CharField(max_length=60)
    Connected_Host = models.CharField(max_length=60,default="20.0.0.1")

    def __str__(self):
        return "{0} {1}".format(self.location, self.Prefix)

LEAST_LATENCY = 'LEAST_LATENCY'
BANDWIDTH = 'BANDWIDTH'
HOP_COUNT = 'HOP_COUNT'
INTENT_CHOICES = (
    (LEAST_LATENCY, 'least_latency'),
    (BANDWIDTH, 'bandwidth'),
    (HOP_COUNT, 'hop_count'),
)


class Intent_Data(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Intent_Type = models.CharField(max_length=60, choices=INTENT_CHOICES, default=None)
    Source_IP = models.CharField(max_length=60)
    Destination_IP = models.CharField(max_length=60)
    Path = models.CharField(max_length=500)
    timestamp = models.DateTimeField()

    def __str__(self):
        return "{0} {1} {2}".format(self.Source_IP, self.Destination_IP, self.Path)


class Intent_Path_Data(models.Model):
    Path = models.ForeignKey(Intent_Data, on_delete=models.CASCADE)
    switch = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    cookie = models.CharField(max_length=60)
    priority = models.IntegerField()
    active = models.BooleanField()
    ipv4_src = models.CharField(max_length=60)
    ipv4_dst = models.CharField(max_length=60)
    in_port = models.IntegerField()
    actions = models.CharField(max_length=500)

    def __str__(self):
        return "{0} {1} {2}".format(self.Path, self.switch, self.in_port)
