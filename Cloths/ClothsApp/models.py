import uuid
from django.db import models


class Cloth(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # belongs_to_order_uuid = models.IntegerField(null=False)
    type_of_cloth = models.CharField(null=True, max_length=2048)
    # cloth_uuid = models.UUIDField(null=True)
    days_for_clearing = models.IntegerField(null = False)

    def __str__(self):
        return f'Cloth, uuid={self.uuid}'
