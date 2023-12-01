from abc import ABC, abstractmethod
from math import floor
class Bindernator:

    def __init__(self, data_list,  pages_per_volume, items_per_page, sections=None,use_remainder=False):
        self.volumes = {}
        self.items_per_page = items_per_page
        self.pages_per_volume = pages_per_volume
        self.sections = sections
        #self.section_size = floor(pages_per_volume/sections)
        self.organize_data(data_list)

    def organize_data(self, data_list):
        current_page = 1
        current_volume = 1

        for item in data_list:
            page_number = (current_page - 1) // self.items_per_page + 1
            if page_number > self.pages_per_volume:
                current_page = 1
                current_volume += 1
                page_number = 1

            volume = self.volumes.setdefault(current_volume, {})
            page = volume.setdefault(page_number, [])

            page.append(item)
            current_page += 1

    def get(self, volume_number,page_number=None, row_number=None):
        item = None
        volume = self.volumes[volume_number]
        item = volume
        if page_number:
            page = volume[page_number]
            item = page
            if row_number:
                #rows are arrays reduce by one
                item = page[row_number -1]
        return item