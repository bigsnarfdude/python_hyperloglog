from typing import List
from datasketch import HyperLogLog
import base64
import pickle

class HLLSerializer:
   MAGIC = "%%%"
   
   @staticmethod
   def from_magic_string(hll_hash: str) -> HyperLogLog:
       trimmed = HLLSerializer.un_magic(hll_hash)
       bytes_data = base64.b64decode(trimmed)
       return pickle.loads(bytes_data)
   
   @staticmethod
   def to_magic_string(hll: HyperLogLog) -> str:
       bytes_data = pickle.dumps(hll)
       encoded = base64.b64encode(bytes_data)
       serialized = encoded.decode('utf-8')
       return HLLSerializer.MAGIC + serialized
   
   @staticmethod
   def un_magic(serialized: str) -> str:
       if serialized.startswith(HLLSerializer.MAGIC):
           return serialized[len(HLLSerializer.MAGIC):]
       return "None"

if __name__ == "__main__":
   # Example usage
   hll = HyperLogLog()
   hll.update('test'.encode('utf-8'))
   
   # Serialize
   serialized = HLLSerializer.to_magic_string(hll)
   print(f"Serialized: {serialized}")
   
   # Deserialize
   deserialized = HLLSerializer.from_magic_string(serialized)
   print(f"Deserialized count: {deserialized.count()}")
