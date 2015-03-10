"""Utility functions and constants."""

from src.gfx import Rect

SCALE = 32

def tile2rect(pos, size=(1, 1)):
    """Return a rect given tile coordiantes."""
    return Rect(pos[0]*SCALE, pos[1]*SCALE, size[0]*SCALE, size[1]*SCALE)