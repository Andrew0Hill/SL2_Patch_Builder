import numpy as np
from typing import List

def hex_param_name_to_str(name: List, rstrip=True):
    """
    :param name:  List of Hex-encoded ASCII characters.
    :param rstrip: Whether or not to strip the trailing whitespace from the parameter names.
    :return: The parsed parameter name.
    """
    t = bytes.fromhex("".join(name)).decode("utf-8")
    return t.rstrip() if rstrip else t

def str_param_name_to_hex(name: str, pad: int=16):
    """
    :param name: String representation of the patch name
    :param pad: Amount of whitespace padding to append to the name.
    :return: A hexadecimal array representing the string
    """
    return [c.encode("utf-8").hex().upper() for c in name[:pad].ljust(pad)]

def hex_array_to_integer(arr: List):
    """
    :param arr: List of Hex-encoded values to convert to integer
    :return: The parsed array.
    """
    return [int(x, 16) for x in arr]


def integer_array_to_hex(arr: List):
    """
    :param arr: List of integer values to convert to Hex strings.
    :return: The converted array
    """
    return [hex(x).replace("0x", "").rjust(2,"0").upper() for x in arr]

