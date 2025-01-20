from typing import List
from datasketch import HyperLogLog
import struct

class HLLMonoid:
    @staticmethod
    def load_list_int(data: List[int]) -> HyperLogLog:
        hll = HyperLogLog(p=12)
        for item in data:
            hll.update(struct.pack('i', item))
        return hll

    @staticmethod
    def load_list_long(data: List[int]) -> HyperLogLog:
        hll = HyperLogLog(p=12)
        for item in data:
            hll.update(struct.pack('q', item))
        return hll

    @staticmethod
    def load_list_string(data: List[str]) -> HyperLogLog:
        hll = HyperLogLog(p=12)
        for item in data:
            hll.update(item.encode('utf-8'))
        return hll

# Example usage
if __name__ == "__main__":
    ints = [1, 2, 3, 4, 5]
    longs = [1000000000, 2000000000, 3000000000]
    strings = ["a", "b", "c", "d"]

    hll_int = HLLMonoid.load_list_int(ints)
    hll_long = HLLMonoid.load_list_long(longs)
    hll_string = HLLMonoid.load_list_string(strings)

    print(f"Estimated cardinality (ints): {hll_int.count()}")
    print(f"Estimated cardinality (longs): {hll_long.count()}")
    print(f"Estimated cardinality (strings): {hll_string.count()}")
