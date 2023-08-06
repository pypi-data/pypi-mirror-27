from typing import List

import rethinkdb as R

from .base import AbstractField

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.3.5"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['LinkField', 'LinkListField']


class LinkField(AbstractField):

    def __init__(self, model_class, **kwargs) -> None:
        super().__init__(
            str,
            description=model_class.__doc__,
            default=None,
            **kwargs
        )
        self._model_class = model_class
        self._table_name = model_class._table
        self._table = R.table(self._table_name)

    def real_value(self, model_record):
        return model_record._values.get(self.name)

    def __get__(self, instance, instance_type):
        if instance is None:
            # when name not None
            # that mean that field for already processed
            # and will be used only in comparation
            if self.name is not None:
                return self._query_row
            return self
        model_id = instance._values.get(self.name)
        result = instance.shared.relation_cache[self._table_name].get(model_id)
        if result is None:
            if model_id is not None:
                result = self._model_class.get(model_id)
                instance.shared.relation_cache[self._table_name][model_id] = result
        return result


class LinkListField(AbstractField):

    def __init__(self, model_class, **kwargs) -> None:
        super().__init__(
            list,
            description=model_class.__doc__,
            default=None,
            **kwargs
        )
        self._model_class = model_class
        self._table_name = model_class._table
        self._table = R.table(model_class._table)
        self._created_list = []

    def _fetch_from_model_list(self, instance) -> List[str]:
        value_ids = instance._values.get(self.name)
        if value_ids is None:
            value_ids = []
        for model_record in self._created_list:
            if model_record.id not in value_ids:
                value_ids.append(model_record.id)
        return value_ids

    def real_value(self, model_record):
        return self._fetch_from_model_list(model_record)

    def __get__(self, instance, instance_type):
        if instance is None:
            # when name not None
            # that mean that field for already processed
            # and will be used only in comparation
            if self.name is not None:
                return self._query_row
            return self
        if not self._created_list:
            model_ids = instance._values.get(self.name)
            if model_ids:
                for model_id in model_ids:
                    result = instance.shared.relation_cache[self._table_name].get(model_id)
                    if result is None:
                        if model_id is not None:
                            result = self._model_class.get(model_id)
                            instance.shared.relation_cache[self._table_name][model_id] = result
                    self._created_list.append(result)
            else:
                instance._values[self.name] = []
        return self._created_list

    def __set__(self, instance, value) -> None:
        if value is not None and not isinstance(value, self.param_type):
            for value_record in value:
                if not isinstance(value_record, self._model_class):
                    raise ValueError(f"This field only for model for {self._model_class}")
            raise ValueError(f'Field {self.name} value should have {str(self.param_type)} type instead of {value}')
        # None value should be converted to empty dict
        self._created_list.clear()
        if value is None:
            self._created_list = []
        else:
            self._created_list = value
        self._fetch_from_model_list(instance)
