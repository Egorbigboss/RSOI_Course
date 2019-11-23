from django.db import models
import uuid

class Order(models.Model):
    belongs_to_user_id = models.IntegerField(null = False)
    uuid = models.UUIDField(primary_key=True)
    # , default=uuid.uuid4, editable=False)
    text = models.CharField(null=True, max_length=2048)
    cloth_uuid = models.UUIDField(null = True, blank = True)

    def __str__(self):
     return f'Order:{0}'.format(self.uuid)
