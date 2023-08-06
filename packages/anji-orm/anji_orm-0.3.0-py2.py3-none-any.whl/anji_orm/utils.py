import logging
from enum import Enum
from typing import Any, Dict, Callable, Tuple

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.3.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['process_functions', 'prettify_value']

_log = logging.getLogger(__name__)


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


def prettify_value(value) -> Any:
    if isinstance(value, Enum):
        return value.name
    if isinstance(value, list):
        return [prettify_value(x) for x in value]
    if isinstance(value, dict):
        return {prettify_value(k): prettify_value(v) for k, v in value.items()}
    return value
