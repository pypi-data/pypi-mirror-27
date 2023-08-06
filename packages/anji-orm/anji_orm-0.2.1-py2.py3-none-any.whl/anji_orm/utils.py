from importlib import import_module
import logging
from typing import AsyncIterable, Any, Dict, Callable, Tuple

import rethinkdb as R

from .core import register

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.1"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['fetch', 'query', 'fetch_cursor', 'async_query', 'process_functions']

_log = logging.getLogger(__name__)


def fetch(rethink_dict):
    class_module = import_module(rethink_dict['__python_info']['module_name'])
    class_object = getattr(class_module, rethink_dict['__python_info']['class_name'], None)
    if class_object is None:
        _log.warning('Task %s cannot be parsed, because class wasnt found!', rethink_dict['id'])
        return None
    obj = class_object(id_=rethink_dict['id'])
    obj.load(rethink_dict)
    return obj


def query(db_query: R.RqlQuery):
    with register.pool.connect() as conn:
        result = db_query.run(conn)
    if isinstance(result, R.net.DefaultCursor):
        return list(filter(lambda x: x is not None, (fetch(obj_data) for obj_data in result)))
    elif isinstance(result, dict):
        return fetch(result)
    elif isinstance(result, list):
        return list(filter(lambda x: x is not None, (fetch(obj_data) for obj_data in result)))
    elif not result:
        return result
    raise Exception("Unkown query result type!")


async def fetch_cursor(cursor) -> AsyncIterable[Dict[str, Any]]:
    """
    Additonal method that wraps asyncio rethinkDB cursos to AsyncIterable.
    Just util method to allow async for usage
    """
    while await cursor.fetch_next():
        yield await cursor.next()


async def async_query(db_query: R.RqlQuery):
    async with register.pool.connect() as conn:  # pylint: disable=not-async-context-manager
        result = await db_query.run(conn)
    if result.__class__.__name__ == 'AsyncioCursor':
        synced_list = [fetch(obj_data) async for obj_data in fetch_cursor(result)]
        return list(filter(lambda x: x is not None, synced_list))
    elif isinstance(result, dict):
        return fetch(result)
    elif isinstance(result, list):
        return list(filter(lambda x: x is not None, (fetch(obj_data) for obj_data in result)))
    elif not result:
        return result
    raise Exception("Unkown query result type!")


def process_functions(fields_dict: Dict, init_function: Callable, configure_function: Callable, definer_ignore: bool = False) -> Tuple[Callable, Callable]:
    for key, value in sorted(fields_dict.items(), key=lambda x: x[0]):
        # Skip service values
        if value.service:
            continue
        # To keep compatibility for cases when we use fields without model
        # for example, like service configuration for cartridges
        if value.name is None:
            value.name = key
        if not (value.definer and definer_ignore):
            init_function = value.wrap_function_with_parameter(
                init_function,
                required=not value.optional,
                use_default=True
            )
        if value.reconfigurable or (value.definer and not definer_ignore):
            configure_function = value.wrap_function_with_parameter(
                configure_function,
                required=not value.reconfigurable,
                use_default=False
            )
    return init_function, configure_function
