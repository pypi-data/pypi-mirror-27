from shuup_testutils.cases import ApiAuthAdminTestCase
from shuup_testutils.generators import ShuupModelsGen
from shuup_testutils.generators import random


class IndexRenderTest(ApiAuthAdminTestCase):
    @classmethod
    def set_up_class(cls):
        super().set_up_class()

    def test_price_min_and_max_values_presence(self):
        price_min_source = random.decimal(min=0, max=100000)
        price_max_source = random.decimal(min=price_min_source, max=100000)
        
        gen = ShuupModelsGen()
        gen.product(price=price_min_source)
        gen.product(price=price_max_source)
        
        response = self.client.get('/catalog')
        # noinspection PyTypeChecker
        price_min_source_int = int(price_min_source)
        # noinspection PyTypeChecker
        price_max_source_int = int(price_max_source)
        self.assert_contains(response, 'min: {},'.format(price_min_source_int))
        self.assert_contains(response, 'max: {},'.format(price_max_source_int))
