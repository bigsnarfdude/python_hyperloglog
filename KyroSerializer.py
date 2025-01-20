from typing import Callable, Any
from dataclasses import dataclass
import pickle

@dataclass
class KryoPool:
   pool_size: int
   instantiator: Callable[[], Any]
   
   @staticmethod
   def with_byte_array_output_stream(size: int, inst: Callable[[], Any]) -> 'KryoPool':
       return KryoPool(size, inst)

class KryoSerializer:
   KRYO_POOL_SIZE = 10
   
   @staticmethod
   def get_kryo():
       # Since we don't have Kryo in Python, using pickle instead
       class PickleWrapper:
           @staticmethod
           def to_bytes_with_class(obj: Any) -> bytes:
               return pickle.dumps(obj)
               
           @staticmethod
           def from_bytes(bytes_data: bytes) -> Any:
               return pickle.loads(bytes_data)
               
       return PickleWrapper()
       
   kryo = get_kryo()
