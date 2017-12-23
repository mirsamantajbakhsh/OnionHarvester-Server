from django.db import models


class Pool(models.Model):
    client_id = models.CharField(max_length=32)
    address_range_start = models.CharField(max_length=16)
    address_range_end = models.CharField(max_length=16)
    dis_time = models.DateTimeField()


class Response(models.Model):
    address = models.CharField(max_length=16)
    port = models.IntegerField()
    check_time = models.DateTimeField()

