import numpy as np
from json import JSONEncoder

def hex_to_str(h: str, rstrip=True):
    """
    :param name:  Hex-encoded ASCII character
    :param rstrip: Whether or not to strip the trailing whitespace from the parameter names.
    :return: The parsed parameter name.
    """
    return bytes.fromhex(h).decode("ascii")

def str_to_hex(s: str, pad: int=16):
    """
    :param name: String representation of the patch name
    :param pad: Amount of whitespace padding to append to the name.
    :return: A hexadecimal array representing the string
    """
    if not s.isascii():
        raise ValueError("Provided string cannot be ASCII encoded!")

    return s.encode("ascii").hex().upper()

def hex_to_int(x: str):
    """
    :param arr: List of Hex-encoded values to convert to integer
    :return: The parsed array.
    """
    return int(x,16)


def int_to_hex(x: int):
    """
    :param arr: List of integer values to convert to Hex strings.
    :return: The converted array
    """
    return hex(x).replace("0x","").rjust(2,"0").upper()
