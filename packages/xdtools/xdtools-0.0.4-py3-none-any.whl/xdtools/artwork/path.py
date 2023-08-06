"""
Contains the definition of Path.
"""

from xdtools.utils.point import Point
from xdtools.artwork.artwork import Artwork


class Path(Artwork):
    """
    A Path.

    === Attributes ===
    name - The name of this Path as it appears in the Layers panel.
	uid - The unique id of this Path.
	position - The position of this Path.

	=== Operations ===
	"""

    def __init__(self, uid, path_data, name='Path', x=0, y=0):
        """Instantiate a new Path."""
        self.uid = uid
        self.path_data = path_data
        self.name = name
        self.position = Point(x, y)

    def __repr__(self):
        """Return a constructor-style representation of this Path."""
        return str.format(
            "Path(uid=\'{}\', name=\'{}\', path_data=\'{}\', position={})",
            self.uid, self.name, self.path_data, self.position)
