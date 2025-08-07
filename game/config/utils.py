#!/usr/bin/env python3

# class Utils:
#     @staticmethod
def to_bool(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() == "true"
    if value is None:
        return False
    return bool(value)