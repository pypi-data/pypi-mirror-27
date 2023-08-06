from typing import Dict, Any, Type, List, Callable
from datetime import datetime
from abc import ABCMeta
import logging
from itertools import product
from enum import Enum

import rethinkdb as R

from .core import register
from .fields import DatetimeField, AbstractField
from .utils import query, async_query

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['SharedEnv', 'Model', 'RethinkModelMetaclass']

MODEL_FIELDS_CONTROL = {
    '_aggregate_dict': ['_fields', '_field_marks'],
    '_aggregate_sets': ['_primary_keys'],
    '_inherit_field': ['_table']
}

BASE_COLLECTION_TYPE = (list, tuple)

_log = logging.getLogger(__name__)


class ModifyDisallowException(Exception):

    pass


class RethinkModelMetaclass(ABCMeta):

    @classmethod
    def _aggregate_sets(mcs, bases, namespace, field):
        actual_field = set()
        for base_class in bases:
            if hasattr(base_class, field):
                actual_field.update(getattr(base_class, field))
        if namespace.get(field, None):
            actual_field.update(namespace.get(field))
        namespace[field] = actual_field

    @classmethod
    def _aggregate_dict(mcs, bases, namespace, field):
        actual_field = {}
        for base_class in bases:
            if hasattr(base_class, field):
                actual_field.update(getattr(base_class, field))
        if namespace.get(field, None):
            actual_field.update(namespace.get(field))
        namespace[field] = actual_field

    @classmethod
    def _inherit_field(mcs, bases, namespace: Dict, field: str):
        current_field_exists = field in namespace
        if not current_field_exists:
            for base_class in bases:
                if hasattr(base_class, field):
                    namespace[field] = getattr(base_class, field)
                    break

    @classmethod
    def _block_modify(mcs, bases, namespace, field):
        if namespace.get(field) and (len(bases) > 1 or (len(bases) == 1 and bases[0] != object)):
            raise ModifyDisallowException('Field {} cannot be modified in child classes'.format(field))

    @classmethod
    def _fetch_fields(mcs, namespace):
        fields = namespace.get('_fields', None) or {}
        field_marks = {}
        primary_keys = set()
        remove_list = []
        for attr_name, attr in namespace.items():
            if getattr(attr, '_anji_orm_field', None):
                remove_list.append(attr_name)
                fields[attr_name] = attr
                attr.name = attr_name
                if attr.field_marks:
                    for field_mark in attr.field_marks:
                        field_marks[field_mark] = attr_name
                if attr.definer:
                    primary_keys.add(attr_name)
        primary_keys = sorted(primary_keys)
        namespace['_fields'] = fields
        namespace['_field_marks'] = field_marks
        namespace['_primary_keys'] = primary_keys

    @classmethod
    def _check_primary_keys(mcs, namespace):
        for field_name, field_item in namespace['_fields'].items():
            if not field_item.definer and field_name in namespace['_primary_keys']:
                namespace['_primary_keys'].remove(field_name)

    def __new__(mcs, name, bases, namespace, **kwargs):

        # Process fields

        mcs._fetch_fields(namespace)

        # Execute control actions

        for key, value in MODEL_FIELDS_CONTROL.items():
            if hasattr(mcs, key):
                for field in value:
                    getattr(mcs, key)(bases, namespace, field)

        mcs._check_primary_keys(namespace)

        # Process with register
        result = super().__new__(mcs, name, bases, namespace, **kwargs)

        if namespace.get('_table'):
            register.add_table(namespace.get('_table'), result)

        return result


