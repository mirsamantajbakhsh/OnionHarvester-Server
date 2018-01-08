import uuid
from datetime import datetime
from django.db import models


class Pool(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_id = models.CharField(max_length=32)
    address_range_start = models.CharField(max_length=16)
    address_range_end = models.CharField(max_length=16)
    dis_time = models.DateTimeField()
    create_time = models.DateTimeField(default=datetime.now)


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=16)
    port = models.IntegerField()
    check_time = models.DateTimeField()
    save_time = models.DateTimeField(default=datetime.now)

