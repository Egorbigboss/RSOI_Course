import uuid
from django.db import models


class Cloth(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_of_cloth = models.CharField(null=True, max_length=2048)
    days_for_clearing = models.IntegerField(default = 0)

    def __str__(self):
        return f'Cloth, uuid={self.uuid}'
