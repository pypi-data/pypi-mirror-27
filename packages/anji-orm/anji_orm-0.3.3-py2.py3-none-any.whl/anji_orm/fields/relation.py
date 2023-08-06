import rethinkdb as R

from .base import AbstractField

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.3.3"
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
        if not self._created_list:
            model_ids = instance._values.get(self.name)
            for model_id in model_ids:
                result = instance.shared.relation_cache[self._table_name].get(model_id)
                if result is None:
                    if model_id is not None:
                        result = self._model_class.get(model_id)
                        instance.shared.relation_cache[self._table_name][model_id] = result
                self._created_list.append(result)
        return self._created_list
