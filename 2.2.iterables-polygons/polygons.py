from typing import Iterator, Union, Tuple
from functools import total_ordering

from polygon import Polygon

@total_ordering
class Polygons(object):
    """Iterable of all regular polygons from 3 to max_edges
    max_edges is specified at initialization and is the n. of edges of the last polygon
    circumradius is common to all the polygons in the sequence.
    """

    def __init__(self, max_edges:int, circumradius:float = 1)->None:
        if max_edges < 3:
            raise ValueError('Number of max edges should be >= 3.')
        self._max_edges = int(max_edges)
        self._circumradius = circumradius
        self._max_efficient = None


    def __repr__(self) -> str:
        return f"Polygons({self.max_edges},{self.circumradius})"
    
    @property
    def max_edges(self)->int:
        return self._max_edges
    
    @property
    def circumradius(self)->float:
        return self._circumradius

    def __iter__(self)->Iterator:
        return (
            Polygon(edges, self.circumradius)
            for edges in range(3, self.max_edges +1)
        )
    
    def __reversed__(self):
        return (
            Polygon(edges, self.circumradius)
            for edges in range(self.max_edges, 2, -1)
        )
    
    @property
    def max_efficient(self)->Polygon:
        if self._max_efficient is None:
            self._max_efficient = max(
                self,
                key = lambda plyg:\
                    plyg.area / plyg.perimeter
            )
        return self._max_efficient

    def __eq__(self, other)->bool:
        if isinstance(other, self.__class__):
            return self.max_edges == other.max_edges and \
                all( pgx == pgy for pgx, pgy in zip(self, other))
        else:
            return NotImplemented

    def __gt__(self, other)->bool:
        if isinstance(other, self.__class__):
            return next(reversed(self)) > next(reversed(other))
        else:
            return NotImplemented
        
# if __name__ == '__main__':
#     ps8 = Polygons(8)
#     print(ps8)
#     print(len(ps8))
#     [print(pg) for pg in ps8]
