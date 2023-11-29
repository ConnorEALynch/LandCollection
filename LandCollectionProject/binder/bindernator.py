from collections.abc import Sequence
import inspect
import warnings
from math import ceil

from django.utils.functional import cached_property
from django.utils.inspect import method_has_no_args
from django.utils.translation import gettext_lazy as _


class UnorderedObjectListWarning(RuntimeWarning):
    pass


class InvalidEntity(Exception):
    pass


class EntityNotAnInteger(InvalidEntity):
    pass


class EmptyEntity(InvalidEntity):
    pass

class Row(Sequence):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator
 


    def __repr__(self):
        return "<Page %s of %s>" % (self.number, self.paginator.num_rows)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                "Page indices must be integers or slices, not %s."
                % type(index).__name__
            )
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_rows

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_row_number(self):
        return self.paginator.validate_page_number(self.number + 1)

    def previous_row_number(self):
        return self.paginator.validate_page_number(self.number - 1)

    def start_index(self):
        """
        Return the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.row_size * (self.number - 1)) + 1

    def end_index(self):
        """
        Return the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_rows:
            return self.paginator.count
        return self.number * self.paginator.row_size


class Page(Sequence):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator
 


    def __repr__(self):
        return "<Page %s of %s>" % (self.number, self.paginator.num_pages)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                "Page indices must be integers or slices, not %s."
                % type(index).__name__
            )
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_page_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_page_number(self.number - 1)

    def start_index(self):
        """
        Return the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.page_size * (self.number - 1)) + 1

    def end_index(self):
        """
        Return the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.page_size

class Volume(Sequence):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def __repr__(self):
        return "<Volume %s of %s>" % (self.number, self.paginator.num_volumes)

    def __len__(self):
        return len(self.object_list)

    def __getitem__(self, index):
        if not isinstance(index, (int, slice)):
            raise TypeError(
                "Volume indices must be integers or slices, not %s."
                % type(index).__name__
            )
        # The object_list is converted to a list so that if it was a QuerySet
        # it won't be a database hit per __getitem__.
        if not isinstance(self.object_list, list):
            self.object_list = list(self.object_list)
        return self.object_list[index]

    def has_next(self):
        return self.number < self.paginator.num_volumes

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.has_previous() or self.has_next()

    def next_page_number(self):
        return self.paginator.validate_volume_number(self.number + 1)

    def previous_page_number(self):
        return self.paginator.validate_volume_number(self.number - 1)

    def start_index(self):
        """
        Return the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        # Special case, return zero if no items.
        if self.paginator.count == 0:
            return 0
        return (self.paginator.page_size * (self.number - 1)) + 1

    def end_index(self):
        """
        Return the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        # Special case for the last page because there can be orphans.
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.page_size

class Bindernator:

    def __init__(self, object_list, volume_size, page_size, row_size=1,sections=1):
        self.object_list = object_list
        self.volume_size = volume_size
        self.page_size = page_size
        self.row_size = row_size
        self.total_items = len(object_list)
        self._check_object_list_is_ordered()
 

    def __iter__(self):
        for page_number in self.page_range:
            yield self.page(page_number)

    
    def validate_row_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise EntityNotAnInteger(_("That row number is not an integer"))
        if number < 1:
            raise EmptyEntity(_("That row number is less than 1"))
        if number > self.num_rows:
            raise EmptyEntity(_("That row contains no results"))
        return number

    def validate_page_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise EntityNotAnInteger(_("That page number is not an integer"))
        if number < 1:
            raise EmptyEntity(_("That page number is less than 1"))
        if number > self.num_pages:
            raise EmptyEntity(_("That page contains no results"))
        return number

    def validate_volume_number(self, number):
        """Validate the given 1-based page number."""
        try:
            if isinstance(number, float) and not number.is_integer():
                raise ValueError
            number = int(number)
        except (TypeError, ValueError):
            raise EntityNotAnInteger(_("That volume number is not an integer"))
        if number < 1:
            raise EmptyEntity(_("That volume number is less than 1"))
        if number > self.num_volumes:
            raise EmptyEntity(_("That volume contains no results"))
        return number
    
    def get_volume(self, volume):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            volume = self.validate_volume_number(volume)
        except EntityNotAnInteger:
            volume = 1
        except EmptyEntity:
            volume = self.num_pages
        return self.volume(volume)

    def volume(self, volume):
        bottom = (volume - 1) * self.volume_size * self.page_size
        top = bottom + self.volume_size * self.page_size

        return self._get_volume(self.object_list[bottom:top], volume, self)

    def _get_volume(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Volume(*args, **kwargs)
    
    def get_row(self, volume, page, row):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            volume = self.get_volume(volume)
            page = self.get_page(volume, page)
            row = self.validate_row_number(row)
        except EntityNotAnInteger:
            row = 1
        except EmptyEntity:
            row = self.num_rows
        return self.row(row)

    def row(self, row):
        bottom = (row - 1) * self.row_size
        top = bottom + self.row_size

        return self._get_row(self.object_list[bottom:top], row, self)

    def _get_row(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return Row(*args, **kwargs)

    def get_page(self, volume, page):
        """
        Return a valid page, even if the page argument isn't a number or isn't
        in range.
        """
        try:
            volume = self.get_volume(volume)
            page = self.validate_page_number(page)
           
        except EntityNotAnInteger:
            page = 1
        except EmptyEntity:
            page = self.num_pages
        return self.page(page)

    def page(self, page):
        """Return a Page object for the given 1-based page number."""
        page = self.validate_page_number(page)
        bottom = (page - 1) * self.page_size
        top = bottom + self.page_size
        return self._get_page(self.object_list[bottom:top], page, self)

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
        if self.count == 0:
            return 0
       
        return ceil(self.count / self.page_size)
    @cached_property
    def num_rows(self):
        """Return the total number of pages."""
        if self.count == 0:
            return 0
       
        return ceil(self.count / self.row_size)
    @cached_property
    def num_volumes(self):
        """Return the total number of pages."""
        if self.count == 0:
            return 0
       
        return ceil(self.count / (self.volume_size * self.page_size))
    @property
    def page_range(self):
        """
        Return a 1-based range of pages for iterating through within
        a template for loop.
        """
        return range(1, self.num_pages + 1)

    def _check_object_list_is_ordered(self):
        """
        Warn if self.object_list is unordered (typically a QuerySet).
        """
        ordered = getattr(self.object_list, "ordered", None)
        if ordered is not None and not ordered:
            obj_list_repr = (
                "{} {}".format(
                    self.object_list.model, self.object_list.__class__.__name__
                )
                if hasattr(self.object_list, "model")
                else "{!r}".format(self.object_list)
            )
            warnings.warn(
                "Pagination may yield inconsistent results with an unordered "
                "object_list: {}.".format(obj_list_repr),
                UnorderedObjectListWarning,
                stacklevel=3,
            )