"""
Contains the definition of Point.
"""

from xdtools.utils.point import Point
from xdtools.artwork.artwork import Artwork


class Rectangle(Artwork):
    """
    A Rectangle.

    === Attributes ===
    name - The name of this Rectangle as it appears in the Layers panel.
	id - The id of this Rectangle.
	position - The position of this Rectangle.
	width - The width of this Rectangle, in pixels.
	height - The height of this Rectangle, in pixels.

	=== Operations ===
	"""

    def __init__(self, uid, name='Rectangle', x=0, y=0, width=50, height=50):
        """
        Instantiate a new Rectangle.
        """
        self.uid = uid
        self.name = name
        self.position = Point(x, y)
        self.width = width
        self.height = height

    def __repr__(self):
        """Return a constructor-style representation of this Rectangle."""
        return str.format(
            "Rectangle(uid=\'{}\', name=\'{}\', position={}, width={}, height={})",
            self.uid, self.name, self.position, self.width, self.height)
