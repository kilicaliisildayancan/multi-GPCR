'''
Implements a union-check tree, which allows group merging and iteration.
Currently works in amortized O(log(N)) work per operation, because the general implementation is messier.
'''

class UnionCheck(object):
    """
    A class that implements an inefficient Union-Check tree.
    Allows asking for the group of an object and merging groups.
    """

    def __init__(self):
        self._groups = {}
    
    def __getitem__(self, obj):
        """
        Gets the group of the object.
        """
        if obj not in self._groups:
            self._groups[obj] = {obj}
        return self._groups[obj]

    def merge(self, obj1, obj2):
        """
        Merges the group of the two objects.
        """
        #The smaller group is added to the large.
        if len(self[obj1]) < len(self[obj2]):
            self.merge(obj2, obj1)
            return
        
        self._groups[obj1] |= self._groups[obj2]

        for obj in self._groups[obj2]:
            self._groups[obj] = self._groups[obj1]

    def groups(self):
        """
        Returns an iterator over all the groups of the UnionCheck.
        """
        return iter(set(map(frozenset, self._groups.values())))