import uuid
from django.db import models
from django.utils.timezone import now



class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    belongs_to_user_id = models.CharField(null=True,max_length=20)
    text = models.CharField(null=True, max_length=2048)
    type_of_cloth = models.CharField(null=True, max_length = 20)
    cloth_uuid = models.UUIDField(null=True)
    date_of_creation = models.DateTimeField(default = now, blank=True)
    def __str__(self):
        return f'Order, uuid={self.uuid}'
