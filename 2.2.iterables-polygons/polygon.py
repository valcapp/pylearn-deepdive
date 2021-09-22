import math
from functools import total_ordering

@total_ordering
class Polygon:
    """ Regular strictly convex polygon whose
    angles are less then 180 deg and sides have equal length
    """

    def __init__(self, edges, circumradius):
        edges = int(edges)
        if edges < 3:
            raise ValueError('Number of edges should be >= 3.')
        if circumradius <= 0:
            raise ValueError('Circuradius should be > 0')
        self._edges = edges
        self._circumradius = circumradius
        self._edge_length = None
        self._apothem = None
        self._perimeter = None
        self._area = None

    def __repr__(self):
        return f"Polygon({self.edges},{self.circumradius})"
    
    @property
    def edges(self):
        return self._edges

    @property
    def vertices(self):
        return self._edges
    
    @property
    def circumradius(self):
        return self._circumradius
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.edges == other.edges
                and self.circumradius == other.circumradius
            )
        else:
            return NotImplemented
    
    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.edges > other.edges
        else:
            return NotImplemented

    @property
    def interior_angle(self):
        n = self.edges
        return (n-2)*180/n

    @property
    def edge_length(self):
        if self._edge_length is None:
            n = self.edges
            r = self.circumradius
            self._edge_length = 2*r*math.sin(math.pi/n)
        return self._edge_length

    @property
    def apothem(self):
        if self._apothem is None:
            n = self.edges
            r = self.circumradius
            self._apothem = r*math.cos(math.pi/n)
        return self._apothem

    @property
    def perimeter(self):
        if self._perimeter is None:
            self._perimeter = self.edges * self.edge_length
        return self._perimeter
    
    @property
    def area(self):
        if self._area is None:
            self._area = self.perimeter * self.apothem / 2
        return self._area

