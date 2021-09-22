from typing import Union, Tuple
from functools import total_ordering

from polygon import Polygon

@total_ordering
class Polygons(object):
    """Sequence of all regular polygons from 3 to max_edges
    max_edges is specified at initialization and is the n. of edges of the last polygon
    circumradius is common to all the polygons in the sequence.
    """

    def __init__(self, max_edges:int, circumradius:float = 1)->None:
        if max_edges < 3:
            raise ValueError('Number of max edges should be >= 3.')
        self._max_edges = int(max_edges)
        self._circumradius = circumradius
        self._polygons = tuple(
            Polygon(edges, self.circumradius)
            for edges in range(3, self.max_edges +1)
        )
        self._max_efficient = max(
            self.polygons,
            key = lambda plyg:\
                plyg.area / plyg.perimeter
        )

    def __repr__(self) -> str:
        return f"Polygons({self.max_edges},{self.circumradius})"
    
    @property
    def max_edges(self)->int:
        return self._max_edges
    
    @property
    def circumradius(self)->float:
        return self._circumradius
    
    @property
    def polygons(self)->tuple:
        return self._polygons
    
    @property
    def max_efficient(self)->Polygon:
        return self._max_efficient
    
    def __len__(self):
        return len(self.polygons)

    def __getitem__(self, which: Union[int, slice],
        )->Union[Polygon, Tuple[Polygon]]:
        return self.polygons[which]
    
    def __eq__(self, other)->bool:
        if isinstance(other, self.__class__):
            return self.polygons == other.polygons
        else:
            return NotImplemented

    def __gt__(self, other)->bool:
        if isinstance(other, self.__class__):
            return self[-1] > other[-1]
        else:
            return NotImplemented
        
# if __name__ == '__main__':
#     ps8 = Polygons(8)
#     print(ps8)
#     print(len(ps8))
#     [print(pg) for pg in ps8]
