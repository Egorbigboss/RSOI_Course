import uuid
from django.db import models
from django.utils.timezone import now



class Stats(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_of_object = models.CharField(null=True,max_length=20)
    text = models.CharField(null=True, max_length=2048)
    count = models.IntegerField(default = 1)
    def __str__(self):
        return f'Stats, uuid={self.uuid}'
