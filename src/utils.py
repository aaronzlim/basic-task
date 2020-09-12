#!/usr/bin/env python

from typing import Tuple

def hex2rgb(color_hex: str) -> Tuple[int]:
    """Convert a hex color string to an RGB tuple"""
    if color_hex[0] == '#':
        color_hex = color_hex[1:]

    try:
        r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
    except:
        r, g, b = None, None, None

    return r, g, b

def rgb2hex(r: int, g: int, b: int) -> str:
    """Convert RBG to a hex string #RRGGBB"""
    try:
        hex_str = '#'
        for c in (r,g,b):
            hex_str += hex(c)[2:].zfill(2)
    except:
        hex_str = ''
    return hex_str

def rgb2grayscale(r: int, g: int, b: int) -> int:
    """Convert RGB to grayscale"""
    return int((r + g + b) / 3)

def rgb2greyscale(r: int, g: int, b: int) -> int:
    """Convert RGB to grayscale"""
    return rgb2grayscale(r, g, b)

def hilo(a: int, b: int, c: int) -> int:
    """Sum the min and max of a, b, c

    Stack Overflow: https://stackoverflow.com/questions/40233986/python-is-there-a-function-or-formula-to-find-the-complementary-colour-of-a-rgb
    """
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement_color(r: int, g: int, b: int) -> Tuple[int]:
    """Find the complement color for a given RGB"""
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))
