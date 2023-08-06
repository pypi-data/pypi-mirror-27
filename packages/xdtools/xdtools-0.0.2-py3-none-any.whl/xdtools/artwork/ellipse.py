"""
Contains the definition of Ellipse.
"""

from xdtools.utils.point import Point
from xdtools.artwork.artwork import Artwork


class Ellipse(Artwork):
    """
    An ellipse.

    === Attributes ===
    uid - the unique id of this Ellipse.
    name - the name of this Ellipse as it appears in the Layers panel.
    position - the position of this Ellipse.
    width - the width of this Ellipse, in pixels.
    height - the height of this Ellipse, in pixels.

    === Operations ===
    """

    def __init__(self, uid: int, name='Ellipse', x=0, y=0, width=50, height=50) -> None:
        """Instantiate a new Ellipse."""
        self.uid = uid
        self.name = name
        self.position = Point(x, y)
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        """Return a constructor-style representation of this Ellipse."""
        return str.format(
            "Ellipse(uid=\'{}\', name=\'{}\', position={}, width={}, height={})",
            self.uid, self.name, self.position, self.width, self.height)
