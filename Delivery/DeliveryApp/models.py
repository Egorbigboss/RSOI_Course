import uuid
from django.db import models


class DeliveryList(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_uuid = models.UUIDField(null = True)
    user_id = models.IntegerField(default = 0)
    status = models.CharField(null = True, max_length = 2048)

    def __str__(self):
        return f'DeliveryList, uuid={self.uuid}'
