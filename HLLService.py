import redis
from typing import Optional

class HLLService:
   def __init__(self, host: str = "localhost", port: int = 6379):
       self.redis_client = redis.Redis(host=host, port=port)
       
   def put(self, hll_key: str, hll_string: str) -> bool:
       return bool(self.redis_client.set(hll_key, hll_string))
   
   def get(self, hll_key: str) -> Optional[str]:
       value = self.redis_client.get(hll_key)
       return value.decode('utf-8') if value else None
