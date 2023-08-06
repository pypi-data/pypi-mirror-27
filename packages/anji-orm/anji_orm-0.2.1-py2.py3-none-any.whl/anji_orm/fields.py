from typing import Callable, Tuple, Type, Any, List, Iterable, Union, Dict
from enum import Enum
from datetime import datetime
from uuid import uuid4
import logging

import rethinkdb as R
import humanize

from .utils import query
from .core import register

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = [
    'AbstractField', 'StringField', 'IntField', 'BooleanField', 'SelectionField',
    'EnumField', 'FloatField', 'DatetimeField', 'ListField', 'DictField', 'LinkField'
]

_log = logging.getLogger(__name__)

LIST_FIELD_SEPARATOR = '|'


class AbstractField(object):  # pylint:disable=too-many-instance-attributes

    _anji_orm_field = True

    def __init__(self, param_type, default=None, **kwargs) -> None:
        """
        :param description: Field description, mostly used for automatic generated commands. Default value is empty string.
        :param default: Field default value, should be strict value or callable function.  Default value is None.
        :param optional: If true, this field is optional.  Default value is False.
        :param reconfigurable: If true, this field can be changed via configure commands.  Default value is False.
        :param definer: If true, this field should be unique per record.  Default value is False.
        :param service: If true, this field used only in internal bot logic.  Default value is False.
        :param field_marks: Additional field marks, to use in internal logic.  Default value is None.
        :param secondary_index: If true, ORM will build secondary_index on this field.  Default value is False.
        :param displayed: If true, this field will be displayed on chat report.  Default value is True.
        :param compute_function: Make field computable and use this function to calculate field value.  Default value is False
        :param cacheable: If false, field value will be recomputed every time on access. Default value is True.
        """
        # Setup fields
        self.param_type: Type = param_type
        self.default: Any = default
        self.description: str = kwargs.pop('description', '')
        self.optional: bool = kwargs.pop('optional', False)
        self.reconfigurable: bool = kwargs.pop('reconfigurable', False)
        self.definer: bool = kwargs.pop('definer', False)
        self.service: bool = kwargs.pop('service', False)
        self.field_marks: List[str] = kwargs.pop('field_marks', None)
        self.secondary_index: bool = kwargs.pop('secondary_index', False)
        self.displayed: bool = kwargs.pop('displayed', True)
        self.compute_function: str = kwargs.pop('compute_function', None)
        self.cacheable: bool = kwargs.pop('cacheable', True)
        # Check rules
        assert not kwargs, f"Cannot parse {kwargs} configuration. What is it?"
        assert not (self.optional and self.definer), f"Field {self.description} should be optional xor definer"
        assert not (self.reconfigurable and self.definer), f"Field {self.description} should be reconfigurable xor definer"
        assert not (self.service and self.definer), f"Field {self.description} should be service xor definer"
        assert self.cacheable or (not self.cacheable and self.compute_function), "Only compute field can be not cacheable"
        compute_function_check = not self.compute_function or (callable(self.compute_function) or isinstance(self.compute_function, str))
        assert compute_function_check, "Compute function should be or callabe, or name of model function"
        # Name will be set by Model Metaclass
        # when field list be fetched
        self.name: str = None

    def wrap_function_with_parameter(
            self, func: Callable,
            required: bool = True, use_default: bool = True) -> Callable:
        kwargs = dict(
            type=self.param_type,
            help=self.description
        )
        if use_default and self.default:
            kwargs['default'] = self.default
        if required:
            parameter_name = self.name
        else:
            parameter_name = f"--{self.name.replace('_', '-')}"
            kwargs['dest'] = self.name
        return register.wrap(
            func,
            parameter_name,
            **kwargs
        )

    def update_keys(self) -> Tuple:
        return (self.name,)

    def update_value(self, instance, _key: str, value) -> None:
        setattr(instance, self.name, value)

    def format(self, value) -> str:  # pylint: disable=no-self-use
        return str(value)

    def _compute_value(self, instance):
        if callable(self.compute_function):
            return self.compute_function(instance)
        return getattr(instance, self.compute_function)()

    def _compute_get_logic(self, instance):
        if not self.cacheable:
            return self._compute_value(instance)
        result = instance._values.get(self.name)
        if result is None:
            result = self._compute_value(instance)
            instance._values[self.name] = result
        return result

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        if self.compute_function:
            return self._compute_get_logic(instance)
        return instance._values.get(self.name)

    def __set__(self, instance, value) -> None:
        if value is not None and not isinstance(value, self.param_type):
            raise ValueError(f'Field {self.name} value should have {str(self.param_type)} type instead of {value}')
        instance._values[self.name] = value


class StringField(AbstractField):

    def __init__(self, default='', **kwargs) -> None:
        super().__init__(
            str,
            default=default,
            **kwargs
        )


class IntField(AbstractField):

    def __init__(self, default=0, **kwargs) -> None:
        super().__init__(
            int,
            default=default,
            **kwargs
        )


class BooleanField(AbstractField):

    def __init__(self, default=False, **kwargs) -> None:
        super().__init__(
            bool,
            default=default,
            **kwargs
        )


class SelectionField(AbstractField):

    def __init__(self, variants: List[List], default=None, **kwargs) -> None:
        assert variants, "You must define some variants"
        if default is None:
            default = variants[0]
        super().__init__(
            str,
            default=default,
            **kwargs
        )
        self.variants = variants

    def __set__(self, instance, value) -> None:
        if value is not None and value not in self.variants:
            raise ValueError(f'Field {self.name} value should be in range {str(self.variants)} type instead of {value}')
        instance._values[self.name] = value


