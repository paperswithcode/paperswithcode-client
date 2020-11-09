import re
from uuid import UUID
from datetime import datetime
from typing import Optional, Callable, Union, Tuple


from paperswithcode.errors import ReadOnlyPropertyError, ValidationError


class Field(object):
    """Parent class for all fields declared in models."""

    def __init__(
        self,
        name: Optional[str] = None,
        read_only: bool = True,
        nullable: bool = True,
        types: Optional[Union[type, Tuple[type, ...]]] = None,
        validator: Optional[Callable] = None,
    ):
        """Initialization.

        Args:
            name (str, optional): Name of the field.
            read_only (bool): Is this field read only.
            nullable (bool): Can this value be None.
            types (Union[TypeVar, List[TypeVar]], optional): Type or list of
                types to validate using isinstance call.
            validator (Callable, optional): Optional callable used for value
                validation.
        """
        self.name = name
        self.read_only = read_only
        self.nullable = nullable
        self.types = types
        self.validator = validator

    @property
    def type_name(self) -> str:
        """Return the type name."""
        return self.__class__.__name__.replace("Field", "")

    def __set__(self, instance, value):
        # Read only should be probably called set_only_once because it allows
        # the value to be set, but only once.
        if self.read_only and instance._data[self.name] is not None:
            raise ReadOnlyPropertyError(
                f"Field {self.name} is marked as read only!"
            )

        if not self.nullable and value is None:
            raise ValidationError("Value cannot be None.")

        value = self.validate(value)

        try:
            current_value = instance._data[self.name]
            if current_value == value:
                return
        except KeyError:
            pass
        instance._dirty[self.name] = True
        instance._data[self.name] = value

    def __get__(self, instance, cls):
        try:
            data = instance._data[self.name]
            return data
        except (KeyError, AttributeError):
            return None

    def validate(self, value):
        if self.types is not None:
            if not isinstance(value, self.types):
                raise ValidationError(
                    f"Not a valid {self.type_name} value: {value!r}."
                )
        if self.validator is not None:
            value = self.validator(value)
        return value


class IDField(Field):
    """IDField is either an object slug or a uuid."""

    def __init__(
        self,
        name: Optional[str] = None,
        read_only: bool = True,
        nullable: bool = True,
        uuid: bool = False,
    ):
        super().__init__(name=name, read_only=read_only, nullable=nullable)
        self.uuid = uuid

    def validate(self, value):
        if self.uuid:
            try:
                UUID(value)
                return value
            except ValueError:
                raise ValidationError(f"Not a valid ID value: {value!r}.s")

        else:
            match = re.match(r"^[\w-]+$", value)
            if match is None:
                raise ValidationError(f"Not a valid ID value: {value!r}.")
            return value


class BooleanField(Field, dict):
    def __init__(
        self,
        name: Optional[str] = None,
        read_only: bool = True,
        nullable: bool = True,
    ):
        super().__init__(
            name=name, read_only=read_only, nullable=nullable, types=(bool,)
        )


class IntegerField(Field):
    def __init__(
        self,
        name: Optional[str] = None,
        read_only: bool = True,
        nullable: bool = True,
    ):
        super().__init__(
            name=name, read_only=read_only, nullable=nullable, types=(int,)
        )


class FloatField(Field):
    def __init__(
        self,
        name: Optional[str] = None,
        read_only: bool = True,
        nullable: bool = True,
    ):
        super().__init__(
            name=name,
            read_only=read_only,
            nullable=nullable,
            types=(int, float),
        )

    def validate(self, value):
        try:
            return float(value)
        except ValueError:
            raise ValidationError(r"Not a valid Float value: {value!r}")


class StringField(Field):
    def __init__(
        self,
        name: Optional[str] = None,
        read_only: bool = False,
        nullable: bool = True,
        max_length: Optional[int] = None,
    ):
        super().__init__(
            name=name, read_only=read_only, nullable=nullable, types=(str,)
        )
        self.max_length = max_length

    def validate(self, value):
        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                f"Maximal length exceeded: "
                f"max_length={self.max_length}, length={len(value)}."
            )
        return value


class DateTimeField(Field):
    def __get__(self, instance, cls):
        data = super().__get__(instance, cls)
        if data:
            fmt = "%Y-%m-%dT%H:%M:%S"
            if "." in data:
                fmt += ".%f"
            if "Z" in data:
                fmt += "Z"
            return datetime.strptime(data, format)
