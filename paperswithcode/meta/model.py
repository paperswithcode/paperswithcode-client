import copy
import logging

from paperswithcode.meta.field import Field
from paperswithcode.meta.resource import Resource


logger = logging.getLogger(__name__)


DEFAULT_LIMIT = 100


class ModelMeta(type):
    """Metaclass for all models.

    The metaclass knows how to inject instance of API from class that contains
    classes with this meta. Class that contains this class has to have 'api'
    property which will be injected into class level API property of Model
    class.

    Creates constructors for all resources and manages instantiation of
    resource fields.
    """

    def __new__(mcs, name: str, bases, data: dict):
        # Attach fields object fo resource instance.
        fields = {}
        for name, field in data.items():
            if isinstance(field, Field):
                if field.name is None:
                    fields[name] = field
                else:  # field has explicit name set in the field constructor
                    fields[field.name] = field
                if field.name is None:
                    field.name = name
        data["_fields"] = fields

        if "__init__" not in data:

            def init(self, **kwargs):
                self._api = kwargs.pop("api", None)
                urls = getattr(self, "urls", None)
                self._data = Resource(urls=urls, api=self._api)
                self._dirty = {}
                for name, value in kwargs.items():
                    if name in fields:
                        value = fields[name].validate(value)
                        self._data[name] = value

                self._old = copy.deepcopy(self._data.data)

            def equals(self, other):
                if not hasattr(other, "__class__"):
                    return False
                if not self.__class__ == other.__class__:
                    return False
                return self is other or self._data == other._data

            def deepcopy(self):
                return self.__class__(api=self._api, **self._data.data)

            if "__str__" not in data:
                data["__str__"] = lambda self: self.__class__.__name__
            if "__repr__" not in data:
                data["__repr__"] = lambda self: str(self)

            data.update(
                {"__init__": init, "equals": equals, "deepcopy": deepcopy}
            )

        return type.__new__(mcs, name, bases, data)

    def __get__(cls, obj, objtype=None):
        if obj is None:
            return cls
        cls._api = obj
        return cls
