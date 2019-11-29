import uuid
from DeliveryApp.test_utility import BaseTestCase
from DeliveryApp.models import DeliveryList
from datetime import datetime

class DeliveryListTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'delivery/user/1/'
        self.delivery1, _ = DeliveryList.objects.get_or_create(order_uuid = uuid.uuid4(),user_id = 1, status = 'Ready for delivery')
        self.delivery2, _ = DeliveryList.objects.get_or_create(order_uuid = uuid.uuid4(),user_id = 1, status = 'Not ready for delivery yet')
        self.data_400 = {
            'tap_of_delivery': 30,
        }
        self.data_201 = {
            'order_uuid' : uuid.uuid4(),
            'status' : 'Not ready for delivery yet',
            'user_id' : 1,
            'date_of_creation' : datetime.now().isoformat(timespec='minutes'),
            'days_for_clearing' : 5,
        }

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]['uuid'], str(self.delivery1.uuid))
        self.assertEqual(response[1]['uuid'], str(self.delivery2.uuid))
        self.assertEqual(response[0]['order_uuid'], str(self.delivery1.order_uuid))
        self.assertEqual(response[1]['order_uuid'], str(self.delivery2.order_uuid))
        self.assertEqual(response[0]['user_id'], self.delivery1.user_id)
        self.assertEqual(response[1]['user_id'], self.delivery2.user_id)
        self.assertEqual(response[0]['status'], 'Ready for delivery')
        self.assertEqual(response[1]['status'], 'Not ready for delivery yet')

    # def testPost400(self):
    #     _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)

    def testPost201(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            new = DeliveryList.objects.get(pk=response['uuid'])
        except DeliveryList.DoesNotExist:
            self.assertTrue(False)
            return
        self.assertEqual(new.order_uuid, self.data_201['order_uuid'])
        self.assertEqual(new.user_id, self.data_201['user_id'])
        self.assertEqual(new.status, self.data_201['status'])


class ConcreteDeliveryViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.delivery, _ = DeliveryList.objects.get_or_create(order_uuid = uuid.uuid4(),user_id = 1, status = 'Ready for delivery')
        uuid_tmp = uuid.uuid4()
        self.url_404 = self.url_prefix + f'delivery/{uuid_tmp}/'
        while uuid_tmp == self.delivery.uuid:
            uuid_tmp = uuid.uuid4()
            self.url_404 = self.url_prefix + f'delivery/{uuid_tmp}/'
        self.url = self.url_prefix + f'delivery/{self.delivery.uuid}/'

    def testGet404(self):

        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url, expected_status_code=200)
        self.assertEqual(response['uuid'], str(self.delivery.uuid))
        self.assertEqual(response['order_uuid'], str(self.delivery.order_uuid))
        self.assertEqual(response['user_id'], self.delivery.user_id)
        self.assertEqual(response['status'], self.delivery.status)

    def testDelete(self):
        _ = self.delete_response_and_check_status(url=self.url, expected_status_code=204)
        self.assertEqual(DeliveryList.objects.count(), 0)