class BaseQueryStrategy:

    @staticmethod
    def generate_list_filter(values, field_name) -> Callable:
        rethinkdb_expr = R.expr(values)
        return lambda doc: rethinkdb_expr.contains(doc[field_name])

    @staticmethod
    def single_secondary_index_query(search_query: R.RqlQuery, model_class: Type['Model'], index_name: str, search_data: Any) -> R.RqlQuery:
        use_unpack = False
        if isinstance(search_data, BASE_COLLECTION_TYPE):
            if model_class._fields.get(index_name):
                use_unpack = model_class._fields.get(index_name).param_type != list
            else:
                use_unpack = isinstance(search_data[0], BASE_COLLECTION_TYPE)
        if use_unpack:
            search_query = search_query.get_all(*search_data, index=index_name)
        else:
            search_query = search_query.get_all(search_data, index=index_name)
        return search_query

    @staticmethod
    def secondary_indexes_query(search_query: R.RqlQuery, model_class: Type['Model'], group_data: Dict, secondary_indexes: List[str]) -> R.RqlQuery:
        if len(secondary_indexes) == 1:
            return BaseQueryStrategy.single_secondary_index_query(
                search_query, model_class, secondary_indexes[0], group_data.get(secondary_indexes[0])
            )
        secondary_indexes = sorted(secondary_indexes)
        index_data = [group_data.get(x) for x in secondary_indexes]
        if any(filter(lambda x: isinstance(x, list), index_data)):
            index_data = list(product(*(x if isinstance(x, list) else [x] for x in index_data)))
        return BaseQueryStrategy.single_secondary_index_query(
            search_query, model_class, ":".join(secondary_indexes), index_data
        )

    @staticmethod
    def build_query(
            model_class: Type['Model'], group_data: Dict,
            limit: int = None, order_by: str = None, descending: bool = False) -> R.RqlQuery:
        group_data = Model.prettify_value(group_data)
        search_query = R.table(model_class._table)
        secondary_indexes = []
        simple_fields = []
        for group_name in group_data.keys():
            if group_name in model_class._fields and model_class._fields.get(group_name).secondary_index:
                secondary_indexes.append(group_name)
            else:
                simple_fields.append(group_name)
        if secondary_indexes:
            search_query = BaseQueryStrategy.secondary_indexes_query(
                search_query, model_class,
                group_data, secondary_indexes
            )
        for simple_field in simple_fields:
            group_value = group_data.get(simple_field)
            if isinstance(group_value, list) and model_class._fields.get(simple_field).param_type != list:
                search_query = search_query.filter(BaseQueryStrategy.generate_list_filter(group_value, simple_field))
            else:
                search_query = search_query.filter(R.row[simple_field] == group_value)
        if order_by:
            if descending:
                order_by = R.desc(order_by)
            search_query = search_query.order_by(order_by)
        if limit:
            search_query = search_query.limit(limit)
        return search_query


class SharedEnv:

    def __init__(self):
        self._env = {}

    def share(self, key: str, value: Any) -> None:
        self._env[key] = value

    def __getattr__(self, key: str) -> Any:
        if key in self._env:
            return self._env[key]
        raise AttributeError


