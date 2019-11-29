import uuid
from ClothsApp.test_utility import BaseTestCase
from ClothsApp.models import Cloth


class ClothsListTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.url = self.url_prefix + 'cloths/all/'
        self.cloth1, _ = Cloth.objects.get_or_create(type_of_cloth = 'test_type',days_for_clearing = 5)
        self.cloth2, _ = Cloth.objects.get_or_create(type_of_cloth = 'test_type1',days_for_clearing = 10)
        self.data_400 = {
            'tap_of_cloth': 30,
        }
        self.data_201 = {
            'type_of_cloth': 'post',
            'days_for_clearing': 15,
        }

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url)
        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]['uuid'], str(self.cloth1.uuid))
        self.assertEqual(response[1]['uuid'], str(self.cloth2.uuid))
        self.assertEqual(response[0]['type_of_cloth'], 'test_type')
        self.assertEqual(response[1]['type_of_cloth'], 'test_type1')
        self.assertEqual(response[0]['days_for_clearing'], 5)

    # def testPost400(self):
    #     _ = self.post_response_and_check_status(url=self.url, data=self.data_400, expected_status_code=400)

    def testPost201(self):
        response = self.post_response_and_check_status(url=self.url, data=self.data_201, expected_status_code=201)
        try:
            new = Cloth.objects.get(pk=response['uuid'])
        except cloth.DoesNotExist:
            self.assertTrue(False)
            return
        self.assertEqual(new.type_of_cloth, self.data_201['type_of_cloth'])
        self.assertEqual(new.days_for_clearing, self.data_201['days_for_clearing'])


class ConcreteClothViewTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.cloth, _ = Cloth.objects.get_or_create(type_of_cloth = "wool", days_for_clearing = 12)
        uuid_tmp = uuid.uuid4()
        self.url_404 = self.url_prefix + f'cloths/{uuid_tmp}/'
        while uuid_tmp == self.cloth.uuid:
            uuid_tmp = uuid.uuid4()
            self.url_404 = self.url_prefix + f'cloths/{uuid_tmp}/'
        self.url = self.url_prefix + f'cloths/{self.cloth.uuid}/'

    def testGet404(self):

        _ = self.get_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testDelete404(self):
        _ = self.delete_response_and_check_status(url=self.url_404, expected_status_code=404)

    def testGet(self):
        response = self.get_response_and_check_status(url=self.url, expected_status_code=200)
        self.assertEqual(response['uuid'], str(self.cloth.uuid))
        self.assertEqual(response['type_of_cloth'], self.cloth.type_of_cloth)
        self.assertEqual(response['days_for_clearing'], self.cloth.days_for_clearing)

    def testDelete(self):
        _ = self.delete_response_and_check_status(url=self.url, expected_status_code=204)
        self.assertEqual(Cloth.objects.count(), 0)
