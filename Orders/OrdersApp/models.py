import uuid
from django.db import models


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    belongs_to_user_id = models.IntegerField(null=False)
    text = models.CharField(null=True, max_length=2048)
    cloth_uuid = models.UUIDField(null=True)

    def __str__(self):
        return f'Order, uuid={self.uuid}'
