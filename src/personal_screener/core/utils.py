from typing import Union, get_args, get_origin


def unwrap_optional(field_type):
    """Return the inner type if field_type is Optional[...]"""
    if get_origin(field_type) is Union:
        args = [arg for arg in get_args(field_type) if arg is not type(None)]
        if len(args) == 1:
            return args[0]
    return field_type