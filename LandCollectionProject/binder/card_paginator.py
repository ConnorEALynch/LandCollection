from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args
import inspect
from math import ceil
from django.utils.translation import gettext_lazy as _
from django.core.paginator import *

class CardPaginator:
    def __init__(self, object_list, binderInfo, binder, volume):

        self.serialized = True
        if binderInfo.pages:
            self.num_pages = binderInfo.pages
            self.serialized = False
        self.per_page = binderInfo.items_per_page
        self.object_list = object_list
        self.binder = binder
        self.volume = volume

    def __iter__(self):
        for page_number in self.page_range:
            yield self.page(page_number)

    def validate_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger(_("That page number is not an integer"))
        if number < 1:
            raise EmptyPage(_("That page number is less than 1"))
        if number > self.num_pages:
            raise EmptyPage(_("That page contains no results"))
        return number

    def get_page(self, number):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            number = self.validate_number(number)
        except PageNotAnInteger:
            number = 1
        except EmptyPage:
            number = self.num_pages
        return self.page(number)

    def page(self, number):
        """Return a Page object for the given 1-based page number."""
        number = self.validate_number(number)
        result = self.object_list
        if self.serialized:
            bottom = (number - 1) * self.per_page
            top = bottom + self.per_page
            if top  >= self.count:
                top = self.count
            result = self.object_list[bottom:top]

        return self._get_page(result, number, self)


    def _get_page(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Page(*args, **kwargs)
    

    @cached_property
    def count(self):
        """Return the total number of objects, across all pages."""
        c = getattr(self.object_list, "count", None)
        if callable(c) and not inspect.isbuiltin(c) and method_has_no_args(c):
            return c()
        return len(self.object_list)

    @cached_property
    def num_pages(self):
        """Return the total number of pages."""
        if self.count == 0 and not self.allow_empty_first_page:
            return 0
        hits = max(1, self.count)
        return ceil(hits / self.per_page)

    @property
    def page_range(self):
        """
        Return a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)



    def get_elided_page_range(self, number=1, *, on_each_side=3, on_ends=2):
        """
        Return a 1-based range of pages with some values elided.

        If the page range is larger than a given size, the whole range is not
        provided and a compact form is returned instead, e.g. for a paginator
        with 50 pages, if page 43 were the current page, the output, with the
        default arguments, would be:

            1, 2, …, 40, 41, 42, 43, 44, 45, 46, …, 49, 50.
        """
        number = self.validate_number(number)

        if self.num_pages <= (on_each_side + on_ends) * 2:
            yield from self.page_range
            return

        if number > (1 + on_each_side + on_ends) + 1:
            yield from range(1, on_ends + 1)
            yield self.ELLIPSIS
            yield from range(number - on_each_side, number + 1)
        else:
            yield from range(1, number + 1)

        if number < (self.num_pages - on_each_side - on_ends) - 1:
            yield from range(number + 1, number + on_each_side + 1)
            yield self.ELLIPSIS
            yield from range(self.num_pages - on_ends + 1, self.num_pages + 1)
        else:
            yield from range(number + 1, self.num_pages+ 1)



