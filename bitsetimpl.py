
from typing import Optional


class Bitset:
    # size is constant, cannot access past size
    # convention for this class is it prints the least significant bit first
    # This convention is different from C++'s implementation. However, it makes more sense in the context of list slicing. 
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

    # Bitset methods
    def popcount(self):
        sm = 0
        for i in self:
            sm += i
        return sm

    def next_permutation(self):
        i = 0
        while i < len(self) - 1 and self[i] <= self[i + 1]:
            i += 1
        i += 1
        if i == len(self):
            self.bigits = 0
            return
        # When doing next permutation, i returns the first instance of a 0 after a 1
        # For example, looking at least significant first, the starting list looks like this
        # and i will take on this index
        # 0 0 1 1 1 0 1 0 0
        #           ^
        #           i
        # Now to get the next permutation, I want to remove a 1 from less than i like this
        # 0 0 0 1 1 0 1 0 0
        # Then I want to reverse the list before i
        # 1 1 0 0 0 0 1 0 0
        # Then I want to set i to 1
        # 1 1 0 0 0 1 1 0 0
        # This would be the next permutation
        # Mathematically, what I can do is count the number of 1s before index i
        # Subtract 1 from the number of 1s
        # Then construct a Bitset with the 1s at the beginning
        # This can be done by using [::-1], but a smarter way is using the number 2^(# of 1s + 1) -1

        # Note: -1 below can be omitted, but is there to show clarity

        num1 = Bitset(i - 1, self.bigits).popcount() - 1
        # To change the digits before i, I need to use a bitmask
        # I want my bitmask to look like this
        # 0 0 0 0 0 1 1 1 1
        #           ^
        #           i
        # Then & it with bigits and | it with the reversed list

        self.bigits = (
            ((1 << (num1 + 1)) - 1)
            | ((1 << len(self)) - 1 - ((1 << i) - 1)) & self.bigits
            | 1 << i
        )

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
        mask = (1 << len(self)) - 1  # prevents additional bits from being added
        return Bitset(
            self.size, mask & ~self.bigits
        )  # But we pass in the size, so previous line is not necessary

    # however, it ensures the code correctness

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


class Solution:
    # https://leetcode.com/problems/subsets/
    def subsets(self, nums: List[int]) -> List[List[int]]:
        b = Bitset(len(nums))
        ret = []
        while True:
            cur = []
            for i, bl in enumerate(b):
                if bl:
                    cur.append(nums[i])
            b += 1
            ret.append(cur)
            if b == 0:
                break

        return ret

    # https://leetcode.com/problems/combination-sum-iii/
    # Description:
    # Use k distinct numbers from 1 to 9 to sum to n
    # Solution:
    # Use Bitset::next_permutation to go through every possible subset of the list [1,2,...,9] of size k
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        if k > n:
            return []

        b = Bitset(9)
        for i in range(k):
            b[i] = 1

        ret = []
        while True:
            cur = []
            for i, t in enumerate(b):
                if t:
                    cur += [i+1]  # We are adding the ith element of a list of [1,2,...,9], which is i+1

            if sum(cur) == n:
                ret.append(cur)

            b.next_permutation()
            if b == 0:
                break
        return ret