class Model(object, metaclass=RethinkModelMetaclass):
    """
    Base class with core logic for rethinkdb usage.
    For usage you must define _table and _fields section.
    All object fields, that defined in _fields will be processed in send() and load() methods
    """

    _table = ''
    _fields: Dict[str, AbstractField] = {}
    _field_marks: Dict[str, AbstractField] = {}
    _primary_keys: List[str] = []
    _query_strategy = BaseQueryStrategy

    shared: SharedEnv = SharedEnv()

    orm_last_write_timestamp = DatetimeField(service=True, displayed=False)

    def _process_fields(self, fields_dict, init_kwargs) -> None:
        for key, value in fields_dict.items():
            if value.optional or value.service:
                default_value = init_kwargs.get(key, value.default)
                if callable(default_value):
                    default_value = default_value()
                setattr(self, key, default_value)
            else:
                setattr(self, key, init_kwargs.get(key, None))

    def __init__(self, id_: str = None, **kwargs) -> None:
        """
        Complex init method for rethinkdb method.
        Next tasks will be executed:
        1. Create all fields, that defined in _fields, for object
        3. Set base fields, like connection link.
            Additionally can set id field in some cases (for example in fetch method)
        4. Create table field, to be used in queries
        """
        self._values: Dict[str, Any] = dict()
        self.id: str = id_  # pylint: disable=invalid-name
        self.table: R.RqlQuery = R.table(self._table)
        self._process_fields(self._fields, kwargs)

    def __get_field_value(self, field) -> Any:
        result = getattr(self, field, None)
        if isinstance(result, Model):
            result = result.id
        return Model.prettify_value(result)

    def _build_python_info(self) -> Dict[str, str]:
        return {
            'module_name': self.__class__.__module__,
            'class_name': self.__class__.__name__
        }

    def to_dict(self) -> Dict[str, Any]:
        """
        Utility method to generate dict from object.
        Used to send information to rethinkdb.
        """
        base_dict = {}
        for field_name, _field_item in self._fields.items():
            base_dict[field_name] = self.__get_field_value(field_name)
        base_dict['__python_info'] = self._build_python_info()
        return base_dict

    def update(self, update_dict: Dict[str, Any]) -> None:
        for _, field in self._fields.items():
            required_keys = field.update_keys()
            for key in required_keys:
                value = update_dict.get(key, None)
                if value is not None:
                    field.update_value(self, key, value)
        self.send()

    def send(self) -> Dict:
        """
        Method, that send information to rethinkdb.
        """
        result = None
        self.orm_last_write_timestamp = datetime.now(R.make_timezone("00:00"))
        with register.pool.connect() as conn:
            model_dict = self.to_dict()
            if self.id is None:
                result = self.table.insert(model_dict).run(conn)
                self.id = result['generated_keys'][0]
            else:
                result = self.table.get(self.id).update(model_dict).run(conn)
        return result

    async def async_send(self) -> Dict:
        result = None
        self.orm_last_write_timestamp = datetime.now(R.make_timezone("00:00"))
        async with register.pool.connect() as conn:  # pylint: disable=not-async-context-manager
            model_dict = self.to_dict()
            if self.id is None:
                result = await self.table.insert(model_dict).run(conn)
                self.id = result['generated_keys'][0]
            else:
                result = await self.table.get(self.id).update(model_dict).run(conn)
        return result

    def load(self, rethink_dict=None) -> None:
        """
        Method, that load information to rethinkdb.
        :param rethink_dict: rethinkdb data for this object. Useful in case, when you get this data from rethinkdb previously, for example, in fetch method.
        """
        if not rethink_dict:
            with register.pool.connect() as conn:
                rethink_dict = self.table.get(self.id).run(conn)
        for key, value in rethink_dict.items():
            if key in self._fields:
                setattr(self, key, value)

    async def async_load(self, rethink_dict=None) -> None:
        if not rethink_dict:
            async with register.pool.connect() as conn:  # pylint: disable=not-async-context-manager
                rethink_dict = await self.table.get(self.id).run(conn)
        for key, value in rethink_dict.items():
            if key in self._fields:
                setattr(self, key, value)

    @staticmethod
    def prettify_value(value) -> Any:
        if isinstance(value, Enum):
            return value.name
        if isinstance(value, list):
            return [Model.prettify_value(x) for x in value]
        if isinstance(value, dict):
            return {k: Model.prettify_value(v) for k, v in value.items()}
        return value

    def delete(self) -> None:
        """
        Method, that delete record from base table.
        Warning: you must be very patient and don't use this method with wrong connection.
        Every rethinkdb must be used only in one thread
        """
        with register.pool.connect() as conn:
            self.table.get(self.id).delete().run(conn)

    async def async_delete(self) -> None:
        async with register.pool.connect() as conn:  # pylint: disable=not-async-context-manager
            await self.table.get(self.id).delete().run(conn)

    @classmethod
    def get_query(cls, id_) -> R.RqlQuery:
        return R.table(cls._table).get(id_)

    def build_similarity_dict(self) -> Dict[str, Any]:
        group_data = dict(__python_info=self._build_python_info())
        for primary_key_part in self._primary_keys:
            group_data[primary_key_part] = getattr(self, primary_key_part)
        return group_data

    def find_similar(self) -> List['Model']:
        return query(self.build_query(self.build_similarity_dict()))

    async def async_find_similary(self) -> List['Model']:
        return await async_query(self.build_query(self.build_similarity_dict()))

    @classmethod
    def build_query(
            cls, group_data: Dict,
            limit: int = None, order_by: str = None, descending: bool = False) -> R.RqlQuery:
        return cls._query_strategy.build_query(
            cls, group_data, limit=limit,
            order_by=order_by, descending=descending
        )

    @classmethod
    def unique_groups_query(cls) -> R.RqlQuery:
        return R.table(cls._table).pluck('__python_info', *cls._primary_keys).distinct()

    def to_describe_dict(self, definer_skip=False) -> Dict[str, str]:
        fields = {}
        for field_name, field_item in self._fields.items():
            if field_item.displayed and not (definer_skip and field_item.definer) and getattr(self, field_name) is not None:
                fields[field_item.description] = field_item.format(getattr(self, field_name))
        return fields
