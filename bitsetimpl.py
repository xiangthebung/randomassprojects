from typing import Optional
class Bitset:
    # size is constant, cannot access past size
    # convention for this class is it prints the least significant bit first
    def __init__(self, sz: Optional[int], startswith=0):
        if sz == None:
            sz = 0
            tmp = startswith
            while tmp:
                tmp >>= 1
                sz += 1
        self.size = sz
        self.bigits = startswith

    def __int__(self):
        return self[:]

    def __getitem__(self, ind):
        if isinstance(ind, slice):
            start, stop, incr = ind.indices(len(self))
            ret = 0
            mult = 1
            for i in range(start, stop, incr):
                ret += self[i] * mult
                mult *= 2
            return ret

        if ind < 0 or ind >= self.size:
            raise IndexError("out of range")

        return (self.bigits >> ind) & 1

    def __setitem__(self, ind, val):
        if isinstance(ind, slice):
            start, stop, incr = ind.indices(len(self))
            vind = 0
            try:
                for i in range(start, stop, incr):
                    self.bigits = (self.bigits & ~(1 << i)) | val[vind] << i
                    vind += 1
            except:
                raise Exception("failed item set")
            return
        if ind < 0 or ind >= self.size:
            raise IndexError("out of range")
        self.bigits = (self.bigits & ~(1 << ind)) | val << ind

    def __iter__(self):
        for i in range(self.size):
            yield self[i]

    def __len__(self):
        return self.size

    def __str__(self):
        ret = ""
        for i in self:
            ret += str(i)
        return ret

    # trivial operations

    def __iadd__(self, toadd):
        self.bigits += toadd
        return self

    def __isub__(self, tosub):
        self.bigits -= tosub
        if self.bigits < 0:
            raise Exception("less than 0")
        return self

    def __invert__(self):
        mask = (1 << len(self)) - 1 #prevents additional bits from being added
        return Bitset(self.size, mask & ~self.bigits) #But we pass in the size, so previous line is not necessary
    #however, it ensures the code correctness
    

    def __eq__(self, other):
        return int(self) == int(other)

    def __lshift__(self, value):
        return Bitset(None, self.bigits << value)
        # since we are returning a value, the size of the returned bitset must be updated

    def __rshift__(self, value):
        return Bitset(None, self.bigits >> value)

    def __and__(self, other):
        return Bitset(None, self.bigits & int(other))

    def __or__(self, other):
        return Bitset(None, self.bigits | int(other))

    def __xor__(self, other):
        return Bitset(None, self.bigits ^ int(other))

    def __ior__(self, other):
        self.bigits |= int(other)
        return self

    def __ixor__(self, other):
        self.bigits ^= int(other)
        return self


from typing import List
#https://leetcode.com/problems/subsets/
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        b = Bitset(len(nums))
        ret = []
        while True:
            cur = []
            for i,bl in enumerate(b):
                if bl:
                    cur.append(nums[i])
            b+=1
            ret.append(cur)
            if b == 0:
                break
            
        return ret