class EnumField(AbstractField):

    def __init__(self, enum_class: Union[Type[Enum], Iterable], default=None, **kwargs) -> None:
        self.variants: List[Enum] = list(enum_class)
        assert self.variants, f"You must define some child in Enum class {enum_class}"
        if default is None:
            default = self.variants[0]
        super().__init__(
            enum_class,
            default=default,
            **kwargs
        )

    def __set__(self, instance, value):
        if value is not None:
            if value in self.param_type.__members__:
                value = self.param_type[value]
            if value not in self.variants:
                raise ValueError(f'Field {self.name} value should be in range {str(self.variants)} type instead of {value}')
        instance._values[self.name] = value


class FloatField(AbstractField):

    def __init__(self, default=0.0, decimal_format: str = "{0:.2f}", **kwargs) -> None:
        super().__init__(
            float,
            default=default,
            **kwargs
        )
        self.decimal_format = decimal_format

    def format(self, value):
        return self.decimal_format.format(value)

    def __set__(self, instance, value):
        """
        Override to fix zero value in rethinkdb
        """
        if isinstance(value, int):
            value = float(value)
        super().__set__(instance, value)


class DatetimeField(AbstractField):

    def __init__(self, default=lambda: datetime.now(R.make_timezone("00:00")), **kwargs) -> None:
        super().__init__(
            datetime,
            default=default,
            **kwargs
        )

    def format(self, value: datetime) -> str:
        return f"{humanize.naturaldate(value)} at {value.strftime('%H:%M:%S')}"


class ListField(AbstractField):

    def __init__(self, default=None, **kwargs) -> None:
        if default is None:
            default = list
        assert not kwargs.get('secondary_index', None), "Currently this is not supported by orm and query builded!"
        super().__init__(
            list,
            default=default,
            **kwargs
        )

    def update_keys(self) -> Tuple:
        return (self.name, f"add_{self.name}", f"remove_{self.name}")

    def update_value(self, instance, key: str, value) -> None:
        if key == self.name:
            setattr(instance, self.name, value.split(LIST_FIELD_SEPARATOR))
        else:
            current_value = getattr(instance, self.name)
            if key.startswith('add_'):
                value = current_value + value
            elif key.startswith('remove_'):
                value = list(set(current_value) - set(value))
            setattr(instance, self.name, value)

    def wrap_function_with_parameter(self, func: Callable, required: bool = True, use_default: bool = True) -> Callable:
        kwargs: Dict[str, Any] = dict(
            # use str type to parse list internal in method
            type=str
        )
        if use_default and self.default:
            kwargs['default'] = self.default
        if required:
            kwargs['help'] = f"{self.description}, для ввода больше одного элемента используйте разделитель {LIST_FIELD_SEPARATOR}"
            return register.wrap(
                func,
                self.name,
                **kwargs
            )
        parameter_name = f"--{self.name.replace('_', '-')}"
        kwargs['dest'] = self.name
        kwargs['help'] = f"{self.description}, для ввода больше одного элемента используйте разделитель {LIST_FIELD_SEPARATOR}"
        func = register.wrap(
            func,
            parameter_name,
            **kwargs
        )
        for mod in ['add', 'remove']:
            parameter_key = mod + '_' + self.name
            if mod == 'add':
                prefix = 'Добавляет к текущему значению поля'
            else:
                prefix = 'Удаляет из текущего значения поля'
            kwargs['help'] = f"{prefix} {self.name} заданное значение. Этот параметр можно использовать несколько раз"
            kwargs['action'] = 'append'
            parameter_name = f"--{(parameter_key).replace('_', '-')}"
            kwargs['dest'] = parameter_key
            func = register.wrap(
                func,
                parameter_name,
                **kwargs
            )
        return func

    def __set__(self, instance, value) -> None:
        if isinstance(value, str):
            value = value.split(LIST_FIELD_SEPARATOR)
        return super().__set__(instance, value)


class DictField(AbstractField):

    def __init__(self, default=None, **kwargs) -> None:
        if default is None:
            default = dict
        assert not kwargs.get('secondary_index', None), "Currently this is not supported by orm and query builded!"
        super().__init__(
            dict,
            default=default,
            **kwargs
        )

    def wrap_function_with_parameter(self, func: Callable, required: bool = True, use_default: bool = True) -> Callable:
        raise NotImplementedError("Wrapping currenty not implemented for dicts")

    def update_value(self, instance, key: str, value) -> None:
        raise NotImplementedError("Update value is currenty not implemented for dicts")


class LinkField(AbstractField):

    def __init__(self, model_class, **kwargs) -> None:
        super().__init__(
            str,
            description=model_class.__doc__,
            default=None,
            **kwargs
        )
        self.key_for_uuid_storing = f'{uuid4()}-link-uuid-key'
        self._model_class = model_class
        self._table = R.table(model_class._table)

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        result = instance._values.get(self.name, None)
        if result is None:
            result_key = instance._values.get(self.key_for_uuid_storing)
            if result_key is not None:
                result = query(
                    self._table.get(result_key)
                )
                instance._values[self.name] = result
        return result

    def __set__(self, instance, value) -> None:
        if value is not None and not isinstance(value, str):
            raise ValueError(f'Field {self.name} value should have uuid of record instead of {value}')
        instance._values[self.key_for_uuid_storing] = value
