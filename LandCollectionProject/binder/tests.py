from .bindernator import *
from unittest import TestCase
from math import ceil
import string
class test_Bindernator(TestCase):

    def setUp(self):
        self.items = 50
        self.volume_size =4
        self.page_size = 2
        self.paginator = OrderBindernator(range(1,self.items),self.volume_size,self.page_size)

    def test_basic_sort(self):

        volumes_count = ceil(self.items / (self.volume_size * self.page_size))

        self.assertEqual(len(self.paginator.volumes),volumes_count)


    def test_alpha_sort(self):
        data_list = []
        for letter in string.ascii_uppercase:
            data_list.append({"name":letter})
        paginator = AlphaBindernator( data_list, self.page_size, ["M","Z"])
        self.assertEqual(paginator.get(1,4,2), [{"name":"G"}])
        
    def test_get_row(self):
        volume = 2
        page =3
        row = 2
        item = self.paginator.get(volume,page,row)
        itemcalc = ((volume -1 )* self.volume_size * self.page_size) + ((page - 1) *self.page_size) + row
        self.assertEqual(item, itemcalc)


    def test_sectionized_sort():
        pass
    def test_sectionized_sort_with_remainder():
        pass




