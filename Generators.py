import uuid
import random
from typing import List

class Generator:
   @staticmethod
   def uuid() -> str:
       return str(uuid.uuid4())
       
   @staticmethod
   def random_uuids(numbers_required: int) -> List[str]:
       return [Generator.uuid() for _ in range(numbers_required)]
       
   one_million_uuids = random_uuids(1000000)
   
   hll_hash = "AQBjb20udHdpdHRlci5hbGdlYmlyZC5TcGFyc2VITMwRAww9CAGyBQJiBwKUCAJcDQE="
   
   data1 = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]
   data2 = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]  # Python doesn't distinguish between int/long
   data3 = ["1", "1", "2", "3", "3", "4", "4", "5", "5"]
   
   @staticmethod
   def random_numbers(numbers_required: int, range_number: int) -> List[int]:
       return [random.randint(0, range_number-1) for _ in range(numbers_required)]
       
   one_million_random_numbers = random_numbers(1000000, 100000)
   moar_random_numbers = random_numbers(100000, 200000)
   unique_numbers = len(set(one_million_random_numbers))
   overlapping_numbers = len(set(moar_random_numbers))
